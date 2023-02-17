from random import Random

class Configs:
    rand = Random()
    T: float

    #charging speed
    U = float()
    speed = float()
    E_MC = float()
    S_EMAX = 10800
    S_EMIN = 540
    R = 1000
    Pm = 1
    DEFAULT_U = 5
    DEFAULT_SPEED = 5
    DEFAULT_EMC = 108000
    DEFAULT_MCS = 5
    P_POP_SIZE_PER_TASK = 100
    P_POP_SIZE = int()
    P_GENERATIONS = 50
    RMP = 0.3
    NC = 15
    NM = 15