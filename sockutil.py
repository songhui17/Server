#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

__all__ = ['b128tostr', 'strtob128', 'SockUtil', 'dump']


def dump(value):
    """
    >>> dump(1)
    1
    >>> dump('abc')
    'abc'
    >>> a = A()
    >>> dump(a)
    {'a': 1}
    >>> dump(B())
    {'a': {'a': 1}}
    >>> dump({'a': 1, 'b': B()})
    {'a': 1, 'b': {'a': {'a': 1}}}
    """
    if value is None:
        return None
    elif isinstance(value, (int, long, float, str, unicode)):
        return value
    elif isinstance(value, dict):
        ret = {}
        for key, v2 in value.iteritems():
            ret[key] = dump(v2)
        return ret
    elif isinstance(value, (tuple, list)):
        # raise Exception('tuple and list is not supported')
        print '[X] tuple and list must contains single type'
        return [dump(v) for v in value]
    else:
        value_dump = getattr(value, 'dump')
        return value_dump()


class A:
    def dump(self):
        ret = {}
        ret['a'] = 1
        return ret


class B:
    def dump(self):
        ret = {}
        ret['a'] = dump(A())
        return ret


def b128tostr(value):
    value &= 0xffff
    low_byte = value & 0x7f
    high_byte = value >> 7
    return chr(high_byte) + chr(low_byte)


def strtob128(value):
    """
    >>> value = b128tostr(0x8c)
    >>> strtob128(value)
    140
    """
    high_byte = ord(value[0])
    low_byte = ord(value[1])
    return (high_byte << 7) + low_byte


