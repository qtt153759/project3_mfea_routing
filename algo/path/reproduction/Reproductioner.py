from algo.path.PPopulation import PPopulation
from algo.path.PIndividual import PIndividual
from abc import ABC, abstractmethod

class Reproductioner(ABC):
    @abstractmethod
    def reproduction(self, pop: PPopulation) -> 'list[PIndividual]':
        pass