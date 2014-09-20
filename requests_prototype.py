import time, requests, pyping
from threading import Thread


def stopwatch(func):
    def measured(arg):
        start_time = time.time()
        func(arg)
        return time.time() - start_time

    return measured


@stopwatch
def download_url(url):
    r = requests.get(url)


def ping_avg(destination):
    r = pyping.ping(destination)
    return r.avg_rtt


print download_url('http://www.google.ru')
print ping_avg('192.168.0.1')


class Chromosome:
    def attack(self):
        print "Test successful!"


def eval_func(chromosome):
    score = 0.0
    attack = Thread(target=chromosome.attack)
    attack.start()
    time.sleep(1)
    score = download_url('http://www.google.ru')
    ping = ping_avg('192.168.0.1')
    if ping is None:
        ping = 10000
    score += ping
    attack.join()
    return score


chr = Chromosome()
print eval_func(chr)
	


	
