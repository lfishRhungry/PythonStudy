#!/usr/bin/env python
# coding:utf8
# -f 8001（通往内网） 8002（通往客户端） 端口转发模式 配置于反向代理时中继服务器
# -s -p 8001  正向代理模式 配置与中继服务器
# -s -r 1.1.1.1 -p 8001  反向代理模式 配置于内网服务器

import socket
import struct
import argparse
import sys
import threading
import select
import ssl

BUF_SIZE = 4096  # 数据读取缓冲区大小
FLAG = 0  # 连接标识符
CMD = "ok"  # 连接确认信息
DEBUG = False  # 异常状态
SSL = False  # ssl状态
CERT = None  # 认证状态


def remote(ipaddr, port, mode, c):
    """
    通过提供的连接请求信息 与需要连接的对象建立连接
    :param ipaddr: 请求IP地址
    :param port: 请求端口地址
    :param mode: 连接模式
    :param c: 请求者套接字对象
    :return: 与远端建立好连接的套接字
    """
    global FLAG
    global DEBUG
    try:
        # 开启套接字
        # AF_INET是服务器与服务器间网络通信   SOCK_STREAM是基于TCP的流式socket通信
        r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 可以设置开启套接字超时时间
        # r.settimeout(15)
        # 请求与请求者要求的IP地址和端口建立连接
        r.connect((ipaddr, port))
        #
        # 配置返回请求连接者的信息
        if mode == 1:  # 1代表TCP模式
            reply = b"\x05\x00\x00\x01"
            FLAG = 1
            if DEBUG:
                print("[*]Connect  success :", ipaddr, port)
        else:  # 否则不支持UDP模式
            reply = b"\x05\x07\x00\x01"
            FLAG = 0
        # 返回套接字地址（IP，port）
        local = r.getsockname()
        # 加入到返回
        reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
    # 异常处理
    except Exception as e:
        print(e)
        reply = b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00"
        FLAG = 0
        if DEBUG:
            print("[-]Connect  fail :", ipaddr, port)
    # 回复请求者
    c.send(reply)
    # 返回与请求者请求连接的远端服务器建立好连接的套接字
    return r


def exchange_data(sock, remoteSock):
    """
    socks5连接与客户端连接的数据交换
    :param sock: 请求方套接字
    :param remoteSock: 被请求者对象套接字
    :return:
    """
    global DEBUG
    try:
        inputs = [sock, remoteSock]
        while True:
            # select轮询两个套接字
            r, w, e = select.select(inputs, [], [])
            # 交换数据
            if sock in r:
                if remoteSock.send(sock.recv(BUF_SIZE)) <= 0:
                    # sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    # remote.shutdown(socket.SHUT_RDWR)
                    remoteSock.close()
                    break
            if remoteSock in r:
                if sock.send(remoteSock.recv(BUF_SIZE)) <= 0:
                    # sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    # remote.shutdown(socket.SHUT_RDWR)
                    remoteSock.close()
                    break
                if DEBUG:
                    # 打印还活着的线程个数
                    print("[*]Current active thread:", threading.activeCount())
                    print("[*]Forwarding data...")
    # 异常处理
    except Exception as e:
        if DEBUG:
            print(e)
        sock.send("socket error")
        # remote.shutdown(socket.SHUT_RDWR)
        remoteSock.close()
        # sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    # 键盘监听
    except KeyboardInterrupt:
        # remote.shutdown(socket.SHUT_RDWR)
        remoteSock.close()
        # sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit(1)


