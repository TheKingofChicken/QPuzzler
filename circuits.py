from abc import ABC
from qiskit import *

class Entity:
    def __init__(self, height, width, sprite, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.height = height
        self.width = width
        self.sprite = sprite

class QuantumGate(ABC):
    
    def __init__(self, cost, settings, current_Track):
        self.cost = cost
        self.settings = settings
        self.current_Track = current_Track
    
    @abs.abstractmethod
    def Qiskit_Equivalent_Dispatcher(self):
        pass

    @abs.abstractmethod
    def Qiskit_Equivalent(self):
        pass

    @abs.abstractmethod
    def Conditional_Qiskit_Equivalent():
        pass

    def Set_Current_Track(self,new_Track):
        self.current_Track = new_Track


class Track:
    def __init__(self, input):
        self.input = input
        self.gates = []
        self.total_Cost = 0
    
    def Add_Gate(self,new_Gate, position):
        self.gates.insert(new_Gate, position)
        self.total_Cost =+ new_Gate.cost

class Level:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.total_Cost = 0

    def Add_Track(self):
        self.inputs.append(Track(Quantum_Bit))

class Quantum_Bit:
    def __init__(self):
        self.state = [1,0,0,0]

    def Update(self, statevector):
        self.state = statevector

    def Get_State(self):
        return self.state
