#!/usr/bin/env python
import os, sys; sys.path.append(os.getcwd())

import server
import select
from socket import *
from sockutil import *


STATE_LOGIN = 0


def on_login(sock, data):
    print '[+] on_login', data


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', 10240))
    except Exception, ex:
        print ex
        return

    buf = ''
    index = 0
    state = STATE_LOGIN
    
    sockutil = SockUtil()
    sockutil.send_request(sock, method='login', username='abc',
                          password='abc', callback=on_login)

    try:
        while True:
            read_socks = [sock]
            read_socks, _, _ = select.select(read_socks, [], [])
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
    except (Exception, KeyboardInterrupt) as ex:
        print ex

    if sock:
        sock.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