def local_socks5(port):
    """
    正向socks5代理模式
    :param port: 监听端口
    :return:
    """
    global BUF_SIZE
    global FLAG
    global DEBUG

    try:
        # 开启socket端口并监听
        # AF_INET是服务器与服务器间网络通信   SOCK_STREAM是基于TCP的流式socket通信
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port)) # 绑定本机所有IP地址
        s.listen(100)
        print("[*]Socks5 server start on 0.0.0.0:", port)
        while True:
            # 接受连接
            c, address = s.accept()
            # 之前没有建立连接 则可以建立并输出连接信息 连接标识符置1
            if not FLAG:
                print("[*]Client from :", address[0])
                FLAG = 1
            # 获取客户端想要访问地址以及的连接信息
            # 套接字读取缓冲区数据
            c.recv(BUF_SIZE)
            # 服务器回应本次采用的socks5版本和方法（不需要验证）
            c.send(b"\x05\x00")
            # 再次记录接收数据
            data = c.recv(BUF_SIZE)
            # 如果数据只有一个字符 重来
            if not data[1]:
                continue
            # 否则就拿到第二个字符（TCP/UDP模式标志）和第四个字符（地址类型）的unicode
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:  # 1代表IPv4
                # （通过解析字节流）从数据中拿到客户端IP地址和端口号
                addr = socket.inet_ntoa(data[4:8])
                port = (struct.unpack('!H', data[8:]))[0]
            elif addrtype == 3:  # 3代表是域名
                length = struct.unpack('B', data[4:5])[0]
                addr = data[5:5 + length]
                port = (struct.unpack('!H', data[5 + length:]))[0]
            # 传入客户端想要连接的IP地址 端口号 连接模式 套接字对象 建立连接 并通知请求者
            r = remote(addr, port, mode, c)
            # 连接成功 开启数据交换线程 交换请求者与被请求远端服务器的数据通信
            if FLAG:
                threading.Thread(target=exchange_data, args=(r, c)).start()
    # 异常处理
    except Exception as e:
        if DEBUG:
            print(e)
        # s.shutdown(socket.SHUT_RDWR)
        s.close()
        print("[-]Sockes5 server start fail...")
        sys.exit(1)
    # 键盘监听
    except KeyboardInterrupt:
        print("[-]Exit...")
        # s.shutdown(socket.SHUT_RDWR)
        s.close()
        sys.exit(1)


def reverse_socks5_main(daddr, dport):
    """
    反向socks5代理模式主函数
    在内网服务器上使用
    :param daddr: 中继IP地址
    :param dport: 中继端口号
    :return:
    """
    global BUF_SIZE
    global FLAG
    global CMD
    global DEBUG
    global SSL
    # global CERT
    try:
        # 开启用于传输cmd的套接字s1 用于确认是否可以传输数据
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 处理ssl认证
        if SSL:
            s1 = ssl.wrap_socket(s1,
                                 ssl_version=ssl.PROTOCOL_TLSv1_2,
                                 # cert_reqs=ssl.CERT_REQUIRED,
                                 # ca_certs=CERT
                                 )
            if DEBUG:
                print("[*]Cipher :", s1.cipher())
        # 请求与中继服务器建立连接
        s1.connect((daddr, dport))
        print("[*]Connected to relay server success:", daddr, dport)
        # 每当中继服务器发送一个表示可以连接的cmd时 开启一个新的socket来进行socks5代理
        while True:
            # 接收中继服务器的确认cmd 可以建立socks5连接
            flag = s1.recv(BUF_SIZE)
            # 如果确认可以连接
            if flag == CMD:
                # 进行socks5连接
                threading.Thread(target=reverse_socks5_hand,
                                 args=(daddr, dport)).start()
    # 异常处理
    except Exception as e:
        if DEBUG:
            print(e)
        print("[-]Connect  relay server fail...")
        # s1.shutdown(socket.SHUT_RDWR)
        s1.close()
        sys.exit(1)
    # 键盘监听
    except KeyboardInterrupt:
        print("[-]Exit...")
        # s1.shutdown(socket.SHUT_RDWR)
        s1.close()
        sys.exit(1)


