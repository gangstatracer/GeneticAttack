# -*- coding: utf-8 -*-
import socket
from struct import *

from checksums import *
import Config


def getIpHeader(srcIp, dstIp, protocol):
    ihl = int(Config.ipMap['ihl'])
    version = int(Config.ipMap['version'])
    tos = int(Config.ipMap['tos'])
    id = int(Config.ipMap['id'])  # id пакета
    frag_off = int(Config.ipMap['frag_off'])
    ttl = int(Config.ipMap['ttl'])
    check = 0  # ядро само заполняет
    saddr = socket.inet_aton(srcIp)
    daddr = socket.inet_aton(dstIp)
    ihl_version = (version << 4) + ihl
    # ! в pack означает big endian формат
    return pack('!BBHHHBBH4s4s', ihl_version, tos, 0, id, frag_off, ttl, protocol, check, saddr, daddr)


def getTcpHeader(srcIp, dstIp, srcPort, dstPort):
    seq = int(Config.tcpMap['seq'])
    ack_seq = int(Config.tcpMap['ack_seq'])
    doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes
    # tcp flags
    fin = int(Config.tcpMap['fin'])
    syn = int(Config.tcpMap['syn'])
    rst = int(Config.tcpMap['rst'])
    psh = int(Config.tcpMap['psh'])
    ack = int(Config.tcpMap['ack'])
    urg = int(Config.tcpMap['urg'])
    window = socket.htons(int(Config.tcpMap['window']))  # maximum allowed window size
    check = 0
    urg_ptr = int(Config.tcpMap['urg_ptr'])

    offset_res = (doff << 4) + 0
    tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)

    # the ! in the pack format string means network order
    tcp_header = pack('!HHLLBBHHH', srcPort, dstPort, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)

    # pseudo header fields
    source_address = socket.inet_aton(srcIp)
    dest_address = socket.inet_aton(dstIp)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)

    psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    psh = psh + tcp_header

    # формируем tcp заголовок с правильной контрольной суммой
    return pack('!HHLLBBHHH', srcPort, dstPort, seq, ack_seq, offset_res, tcp_flags, window, tcp_checksum(psh), urg_ptr)


def getUdpHeader(srcPort, dstPort, data):
    length = 8 + len(data)  # 8=4+4 - по 4 байта на порт
    chcksum = 0  # необязательна для ipv4 оставляем нулями
    return pack('!HHHH', srcPort, dstPort, length, chcksum) + data


def getIcmpHeader(data):
    id = int(Config.icmpMap['id'])
    type = int(Config.icmpMap['type'])
    code = int(Config.icmpMap['code'])
    seq = int(Config.icmpMap['seq'])
    header = pack('bbHHh', type, code, 0, id, seq)
    # вычисляем чексумму с "пустым" заголовком
    my_checksum = icmp_checksum(header + data)
    # и формируем окончательный заголовок с контрольной суммой и данными
    header = pack('bbHHh', type, code, socket.htons(my_checksum), id, seq)
    return header + data
