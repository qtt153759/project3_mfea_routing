from pathlib import Path
import random
import sys

def createInput(sectorNumber:int)->None:
  Path("./data/").mkdir(parents=True, exist_ok=True)
  with open("./data/mfea_"+str(sectorNumber)+"_highP_1.txt", 'a+') as f:
    f.write("0 0\n")
    for i in range(800):
        x,y=1000,1000
        while pow(x,2)+pow(y,2)>=pow(1000,2):
          x=random.uniform(-1000,1000)
          y=random.uniform(-1000,1000)
        p=random.uniform(0.05,0.15)
        e0=random.uniform(5000,10800)
        sensorDetails=f"{x:.2f} {y:.2f} {p:.2f} {e0:2f}\n"
        f.write(sensorDetails)
    for i in range(160):
        x,y=1000,1000
        while pow(x,2)+pow(y,2)>=pow(1000,2):
          x=random.uniform(-1000,1000)
          y=random.uniform(-1000,1000)
        p=random.uniform(0.15,0.2)
        e0=random.uniform(5000,10800)
        sensorDetails=f"{x:.2f} {y:.2f} {p:.2f} {e0:2f}\n"
        f.write(sensorDetails)
    for i in range(40):
        x,y=1000,1000
        while pow(x,2)+pow(y,2)>=pow(1000,2):
          x=random.uniform(-1000,1000)
          y=random.uniform(-1000,1000)
        p=random.uniform(0.2,0.25)
        e0=random.uniform(5000,10800)
        sensorDetails=f"{x:.2f} {y:.2f} {p:.2f} {e0:2f}\n"
        f.write(sensorDetails)

if __name__ == "__main__":
    sectorNumber = sys.argv
    createInput(int(sectorNumber[1]))
    
    