def reverse_socks5_hand(daddr, dport):
    """
    socks5握手
    用于内网服务器与中继服务器通信
    :param daddr: 中继IP
    :param dport: 中继端口
    :return:
    """
    global DEBUG
    global SSL
    # global CERT
    try:
        # 新开启套接字s2 用于获取连接信息
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 配置ssl认证
        if SSL:
            s2 = ssl.wrap_socket(s2,
                                 ssl_version=ssl.PROTOCOL_TLSv1_2,
                                 # ca_certs=CERT,
                                 # cert_reqs=ssl.CERT_REQUIRED
                                 )
            if DEBUG:
                print("[*]Cipher :", s2.cipher())
        # 请求与中继服务器建立连接
        s2.connect((daddr, dport))
        if DEBUG:
            print("[*]New socket start...")
        #
        # 获取对方连接信息
        s2.recv(BUF_SIZE)
        s2.send(b"\x05\x00")
        data = s2.recv(BUF_SIZE)
        if data:
            mode = ord(data[1])  # 是否是TCP
            addrtype = ord(data[3])
            if addrtype == 1:  # 如果是IPv4
                addr = socket.inet_ntoa(data[4:8])
                port = (struct.unpack('!H', data[8:]))[0]
            elif addrtype == 3:  # 如果是域名
                length = struct.unpack('B', data[4:5])[0]
                addr = data[5:5 + length]
                port = (struct.unpack('!H', data[5 + length:]))[0]
            # 将解析出来的连接信息传入remote方法 得到建立好socks连接的socket
            r = remote(addr, port, mode, s2)  # forward requests
            exchange_data(s2, r)
        else:
            # s2.shutdown(socket.SHUT_RDWR)
            s2.close()
    except Exception as e:
        if DEBUG:
            print(e)
        # s2.shutdown(socket.SHUT_RDWR)
        s2.close()
    except KeyboardInterrupt:
        print("[-]Exit...")
        # s2.shutdown(socket.SHUT_RDWR)
        s2.close()
        sys.exit(1)


def forward_translate(s, c):
    """
    端口转发数据传输
    :param s: server套接字对象
    :param c: client套接字对象
    :return:
    """
    global BUF_SIZE
    global DEBUG
    try:
        # 套接字对象列表
        conlist = [c, s]
        while True:
            # select轮询
            r, w, e = select.select(conlist, [], [])
            # 如果client套接字可读
            if c in r:
                # 将client套接字接收到的信息转发给server 没有信息就关闭套接字并中断
                if s.send(c.recv(BUF_SIZE)) <= 0:
                    # c.shutdown(socket.SHUT_RDWR)
                    c.close()
                    # s.shutdown(socket.SHUT_RDWR)
                    s.close()
                    break
            # 如果server套接字可读
            if s in r:
                # 将server套接字接收到的信息转发给client 没有信息就关闭套接字并中断
                if c.send(s.recv(BUF_SIZE)) <= 0:
                    # s.shutdown(socket.SHUT_RDWR)
                    s.close()
                    # c.shutdown(socket.SHUT_RDWR)
                    c.close()
                    break
                if DEBUG:
                    # 返回还活着的线程个数
                    print("[*]Current active thread:", threading.activeCount())
                    print("[*]Forwarding data...")
    # 异常处理
    except Exception as e:
        if DEBUG:
            print(e)
        # s.shutdown(socket.SHUT_RDWR)
        s.close()
        # c.shutdown(socket.SHUT_RDWR)
        c.close()
    # 键盘监听
    except KeyboardInterrupt:
        print("[-]Exit...")
        # s.shutdown(socket.SHUT_RDWR)
        s.close()
        # c.shutdown(socket.SHUT_RDWR)
        c.close()
        sys.exit(1)


