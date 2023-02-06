from elements.Sensor import Sensor
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
import math

class NetworkDivider:
    @staticmethod
    def cluster(sectorsNo: int, sensors: 'list[Sensor]') -> 'list[list[Sensor]]':
        phi = 2.0 * math.pi / (1.0 * sectorsNo) #the angle in radian of each sector (our working space is a circle centered by service station)
        #Please pay attention that a sector can be empty and this code does not handle that situation

        result: 'list[list[Sensor]]'
        result = []
        for k in range(sectorsNo):
            result.append([])
            for s in sensors:
                #first vector (ox): (1,0)
                firstvector = (1,0)

                #calculate second vector
                secondvector = (s.x-ProblemManager.serviceStation.x, s.y-ProblemManager.serviceStation.y)

                #calculate the angle between 2 vectors using dot product
                #dot product
                dotProduct = firstvector[0] * secondvector[0] + firstvector[1] * secondvector[1]
                #calculate length product
                lengthProduct = math.sqrt(pow(firstvector[0],2)+pow(firstvector[1],2)) * math.sqrt(pow(secondvector[0],2)+pow(secondvector[1],2))
                cosphi = dotProduct / lengthProduct
                angle = math.acos(cosphi)
                if secondvector[1] < 0:
                    angle = 2*math.pi - angle

                #if it belong to this sector then add it 
                if angle > k * phi and angle < (k + 1) * phi:
                    result[k].append(s)
                
        return result