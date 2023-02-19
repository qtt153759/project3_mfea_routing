from algo.path.PSolver import PSolver
from elements.Sensor import Sensor
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
from problem.Solution import Solution
from algo.NetworkDivider import NetworkDivider
from cycler import cycler
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
class ProblemSolver:

    @staticmethod
    def solve() -> Solution:
        clusters: 'list[list[Sensor]]'
        clusters = NetworkDivider.cluster(ProblemManager.getTaskNumber(), ProblemManager.sensors)



        ussd = 0
        for cluster in clusters:
            if ussd < len(cluster):
                ussd = len(cluster)

        ProblemManager.subNet = clusters
        ProblemManager.USSD = ussd

        n = ProblemManager.initSensors / Configs.DEFAULT_MCS

        d = math.sqrt(2.0 / ProblemManager.getSensorDensity())

        #estimation of the charging cirle T
        Configs.T = (Configs.DEFAULT_EMC - Configs.Pm * d *  n / Configs.DEFAULT_SPEED) / Configs.DEFAULT_U \
                + n * d / Configs.DEFAULT_SPEED
        Configs.P_POP_SIZE = ProblemManager.getTaskNumber() * Configs.P_POP_SIZE_PER_TASK
    #		System.out.println(Configs.T);
        energyConsumePerT=0
        for sensor in ProblemManager.sensors:
            energyConsumePerT+=sensor.p*Configs.T
        conditionChargerForInfinitive=energyConsumePerT/Configs.DEFAULT_EMC
        print("condition",conditionChargerForInfinitive)
        #Test drawing
        # figure, axes = plt.subplots()
        # Drawing_uncolored_circle = plt.Circle( (ProblemManager.serviceStation.x, ProblemManager.serviceStation.y ), Configs.R , fill = False )
        # plt.xlim([ProblemManager.serviceStation.x - Configs.R*1.05, ProblemManager.serviceStation.x + Configs.R*1.05])
        # plt.ylim([ProblemManager.serviceStation.x - Configs.R*1.05, ProblemManager.serviceStation.x + Configs.R*1.05])
        # for index, subnet in enumerate(ProblemManager.subNet):
        #     # color = ['b','g','r','c','m','y','k']
        #     color = cm.rainbow(np.linspace(0, 1, len(ProblemManager.subNet)))

        #     for node in subnet:
        #         axes.scatter(node.x, node.y, s=1,c=color[index%len(color)])
        #         #plt.plot(node.x, node.y, "go")

        #     phi = 2*math.pi / len(ProblemManager.subNet)
        #     # for i in range(len(ProblemManager.subNet)):
        #     #     axes.plot([ProblemManager.serviceStation.x+Configs.R*math.cos(phi*i), \
        #     #                ProblemManager.serviceStation.x],\
        #     #               [ProblemManager.serviceStation.y+Configs.R*math.sin(phi*i),\
        #     #                ProblemManager.serviceStation.y], c='#000000')


        #     axes.spines['left'].set_position('center')
        #     axes.spines['bottom'].set_position('center')
        #     axes.spines['right'].set_color('none')
        #     axes.spines['top'].set_color('none')
        #     axes.xaxis.set_ticks_position('bottom')
        #     axes.yaxis.set_ticks_position('left')
        #     axes.set_aspect( 1 )
        #     axes.add_artist( Drawing_uncolored_circle )
        #     plt.title( 'Circle' )
        # plt.show()




        solution = PSolver.solve()
    # //		
    # //		TIndividual.setPath(solution.getPath());
    # //		TIndividual.setGreedyChargingTime(solution.getTime());
    # //		solution.setTime(TSolver.solve());
    # //		
        return solution
