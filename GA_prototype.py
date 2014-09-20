from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import DBAdapters
import pyevolve

def eval_func(chromosome):
   score = 0.0
   for value in chromosome:
      if value==0:
         score += 1   
   return score

pyevolve.logEnable()
genome = G1DList.G1DList(50)
genome.setParams(rangemin=0, rangemax=10)
genome.evaluator.set(eval_func)
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(500)
ga.setPopulationSize(10)
ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
csv_adapter = DBAdapters.DBFileCSV(identify="run1", filename="statsfyuk.csv")
ga.setDBAdapter(csv_adapter)
ga.evolve(freq_stats=20)
print ga.bestIndividual()