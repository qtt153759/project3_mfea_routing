import sys
from multipledispatch import dispatch
from algo.path.PIndividual import PIndividual
from problem.ProblemManager import ProblemManager
from problem.Configs import Configs

class Solution:
    """Description here"""

    path: 'list[list[int]]'
    """n/a"""

    time: 'list[list[float]]'
    """n/a"""

    @dispatch(list, list)
    def __init__(self, path: 'list[list[int]]', time: 'list[list[float]]') -> None:  # type: ignore
        self.path = path
        self.time = time
    
    @dispatch(list)
    def __init__(self, indivs: 'list[PIndividual]') -> None:
        V = len(ProblemManager.chargers)
        self.path = []
        self.time = []
        for i in range(V):
            self.path.append([])
            self.time.append([])

        for a in range(V):
            tour: 'list[int]'
            tour = indivs[a].path
            for i in range(len(tour)):
                self.path[a].append(tour[i])
                self.time[a].append(indivs[a].chargingTime[i])


    def extractSolution(self) -> 'dict[str, float]':
        V = len(self.path)
        totalDead = 0
        sumEAfterT = 0
        minLifetime = sys.float_info.max
        totalLifetime = 0.0
        a = 0
        for a in range(V):
            ch = ProblemManager.chargers[a]
            leng = len(self.path[a])
            
            #double arriveTime[] = new double[leng]
            arriveTime: 'list[float]'
            arriveTime = [0.0] * leng

            #boolean[] visited = new boolean[ProblemManager.maxSensorId + 1]
            visited: 'list[bool]'
            visited = [False] * (ProblemManager.maxSensorId + 1)

            dead = 0
            sumE = 0.0

            arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.getId()][self.path[a][0]] / Configs.speed
            for i in range(leng):
                visited[self.path[a][i]] = True
                s = ProblemManager.getSensorById(self.path[a][i])
                eRemain = s.E0 - arriveTime[i] * s.p
                eAfterT = s.E0 - Configs.T * s.p + self.time[a][i] * ch.U
                if eRemain < s.Emin or eAfterT < s.Emin:
                    dead += 1
                else:
                    sumE += eAfterT
                    t = (eAfterT - s.Emin) / s.p
                    if t < minLifetime:
                        minLifetime = t
                
                lifetime = (s.E0 + self.time[a][i] * ch.U - s.Emin) / s.p
                totalLifetime += lifetime

                if i < (leng - 1):
                    arriveTime[i + 1] = arriveTime[i] \
                        + ProblemManager.distance[self.path[a][i]][self.path[a][i + 1]] / ch.speed + self.time[a][i]

            for s in ProblemManager.subNet[a]:
                if not visited[s.id]:
                    eAfterT = s.E0 - Configs.T * s.p
                    if eAfterT < Configs.S_EMIN:
                        dead += 1
                    else:
                        sumE += eAfterT
                        t  = eAfterT / s.p
                        minLifetime = t if t < minLifetime else minLifetime
                    totalLifetime += s.getLifetime()
            totalDead += dead
            sumEAfterT += sumE

        networkSurvivability = 100 * (ProblemManager.initSensors - totalDead) / (1.0 * ProblemManager.initSensors)
        avgE = sumEAfterT / (1.0 * ProblemManager.initSensors)
        avgDeadDuration = totalLifetime / (1.0 * ProblemManager.initSensors)
        emove = 0.0
        
        for a in range(V):
            emove += ProblemManager.chargers[a].getEmove(self.path[a])
        
        result = {}
        result["network_survivability"] = networkSurvivability
        result["network_lifetime"] = minLifetime + Configs.T
        result["average_energy"] = avgE
        result["moving_cost"] = emove
        result["average_lifetime"] = avgDeadDuration
        return result


    def log(self, outputFileName: str) -> None:
        f = open(outputFileName,"w")
        firstLine = f"{ProblemManager.serviceStation.x} {ProblemManager.serviceStation.y}\n"
        f.write(firstLine)

        V = len(self.path)
        print(f"Number of charging vehicles: {V}")
        print(f"Survey time: {Configs.T}")

        print("Network clustering infor: ")

        for i in range(ProblemManager.getTaskNumber()):
            print(f"Cluster {i}:")
            l = []
            for kk in ProblemManager.subNet[i]:
                l.append(kk.id)
            print(l)

        totalDead = 0
        totalLifetime = 0

        for a in range(V):
            ch = ProblemManager.chargers[a]
            leng = len(self.path[a])
            
            #double arriveTime[] = new double[leng]
            arriveTime = [0.0] * leng
            
            #boolean[] visited = new boolean[ProblemManager.maxSensorId + 1]
            visited = [False] * (ProblemManager.maxSensorId + 1)
            dead = 0

            print(f"Vehicle {a}")
            print("Charging tour: ")
            
            for i in range(leng):
                print(f"{self.path[a][i]} ", end =" -> ")
                visited[self.path[a][i]] = True
            print("")

            sum = 0.0
            print(f"Charging time: ")
            for i in range(leng):
                print(f"{self.time[a][i]} ", end =" + ")
                sum += self.time[a][i]

            print("")

            print(f"Traveling energy: {ch.getEmove(self.path[a])}")
            print(f"Charging energy: {sum * ch.U}")
            print(f"Total energy used: {ch.getEmove(self.path[a]) + sum * ch.U}")
            print(f"Charging round duration: {ch.getEmove(self.path[a]) / ch.Pm + sum}")

            print("ID | p | E0 | time_arrive | E_remain | time_charge | energy_charge| E_after_charge | E_after_cycle")
            arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.getId()][self.path[a][0]] / Configs.speed
            for i in range(leng):
                s = ProblemManager.getSensorById(self.path[a][i])
                eRemain = s.E0 - arriveTime[i] * s.p
                eAfterCharged = eRemain + self.time[a][i] * (ch.U - s.p)
                eAfterT = s.E0 - Configs.T * s.p + self.time[a][i] * ch.U

                sensorDetails = f"{s.id} | {s.p:.2f} | {s.E0:.2f} | {arriveTime[i]:.2f} | {eRemain:.2f} | {self.time[a][i]:.2f} | {(self.time[a][i]*ch.U):.2f} | {eAfterCharged:.2f} | {eAfterT:.2f}"
                f.write(f"{s.x} {s.y} {s.p} {max(eAfterT,s.Emin)}\n")
                if (eRemain < s.Emin or eAfterT < s.Emin):
                    prRed(sensorDetails)
                    dead+=1
                else:
                    print(sensorDetails)
                

                lifetime = (s.E0 + self.time[a][i] * ch.U - s.Emin) / s.p
                totalLifetime += lifetime

                if (i < leng - 1):
                    arriveTime[i + 1] = arriveTime[i] \
                            + ProblemManager.distance[self.path[a][i]][self.path[a][i + 1]] / ch.speed + self.time[a][i]



            for s in ProblemManager.subNet[a]:
                if (not visited[s.getId()]):
                    eAfterT = s.E0 - Configs.T * s.p
                    sensorDetails = f"{s.id} | {s.p:.2f} | {s.E0:.2f} | {eAfterT:.2f}"
                    f.write(f"{s.x} {s.y} {s.p} {max(eAfterT,s.Emin)}\n")
                    if (eAfterT < Configs.S_EMIN):
                        prRed(sensorDetails)
                        dead+=1
                    else:
                        print(sensorDetails)

                    totalLifetime += s.getLifetime()

            totalDead += dead

        networkSurvivability = 100 * (ProblemManager.initSensors - totalDead) / (1.0 * ProblemManager.initSensors)

        emove = 0
        for a in range(V):
            emove += ProblemManager.chargers[a].getEmove(self.path[a])
        

        print(f"Network survivability: {networkSurvivability}%")
        ProblemManager.networkSurvivability = networkSurvivability

        networkSurvivabilityOverThousand=100 * (ProblemManager.initSensors - totalDead) /1000
        print(f"networkSurvivabilityOverThousand: {networkSurvivabilityOverThousand}%")
        ProblemManager.networkSurvivabilityOverThousand = networkSurvivabilityOverThousand

        print(f"Average dead duration: {totalLifetime / (1.0 * ProblemManager.initSensors)}")
        print(f"Traveling energy: {emove}")
        f.close()

    
def prRed(skk): print("\033[91m{}\033[00m" .format(skk))




