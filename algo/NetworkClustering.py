from elements.Sensor import Sensor
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
import math

class Centroid:
    DIFF = 1E-3

    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def getDistance(self, x: float, y: float) -> float: 
        return math.sqrt((self.x - x) * (self.x - x) + (self.y - y) * (self.y - y))

    def isDifference(self, c: 'Centroid') -> bool:
        return self.getDistance(c.x, c.y) > self.DIFF


class NetworkClustering:

    #private static final double MIN_X = 0;
    MIN_X: float
    MIN_X = 0.0

    #private static final double MAX_X = 1000;
    MAX_X: float
    MAX_X = 1000

    #private static final double MIN_Y = 0;
    MIN_Y: float
    MIN_Y = 1000.0

    #private static final double MAX_Y = 1000;
    MAX_Y: float
    MAX_Y = 1000.0

    #private static final double MAX_ITERATIONS = 1000;
    MAX_ITERATIONS: float
    MAX_ITERATIONS = 1000.0

    @staticmethod
    def generateRandomCentroids(k: int) -> 'list[Centroid]':
        centroids: list[Centroid]
        centroids = []
        while (len(centroids) < k):
            c = Centroid(Configs.rand.uniform(0,1) * (NetworkClustering.MAX_X - NetworkClustering.MIN_X) + NetworkClustering.MIN_X, Configs.rand.uniform(0,1) * (NetworkClustering.MAX_Y - NetworkClustering.MIN_Y) + NetworkClustering.MIN_Y)
            centroids.append(c)
        
        return centroids

    @staticmethod
    def getNearestCentroid(p: Sensor, centroids: 'list[Centroid]') -> Centroid:
        minDis = centroids[0].getDistance(p.x, p.y)
        index = 0
        for i in range(1, len(centroids)):
            c = centroids[i]
            dis = c.getDistance(p.x, p.y)
            if (dis < minDis):
                minDis = dis
                index = i

        return centroids[index]

    @staticmethod
    def assignToCluster(p: Sensor, centroid: Centroid,  clusters: 'dict[Centroid, list[Sensor]]'):
        if (clusters.get(centroid) == None):
            clusters[centroid] = []

        clusters[centroid].append(p)

    @staticmethod
    def getCentroid(points: 'list[Sensor]') -> Centroid:
        xmean = 0.0
        ymean = 0.0
        for s in points:
            xmean += s.x
            ymean += s.y
        return Centroid(xmean / len(points), ymean / len(points))

    @staticmethod
    def relocateCentroids(centroids: 'list[Centroid]', \
            clusters: 'dict[Centroid, list[Sensor]]') -> 'list[Centroid]':
        newCentroids: 'list[Centroid]'
        newCentroids = []
        for c in centroids:
            newCentroids.append(NetworkClustering.getCentroid(clusters[c]))
        return newCentroids

    @staticmethod
    def checkTermination(oldCentroids: 'list[Centroid]', newCentroids: 'list[Centroid]') -> bool:
        for i in range(len(oldCentroids)):
            old = oldCentroids[i]
            newCen = newCentroids[i]
            if (old.isDifference(newCen)):
                return False
        return True

    #@SuppressWarnings({ "unchecked", "rawtypes" })
    @staticmethod
    def cluster(k: int, sensors: 'list[Sensor]') -> 'list[list[Sensor]]':
        clusters: 'dict[Centroid, list[Sensor]]'
        clusters = {}
        points: 'list[Sensor]'
        points = []
        points += ProblemManager.sensors

        centroids = NetworkClustering.generateRandomCentroids(k)
        oldCentroids : 'list[Centroid]'
        oldCentroids = []

        iter = 0
        while True :
            clusters = {}
            for p in points:
                centroid = NetworkClustering.getNearestCentroid(p, centroids)
                NetworkClustering.assignToCluster(p, centroid, clusters)
            

            oldCentroids.clear()
            oldCentroids += centroids

            centroids = NetworkClustering.relocateCentroids(centroids, clusters)
            iter += 1
            if (iter > NetworkClustering.MAX_ITERATIONS or NetworkClustering.checkTermination(oldCentroids, centroids)):
                break
            print("ok")

        result: 'list[list[Sensor]]'
        result = []
        for i in range(k):
            result.append([])
            #bug prone
            result[i] += clusters.get(oldCentroids[i]) #type: ignore

        return result
