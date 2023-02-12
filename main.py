import sys
import time
from algo.path.reproduction.GA_Reproductioner import GA_Reproductioner
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
from elements.Charger import Charger
from algo.path.PSolver import PSolver
from algo.path.reproduction.MFEA_Reproductioner import MFEA_Reproductioner
from algo.ProblemSolver import ProblemSolver


# if len(sys.argv) == 1:
#     # print("main.py <input>")
#     # exit(0)
#     data = input("Data path: ")
# else:
#     data = sys.argv[1]
start=time.time()
data = r"./data/mfea_1000.txt"
k = 5
Configs.rand.seed(0)
Configs.U = 5
Configs.speed = 5
Configs.E_MC = 100000

ProblemManager.readInput(data,1.0)

for i in range(k):
    ProblemManager.chargers.append(Charger(Configs.E_MC, Configs.speed, Configs.Pm, Configs.U))

PSolver.reproductioner = MFEA_Reproductioner()
solution = ProblemSolver.solve()
solution.log()
print("total calculate time:",time.time()-start)
