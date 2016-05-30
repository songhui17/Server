#!/usr/bin/env python

__all__ = ['short2str', 'str2short', 'send_message', 'SockUtil']


def short2str(value):
    value &= 0xffff
    low_byte = value & 0xff
    high_byte = value >> 8
    return chr(high_byte) + chr(low_byte)


def str2short(value):
    """
    >>> value = short2str(12)
    >>> str2short(value)
    12
    """
    high_byte = ord(value[0])
    low_byte = ord(value[1])
    return (high_byte << 8) + low_byte


def send_message(sock, data, callback, request_id, callback_map):
    """ payload = {'type':'type_name', ...}
    Exception:
    
    sendall

    """
    data['__request_id__'] = request_id

    payload = repr(data)
    message = '%s%s' % (short2str(len(payload)), payload)
    print '[+] send_message:', message

    if callback and (callback_map is not None):
        print '[+] add callback request_id:', request_id
        callback_map[request_id] = callback

    sock.sendall(message)

    request_id += 1
    return request_id


class SockUtil:

    callback_map = {}
    handler_map = {}
    request_id = 0

    def __init__(self):
        pass

    def _send_message(self, sock, wrapped):
        """_send_message: util

        Exception:

        sendall

        """
        payload = repr(wrapped)
        message = '%s%s' % (short2str(len(payload)), payload)
        print '[+] send_message:', message
        sock.sendall(message)

    def send_request(self, sock, method, **kwargs):
        """send_request(sock, method, callback=method, ...)
        Params:
        method      :??

        Exception:

        sendall

        ValueError  :method is None
        """
        callback = kwargs.pop('callback', None)
        if callback:
            print '[+] add callback request_id:', self.request_id
            self.callback_map[request_id] = callback

        if not method:
            raise ValueError('method is None')

        wrapped = {
            'type': 'request',
            'request_id': self.request_id,
            'handler': method,
            'data': kwargs,
        }
        self._send_message(sock, wrapped)
        self.request_id += 1

    def send_response(self, sock, request_id, **kwargs):
        """send_request(...): 

        Exception:
        
        sendall
        """
        wrapped = {
            'type': 'response',
            'request_id': request_id,
            'status': 'ok',
            'data': kwargs,
        }
        self._send_message(sock, wrapped)

    def send_error(self, sock, request_id, **kwargs):
        """send_error

        Exception:
        
        sendall
        """
        wrapped = {
            'type': 'response',
            'request_id': request_id,
            'status': 'error',
            'data': kwargs,
        }
        self._send_message(sock, wrapped)

    def recv_message(self, sock, payload):
        message = eval(payload)
        print '[+] recv', message
        msg_type = message.get('type', None)
        if not msg_type:
            print '[-] implementation error: message type is not specified'
            return

        data = message.get('data', {})
        if msg_type == 'request':
            handler_name = data.get('handler', None)
            general_handler = self.handler_map.get(handler_name, None)
            if general_handler:
                try:
                    general_handler(**data)
                except:
                    pass
            else:
                print '[-] no handler for', handler_name[0, 10]

            # TODO: to instance
        elif msg_type in ['response', 'error']:
            request_id = message.get('request_id', None)

            if not request_id:
                print '[-] implementation error: request_id is not specified'
                return

            callback = self.callback_map.pop(request_id, None)
            if callback:
                try:
                    callback(sock, **data)
                except:
                    pass
            else:
                print '[-] no callback for request_id:', request_id

    def register_handler(self, key, handler):
        """register_handler:
        Exception

        ValueError  :key exist
        ValueError  :handler is not callable
        """
        if not key:
            raise ValueError('key is None')

        if self.handler_map.has_key(key):
            raise ValueError('key: {0} already register'.format(key))

        if not callable(handler):
            raise ValueError('handle is not a method')

        self.handler_map[key] = handler
