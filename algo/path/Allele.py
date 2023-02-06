from multipledispatch import dispatch

class Allele:

    value: float

    sensorId: int

    def __init__(self, value: float, sensorId: int) -> None:
        self.value = value
        self.sensorId = sensorId
    
    def __gt__(self, __o: 'Allele') -> bool:
        if self.value > __o.value:
            return True
        else:
            return False

    def __eq__(self, __o: 'Allele') -> bool:
        if self.value == __o.value:
            return True
        else:
            return False

    def __lt__(self, __o: 'Allele') -> bool:
        if self.value < __o.value:
            return True
        else:
            return False