def forward_main(ports):
    """
    端口转发模式
    :param ports: 通往内网服务器端口port1 客户端端口port2
    :return:
    """
    global BUF_SIZE
    global CMD
    global DEBUG
    global SSL
    global CERT

    # 开启socket并尝试监听端口port1（server）
    try:
        # AF_INET是服务器与服务器间网络通信   SOCK_STREAM是基于TCP的流式socket通信
        sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_s.bind(("0.0.0.0", ports[0]))
        sock_s.listen(100)
        print("[*]Listen on 0.0.0.0:", ports[0])
    # 打开端口失败则返回错误并退出
    except Exception as e:
        print("[-]port %s has been used or permission denied!" % ports[0])
        if DEBUG:
            print(e)
        sys.exit(1)

    # 尝试监听端口port2（client）
    try:
        sock_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # port 2
        sock_c.bind(("0.0.0.0", ports[1]))
        sock_c.listen(100)
        print("[*]Listen on 0.0.0.0:", ports[1])
    # 打开端口失败则返回异常并退出
    except Exception as e:
        print("[-]port %s has been used or permission denied!" % ports[1])
        if DEBUG:
            print(e)
        sys.exit(1)
    try:
        # 拿到两个端口的套接字对象  sock_s是发送CMD（ok）的那一个端口
        inputs = [sock_s, sock_c]
        con_cmd = None  # cmd端口连接状态记为关闭
        first_con = 1  # 第一客户端连接状态记为开启
        # 异步IO模式 疯狂的用select轮询
        while True:
            # 返回可读的socket
            rs, ws, es = select.select(inputs, [], [])
            # 如果服务器端口准备好读取了
            if sock_s in rs:
                # 且cmd端处于未连接状态
                if not con_cmd:
                    # 接受与服务器socket连接 返回已建立连接的socket和地址
                    con_s, address1 = sock_s.accept()
                    # 当开启了ssl 配置ssl认证
                    if SSL:
                        # keyfile 和 certfile 指定文件 server_side 指定是 server side 还是 client side
                        con_s = ssl.wrap_socket(con_s,
                                                server_side=True,
                                                certfile=CERT,
                                                keyfile=CERT,
                                                ssl_version=ssl.PROTOCOL_TLSv1_2
                                                )
                        # ssl建立异常时 返回错误信息
                        if DEBUG:
                            print("[*]Cipher :", con_s.cipher())
                    print("[*]Client from :" + str(address1[0]) + " :" + str(address1[1]) + " on Port " + str(
                        ports[0]))
                    # 记录cmd端口连接状态
                    con_cmd = con_s

            # 如果客户端端口准备好连接了
            if sock_c in rs:
                # 接受socket连接 返回建立好连接的socket和地址
                con_c, address2 = sock_c.accept()
                # 异常处理
                if DEBUG:
                    print("[*]Client from :" + str(address2[0]) + " :" + str(address2[1]) + " on Port " + str(
                        ports[1]))
                else:
                    # 如果第一个服务端已建立连接 输出客户端连接信息与端口号
                    if first_con:
                        print("[*]Client from :" + str(address2[0]) + " :" + str(address2[1]) + " on Port " + str(
                            ports[1]))
                        first_con = 0  # 再次置零 保证下一次循环正常运行
                # 在与内网服务器端连接后 向它发送ok表示可以建立socks5通信
                if con_cmd:
                    con_s.send(CMD)
                    # 接受用于数据传输的隧道socket 返回连接套接字和地址
                    con_s_tun, con_s_tun_addr = sock_s.accept()
                    # 配置ssl认证信息
                    if SSL:
                        con_s_tun = ssl.wrap_socket(con_s_tun,
                                                    server_side=True,
                                                    certfile=CERT,
                                                    keyfile=CERT,
                                                    ssl_version=ssl.PROTOCOL_TLSv1_2
                                                    )
                        # 错误处理
                        if DEBUG:
                            print("[*]Cipher :", con_s_tun.cipher())
                    # 开启端口转发数据传输的线程
                    threading.Thread(target=forward_translate,
                                     args=(con_s_tun, con_c)).start()
    # 键盘监听处理
    except KeyboardInterrupt:
        # 当使用了exit键则关闭两个套接字并退出
        print("[-]Exit...")
        # sock_s.shutdown(socket.SHUT_RDWR)
        sock_s.close()
        # sock_c.shutdown(socket.SHUT_RDWR)
        sock_c.close()
        sys.exit(1)
    # 异常处理
    except Exception as e:
        if DEBUG:
            print(e)
        # sock_s.shutdown(socket.SHUT_RDWR)
        sock_s.close()
        # sock_c.shutdown(socket.SHUT_RDWR)
        sock_c.close()


