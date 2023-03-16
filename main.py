import sys
import time
from algo.path.reproduction.GA_Reproductioner import GA_Reproductioner
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
from elements.Charger import Charger
from algo.path.PSolver import PSolver
from algo.path.reproduction.MFEA_Reproductioner import MFEA_Reproductioner
from algo.ProblemSolver import ProblemSolver

#this part is for recursive call

if len(sys.argv) == 2:
    count = int(sys.argv[1])
else:
    #manual input here
    # data = r"./data/mfea_1000.txt"
    count = 0




#output current network state to file
outputPath = r"./output"
#get a name for our output
fileName = f"/{count}.txt"
result = f"/survivability.txt"



start=time.time()

k = 20
Configs.rand.seed(0)
Configs.U = 5
Configs.speed = 5
Configs.E_MC = 108000
Configs.networkSurvivabilityFitness=0.8 #1,0.75,0.5,0.25,0
Configs.totalTimeRatioFitness=0.2       #0,0.25,0.5,0.75,1
Configs.mode="default" #[default,two_opt,three_opt]


#read input from file
ProblemManager.readInput(outputPath+fileName,1.0)

#update new output file
count = count + 1
fileName = f"/{count}.txt"

for i in range(k):
    ProblemManager.chargers.append(Charger(Configs.DEFAULT_EMC, Configs.speed, Configs.Pm, Configs.U))

PSolver.reproductioner = MFEA_Reproductioner()
solution = ProblemSolver.solve()

#log output to file
solution.log(outputPath+fileName)

f = open(outputPath+result, 'a')
if count==1: 
    f.write("\n***************************************************************************\n")
    f.write(f"k={k}, fitness ratio = ({Configs.networkSurvivabilityFitness},{Configs.totalTimeRatioFitness}) => Total survie over 1000:\n" )
f.write(f"{ProblemManager.networkSurvivabilityOverThousand}, ")
f.close()
print("total calculate time:",time.time()-start)

    

