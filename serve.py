#!/usr/bin/python
import time
import argparse
import threading
import functools
import SocketServer


PRINT_OUT = False
BUF_SIZE = 8192
p = lambda *args, **kwargs: ()


def pretty_print(fmt, data, mode=None, limit=None):
    if mode == 'hex':
        data = map(lambda b: format(ord(b), '02x'), data)
    else:
        data = map(ord, data)

    if limit is not None and len(data) > limit:
        fmt += ' ... (%d)'
        print(fmt % (data[:limit], len(data)))
    else:
        print(fmt % data)


class TcpEchoHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data) == 0:
                break
            p('%s', data)
            self.request.sendall(data)


class UdpEchoHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        conn = self.request[1]
        p('%s =>\n    %s', conn, data)
        conn.sendto(data, self.client_address)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


def start_tcp_server(addr):
    s = ThreadedTCPServer(addr, TcpEchoHandler)
    s.serve_forever()


def start_udp_server(addr):
    s = ThreadedUDPServer(addr, UdpEchoHandler)
    s.serve_forever()


def main(args):
    addr = (args['host'], args['port'])
    print("start echo server...")
    threads = [
        threading.Thread(target=start_tcp_server, args=(addr,)),
        threading.Thread(target=start_udp_server, args=(addr,)),
    ]

    for t in threads:
        t.setDaemon(True)
        t.start()
    while threading.active_count() > 0:
        time.sleep(1)


if __name__ == '__main__':
    desc = '''A simple TCP/UDP echo server.'''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--host', default='127.0.0.1',
                        help='host that echo server bind to')
    parser.add_argument('--port', type=int, default=9000,
                        help='port that echo server bind to')
    parser.add_argument('--print', action='store_true',
                        help='print out what received')
    args = vars(parser.parse_args())

    PRINT_OUT = args['print']
    p = functools.partial(pretty_print, mode='hex', limit=40)
    try:
        main(args)
    except KeyboardInterrupt:
        pass
