#!/usr/bin/env python
import os, sys; sys.path.append(os.getcwd())

import server
import select
from socket import *
from sockutil import *


STATE_DONE = -1
STATE_LOGIN = 0


class Handler:
    state = STATE_LOGIN
    sockutil = None

    def _remote(self, sock, method, *args, **kwargs):
        callback = getattr(self, 'on_%s' % method)
        onerror = getattr(self, 'on_%s_error' % method)

        self.sockutil.send_request(
            sock, method=method, callback=callback, onerror=onerror,
            *args, **kwargs)

    def on_login(self, sock, ret):
        _, errno = ret
        if errno == server.E_OK:
            print '[+] on_login ok'

            self.sockutil.send_request(
                sock, method='get_account_info',
                username='abc', callback=self.on_get_account_info,
                onerror=self.on_get_account_info_error)
        else:
            print '[-] on_login failed, errno:', errno
            self.state = STATE_DONE

    def on_login_error(self, sock, error):
        print '[-] on_login_error:', error
        self.state = STATE_DONE

    def on_get_account_info(self, sock, data):
        print '[+] on_get_account_info:', data
        actor_id = data.get('actor_id', None)
        if actor_id:
            print '[-] fatal error'
            # raise
            self.state = STATE_DONE

        if actor_id == -1:
            self._remote(sock, 'create_actor', username='abc', actorname='sniper')
        else:
            self._remote(sock, 'get_actor_info', username='abc')

    def on_get_account_info_error(self, sock, error):
        print '[-] on_get_account_info:', error
        self.state = STATE_DONE

    def on_create_actor(self, sock, ret):
        _, errno = ret
        if errno == server.E_OK:
            print '[+] on_create_actor ok'
            self._remote(sock, 'get_actor_info', username='abc')
        else:
            print '[-] on_create_actor failed, errno:', errno
            self.state = STATE_DONE

    def on_create_actor_error(self, sock, error):
        print '[-] on_create_actor_error:', error
        self.state = STATE_DONE

    def on_get_actor_info(self, sock, ret):
        data, errno = ret
        if errno == server.E_OK:
            print '[+] on_get_actor_info ok'
            print data
            self.state = STATE_DONE
        else:
            print '[-] on_get_actor_info failed'
            self.state = STATE_DONE

    def on_get_actor_info_error(self, sock, error):
        print '[-] on_get_actor_info_error'
        self.state = STATE_DONE

def main():
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', 10240))
    except Exception, ex:
        print ex
        return

    buf = ''
    index = 0
    
    handler = Handler()
    sockutil = SockUtil()
    handler.sockutil = sockutil

    sockutil.send_request(sock, method='login', username='abc',
                          password='abc', callback=handler.on_login,
                          onerror=handler.on_login_error)

    try:
        while True:
            read_socks = [sock]
            read_socks, _, _ = select.select(read_socks, [], [], 1)
            if sock in read_socks:
                recved = sock.recv(1024)
                if len(recved) == 0:
                    print '[+] close socket'
                    print '[+] buf', buf, 'index', index
                    sock.close()
                    break

                # import pdb; pdb.set_trace()
                buf += recved
                buf = buf[index:]
                index = 0
                if len(buf) >= 2:
                    prev_index = index

                    msg_length = str2short(buf[index:index+3])
                    index+=2
                    if msg_length > 1024:
                        # TODO: handle and close socket
                        raise Exception('fatal error')
                    if msg_length < len(buf) - index:
                        # not ready
                        index = prev_index
                    else:
                        payload = buf[index:index+msg_length]
                        index += msg_length
                        sockutil.recv_message(sock, payload)

            if handler.state == STATE_DONE:
                break
            print '.',
    except (Exception, KeyboardInterrupt) as ex:
        print ex

    if sock:
        sock.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