def main():
    """
    主函数 命令行解析
    :return:
    """
    global DEBUG
    global SSL
    global CERT
    # 配置命令行传参方式
    parser = argparse.ArgumentParser(prog='socks5proxy',
                                     description='socks5proxy',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     usage='''%(prog)s [options]
                                            tsocks -s -p 1028		Socks5 server mode
                                            tsocks -s -r 1.1.1.1 -p 8001	Reverse socks5 server mode (internal)
                                            tsocks -f 8001 8002		Port forward mode (delay)
                                            tsocks -s -S -r 1.1.1.1 -p 443	Reverse socks5  over ssl
                                            tsocks -f 443 8002 -S -c cert.pem    Port forward over ssl
                                            -----------------------------------------------------------------------
                                            generate cert:
                                            openssl req -new -x509 -keyout cert.pem -out cert.pem -days 1095 -nodes''',
                                     )
    # 命令行参数对应操作
    # -s socks5服务器模式
    parser.add_argument('-s', '--server', action="store_true",
                        default=False, help='Socks5 server mode')
    # -p/-port socks5服务器监听端口
    parser.add_argument('-p', '--port', metavar="PORT", dest='port', type=int,
                        default=1080, help='Socks5 server mode listen port or remote port')
    # -r/-remove 反向socks5模式 设置中继IP地址
    parser.add_argument('-r', '--remote', metavar="REMOTE_IP", type=str,
                        default=None, help='Reverse socks5 server mode ,set remote relay IP')
    # -f/--forward 设置端口转发模式下的内网服务器连接端口port_1和客户端连接端口_2
    parser.add_argument('-f', '--forward', nargs=2, metavar=('PORT_1', 'PORT_2'),
                        type=int, help='Set forward mode,server connect port_1,client connect port_2')
    # -d/--debug 开启时为调试模式 显示调试信息
    parser.add_argument('-d', '--debug', action="store_true",
                        default=False, help='Set debug mode,will show debug information')
    # -S/--ssl 使用sll 只支持反向代理模式 中继服务器必须也使用ssl
    parser.add_argument('-S', '--ssl', action="store_true", default=False,
                        help='Set use ssl,just support reverse proxy mode,relay server must also use ssl')
    # -c/--cert 设置ssl认证文件路径 只在中继服务器中配置
    parser.add_argument('-c', '--cert', metavar='CERT_FILE', type=str,
                        default="cert.pem", help='Set ssl cert file path,only set relay server')
    # 获得解析参数对象
    args = parser.parse_args()
    # 将获取用户设置的相应参数传递
    DEBUG = args.debug
    SSL = args.ssl
    CERT = args.cert

    # 当传递参数长度不合法时 退出程序
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    # 当用户同时设置了端口转发模式和socks5代理模式的参数时 给出提醒并退出
    if args.server and args.forward:
        print("[-]Socks5 or forward mode only one...")
        sys.exit(1)
    # 当用户同时配置了ssl参数和端口转发参数时
    if args.ssl and args.forward:
        # 检查ssl认证文件路径
        try:
            f_1 = open(args.cert)
            f_1.close()
        # 没有ssl认证文件则给出提示并退出
        except Exception as e:
            if DEBUG:
                print(e)
            print("[-]Cert file not exist or error...")
            sys.exit(1)

    # 当用户配置了socks5服务器模式
    if args.server:
        # 如果设置了中继IP地址 是反向代理模式时（内网服务器端使用）
        if args.remote:
            while True:
                # 将中继IP地址及中继端口传入反向socks5代理主函数
                reverse_socks5_main(args.remote, args.port)
        # 否则就socks5代理服务器模式
        else:
            while True:
                # 将socks5服务器监听端口
                local_socks5(args.port)
    # 如果使用了端口转发模式
    if args.forward:
        while True:
            # 将端口port1（server） port2（client）信息参数传入
            forward_main(args.forward)


if __name__ == '__main__':
    main()
