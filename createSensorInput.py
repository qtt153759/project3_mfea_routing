from pathlib import Path
import random
import sys

def createInput(sectorNumber:int)->None:
  Path("./data/").mkdir(parents=True, exist_ok=True)
  with open("./data/mfea_"+str(sectorNumber)+".txt", 'a+') as f:
    f.write("0 0\n")
    for i in range(sectorNumber):
        x=random.uniform(-1000,1000)
        y=random.uniform(-1000,1000)
        p=random.uniform(0.05,0.3)
        e0=random.uniform(5000,10800)
        sensorDetails=f"{x:.2f} {y:.2f} {p:.2f} {e0:2f}\n"
        f.write(sensorDetails)

if __name__ == "__main__":
    sectorNumber = sys.argv
    createInput(int(sectorNumber[1]))




