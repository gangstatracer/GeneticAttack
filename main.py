from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import DBAdapters
import pyevolve
from genetic_algorithm import *
from Config import *

reload_conf()
pyevolve.logEnable()
genome = AttackGenome('192.168.0.1')
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(20)
ga.setPopulationSize(20)
ga.terminationCriteria.set(GSimpleGA.RawStatsCriteria)
csv_adapter = DBAdapters.DBFileCSV(identify="run2", filename="stats.csv")
ga.setDBAdapter(csv_adapter)
ga.evolve(freq_stats=1)
print ga.bestIndividual()