class SockUtil:

    callback_map = {}
    errorcallack_map = {}
    handler_map = {}
    request_id = 1

    def __init__(self):
        pass

    def _encode(self, obj):
        """_encode -> text
        """
        # return repr(wrapped)
        return json.dumps(dump(obj))

    def _decode(self, json_text):
        """_decode -> pathon obj

        >>> obj = {'a':1, 'b':[1,2], 'c':{'m':1,'n':2}}
        >>> sockutil = SockUtil()
        >>> text = sockutil._encode(obj)
        >>> dec_obj = sockutil._decode(text)
        >>> dec_obj == obj
        True

        """
        # return eval(payload)
        return json.loads(json_text)

    def _send_message(self, sock, wrapped):
        """_send_message: util

        Exception:

        sendall

        """
        try:
            payload=  self._encode(wrapped)
        except:
            print '[-] failed to encode message'
            raise
        handler = wrapped.get('handler')
        assert handler is not None, 'handler name must be given'
        total_length = len(payload) + 2 + len(handler)
        # import pdb; pdb.set_trace()
        message = '%s%s%s%s' % (b128tostr(total_length),
                                b128tostr(len(handler)),
                                handler, payload)
        print '[+] send_message len(payload):', len(payload), 'message:', message
        sock.sendall(message)

    def send_request(self, sock, method, **request):  #*args, **kwargs):
        """send_request(sock, method, callback=method, ...)
        Params:
        method      :??

        Exception:

        sendall

        ValueError  :method is None
        """
        # callback = kwargs.pop('callback', None)
        callback = request.pop('callback', None)
        if callback:
            print '[+] add callback request_id:', self.request_id
            self.callback_map[self.request_id] = callback

        # errorcallback = kwargs.pop('onerror', None)
        errorcallback = request.pop('onerror', None)
        if errorcallback:
            print '[+] add errorcallback request_id:', self.request_id
            self.errorcallack_map[self.request_id] = errorcallback

        if not method:
            raise ValueError('method is None')

        wrapped = {
            'type': 'request',
            'request_id': self.request_id,
            'require_response': callback is not None,
            'handler': '%s_request' % method,
            # 'args': args,  # remove args
            # 'kwargs': kwargs,
            'request': request
        }
        self._send_message(sock, wrapped)
        self.request_id += 1

    def send_response(self, sock, request_id, request_handler, response):  # *args, **kwargs):
        """send_request(...): 

        Exception:
        
        sendall
        """
        wrapped = {
            'type': 'response',
            'request_id': request_id,
            'handler' : '%s_response' % request_handler,
            # 'args': args,
            # 'kwargs': kwargs,
            'response': response
        }
        self._send_message(sock, wrapped)

    def send_error(self, sock, request_id, request_handler, error):  # *args, **kwargs):
        """send_error(sock, request_id, error=...) : error is required to
        simplify communication with CSharp, use kwargs only

        Exception:
        
        sendall
        """
        wrapped = {
            'type': 'error',
            'request_id': request_id,
            'handler': '%s_error' % request_handler,
            # 'args': args,
            # 'kwargs': kwargs,
            'error': error
        }
        self._send_message(sock, wrapped)

    def _skip_str(self, payload):
        length = strtob128(payload[0:2])
        return payload[2 + length:]

    def recv_message(self, sock, payload):
        """recv_message
        Exception:

        sock.sendall
        """
        payload = self._skip_str(payload)  #skip handler

        try:
            # message = eval(payload)
            message = self._decode(payload)
        except SyntaxError:
            print '[-] failed to parse response: syntax error'
            raise
        except:
            # TODO: concrete
            print '[-] failed to parse response', payload
            raise

        print '[+] recv', message
        msg_type = message.get('type', None)
        if msg_type is None:
            print '[-] implementation error: message type is not specified'
            return

        if msg_type == 'request':
            args = message.get('args', ())
            # kwargs = message.get('kwargs', {})
            kwargs = message.get('request', {})

            handler_name = message.get('handler', None)
            general_handler = self.handler_map.get(handler_name, None)
            if general_handler == 'get_actor_level_info_request':
                import pdb; pdb.set_trace()

            request_id = message.get('request_id', None)
            require_response = message.get('require_response', False)
            if general_handler:
                try:
                    ret = general_handler(*args, **kwargs)
                    if request_id is not None and require_response:
                        print '[+] send response:', ret
                        self.send_response(sock, request_id, handler_name, response=ret)
                except Exception, ex:
                    # TODO: serialize exception/error
                    print '[-] send error:', str(ex)
                    self.send_error(sock, request_id, handler_name, error=str(ex))
            else:
                info = '[-] no handler for %s' % handler_name[0:10]
                print info
                self.send_error(sock, request_id, handler_name, error=info)

            # TODO: to instance
        elif msg_type in ['response', 'error']:
            request_id = message.get('request_id', None)

            if request_id is None:
                print '[-] implementation error: request_id is not specified'
                return

            callback = self.callback_map.pop(request_id, None)
            response = message.get('response', {})

            errorcallback = self.errorcallack_map.pop(request_id, None)
            error = message.get('error', {})

            if msg_type == 'response':
                if callback:
                    try:
                        if isinstance(response, dict):
                            callback(sock, request_id=request_id, **response)  # *args, **kwargs)
                        else:
                            callback(sock, response, request_id=request_id)
                    except Exception, ex:
                        print '[-] failed to callback', ex
                    except:
                        print '[-] failed to callback'
                else:
                    print '[-] no callback for request_id:', request_id

            if msg_type == 'error':
                if errorcallback:
                    try:
                        if isinstance(error, dict):
                            errorcallback(sock, request_id=request_id, **error)  # *args, **kwargs)
                        else:
                            errorcallback(sock, error, request_id)
                    except Exception, ex:
                        print '[-] failed to callback', ex
                    except:
                        print '[-] failed to callback'
                else:
                    print '[-] no errorcallback for request_id:', request_id
                    # TODO: drop current connection/socket
                    raise Exception('uncaught remote error')

    def register_handler(self, key, handler):
        """register_handler: $(key)_request will be register
        Exception

        ValueError  :key exist
        ValueError  :handler is not callable
        """
        if not key:
            raise ValueError('key is None')

        key = '%s_request' % key
        if self.handler_map.has_key(key):
            raise ValueError('key: {0} already register'.format(key))

        if not callable(handler):
            raise ValueError('handle is not a method')

        self.handler_map[key] = handler


if __name__ == '__main__':
    import doctest
    doctest.testmod()
