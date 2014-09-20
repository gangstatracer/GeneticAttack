# -*- coding: utf-8 -*-

from headers import *


def getSocket():
    # создаем raw socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        # z = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        # # говорим ядру, не добавлять заголовки, т.к. мы сами включаем заголовки
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        return s
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        exit()


def getTcpSynPacket(**kwargs):
    srcIp = kwargs.get('srcIp')
    dstIp = kwargs.get('dstIp')
    srcPort = kwargs.get('srcPort')
    dstPort = kwargs.get('dstPort')
    ip_header = getIpHeader(srcIp, dstIp, socket.IPPROTO_TCP)
    tcp_header = getTcpHeader(srcIp, dstIp, srcPort, dstPort)
    return ip_header + tcp_header


def getUdpPacket(**kwargs):
    srcIp = kwargs.get('srcIp')
    dstIp = kwargs.get('dstIp')
    srcPort = kwargs.get('srcPort')
    dstPort = kwargs.get('dstPort')
    data = kwargs.get('data')
    ip_header = getIpHeader(srcIp, dstIp, socket.IPPROTO_UDP)
    udp_header = getUdpHeader(srcPort, dstPort, data)
    return ip_header + udp_header


def getIcmpPacket(**kwargs):
    srcIp = kwargs.get('srcIp')
    dstIp = kwargs.get('dstIp')
    data = kwargs.get('data')
    ip_header = getIpHeader(srcIp, dstIp, socket.IPPROTO_ICMP)
    icmp_header = getIcmpHeader(data)
    return ip_header + icmp_header
