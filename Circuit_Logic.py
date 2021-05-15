import numpy as np
import qiskit as qs
import math
import pygame as pg
import copy

class Quantum_Gate():
        
    def __init__(self, cost, conditional, current_Track, current_Position, rectangle = None):
        self.cost = cost
        self.conditional = conditional
        self.current_Track = current_Track
        self.current_Position = current_Position
        if rectangle is None:
            self.rectangle = pg.Rect(0, 0, 100, 100)
        else:
            self.rectangle = rectangle

    def add_conditional(self, new_conditional):
        self.conditional = new_conditional 
        
    def unlink(self):
        if self.conditional:
            if isinstance(self, Conditional_Gate):
                self.conditional.conditional = None
                self.conditional = None
                self.aux_rectangle = pg.Rect(self.rectangle.midbottom[0], self.rectangle.midbottom[1] - 10, 30, 30)
            else:
                self.conditional.aux_rectangle = pg.Rect(self.rectangle.midbottom[0], self.rectangle.midbottom[1] - 10, 30, 30)
                self.conditional.conditional = None
                self.conditional = None

class Track(): #class for the track which each qbit moves along
    def __init__(self, input, level, position):
        self.input = input
        self.gates = []
        self.level = level
        self.position = position
        self.rectangle = pg.Rect(430, 0, 1480, 150)
    
    def move_gate(self, pos, new_gate):#moves around gates in the different tracks
        has_aux_gate = hasattr(new_gate, "aux_gate")
        
        level_Tracks = self.level.tracks
        
        method_Bypass = False
        method_Bypass = isinstance(new_gate, I_Gate)
        if not method_Bypass:
            method_Bypass = (isinstance(new_gate, AUX_Gate) and self.position == 0) or (isinstance(new_gate, SWAP_Gate) and self.position + 1 == len(self.level.tracks))
        
        if not method_Bypass:
            
            if new_gate.current_Track:
                new_gate.current_Track.gates.insert(new_gate.current_Position, I_Gate(0,None,self,new_gate.current_Position))
                new_gate.current_Track.gates.pop(new_gate.current_Position + 1)
        
            if has_aux_gate:
                if new_gate.aux_gate.current_Track:
                    new_gate.aux_gate.current_Track.gates.insert(new_gate.aux_gate.current_Position,(I_Gate(0,None,self,new_gate.current_Position)))
                    new_gate.aux_gate.current_Track.gates.pop(new_gate.current_Position + 1)
                    new_gate.aux_gate.current_Position = None
            
            new_gate.current_Position = None
            
            if not pos < len(self.gates):
                for x in range(pos - len(self.gates) +1):
                    self.gates.append(I_Gate(0,None,self, len(self.gates) + x))
        
            if has_aux_gate:
                if isinstance(new_gate, SWAP_Gate):
                    if not pos < len(level_Tracks[self.position + new_gate.aux_gate.distance].gates):
                        for x in range(pos - len(level_Tracks[self.position + new_gate.aux_gate.distance].gates) + 1):
                            level_Tracks[self.position + new_gate.aux_gate.distance].gates.append(I_Gate(0,None,self, len(self.gates) + x))
                else:
                    if not pos < len(level_Tracks[self.position - new_gate.distance].gates):
                        for x in range(pos - len(level_Tracks[self.position - new_gate.distance].gates) + 1):
                            level_Tracks[self.position - new_gate.distance].gates.append(I_Gate(0,None,self, len(self.gates) + x))
            if not new_gate.current_Track:
                updated_gate = copy.copy(new_gate)
                if has_aux_gate:
                    updated_gate.aux_gate = copy.copy(new_gate.aux_gate)
                    updated_gate.aux_gate.aux_gate = updated_gate
            else:
                updated_gate = new_gate
            updated_gate.current_Position = pos
            updated_gate.current_Track = self
            if isinstance(self.gates[pos], I_Gate):
                self.gates[pos] = updated_gate
            else:
                self.gates.insert(pos, updated_gate)
            if has_aux_gate:
                if isinstance(updated_gate.aux_gate.current_Track.gates[pos], I_Gate):
                    updated_gate.aux_gate.current_Track.gates[pos] = updated_gate.aux_gate
                else:
                    updated_gate.aux_gate.current_Track.gates.insert(pos, updated_gate.aux_gate)
            
            self.i_gate_cleaner()
            if has_aux_gate:
                updated_gate.aux_gate.current_Track.i_gate_cleaner()
            
            return updated_gate
        else: return new_gate
        
    
    def delete_gate(self, del_gate):
        after_gate = False
        for gate in self.gates:
            if after_gate:
                gate.current_Position -= 1
                gate.unlink()
            if gate == del_gate:
                after_gate = True
        if hasattr(del_gate, 'aux_gate'):
            after_aux_gate = False
            for gate in self.gates:
                if after_aux_gate:
                    gate.current_Position -= 1
                    gate.unlink()
                if gate == del_gate:
                    after_aux_gate = True
            del_gate.aux_gate.current_Track.gates.remove(del_gate.aux_gate)
            del_gate.aux_gate.unlink()
            del_gate.aux_gate.aux_gate = None
            del_gate.aux_gate = None
        self.gates.remove(del_gate)
        del_gate.unlink()
    
    def i_gate_cleaner(self):
        I_gates_length = 0
        for gate_index in range(len(self.gates)):
            if isinstance(self.gates[gate_index], I_Gate):
                I_gates_length += 1
            else:
                I_gates_length = 0
        self.gates = self.gates[0:len(self.gates) - I_gates_length]
        
class Level():
    def __init__(self, inputs, outputs, available_gates, goal_text, name):
        self.inputs = inputs
        self.outputs = outputs
        self.total_Cost = 0
        self.tracks = []
        self.available_gates = available_gates
        self.goal_text = goal_text
        self.name = name

    def add_track(self, track):
        self.tracks.append(track)

    def clear(self):
        self.tracks.clear()
        
    def move_track(self, pos, new_track):
        self.tracks.remove(new_track)
        self.tracks.insert(pos, new_track)
        
    def assign_Conditional(self, gate, conditional):
        if gate.current_Position == conditional.current_Position and (self.tracks.index(gate.current_Track) == self.tracks.index(conditional.current_Track) + 1 or self.tracks.index(gate.current_Track) == self.tracks.index(conditional.current_Track) - 1):
            gate.unlink()
            conditional.unlink()
            gate.conditional = conditional
            conditional.conditional = gate
            conditional.aux_rectangle = gate.rectangle.inflate(30,30)

    def run(self):
        #to iterate over the matrix column by column, we place it into a np.array object
        gate_Layers = np.array(self.tracks)
        #construction of the adequate QuantumCircuit object
        qr = qs.QuantumRegister(len(self.tracks))
        qc = qs.QuantumCircuit()
        qc.add_register(qr)
        for qbit_index in range(len(self.tracks)):
            qc.initialize(self.inputs, qr[qbit_index])
        for gate_Layer in gate_Layers.transpose():
            for gate in gate_Layer:
                gate.Qiskit_Equivalent_Dispatcher(qr)

class Quantum_Bit:
    def __init__(self):
        self.state = [1, 0, 0, 0]
        self.is_superposed = False
        self.is_entangled = False

    def set_state(self, zero_Prob, one_Prob, zero_Angle, one_Angle):
        self.state = [zero_Prob, zero_Angle, one_Prob, one_Angle]

    def update(self, statevector_Coordinates):
       self.state =  statevector_Coordinates
    """the statevector qiskit uses to describe entangled qbits are incomplete, for example: qbit 0 is (50%, 0%) and qbit 1 is (0%, 50%)
        so far, the way we've found to deal with this is to add the possibilities together, but we still need to check if it would work
        all the time """

    def get_state(self):
        return self.state

class Conditional_Gate(Quantum_Gate):
    def __init__(self, cost, conditional, current_Track, current_Position, rectangle = None):
        self.cost = cost
        self.conditional = conditional
        self.current_Track = current_Track
        self.current_Position = current_Position
        if rectangle is None:
            self.rectangle = pg.Rect(0, 0, 100, 100)
        else:
            self.rectangle = rectangle
        self.aux_rectangle = pg.Rect(self.rectangle.midbottom[0], self.rectangle.midbottom[1] - 10, 30, 30)
    
    def __str__(self):
        return "if"
    
    def __repr__(self):
        return self.__str__()
    
    def __copy__(self):
        return Conditional_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())
    


# here we start setting up the quantum gate that'll be in the final game
# they're all exactly the same, except for their Qiskit_Equivalent
class SWAP_Gate(Quantum_Gate):
    
    def __init__(self, cost, conditional, current_Track, current_Position, rectangle = None, aux_gate = None):
        self.cost = cost
        self.SWAPconditional = conditional
        self.SWAPcurrent_Track = current_Track
        self.SWAPcurrent_Position = current_Position
        if aux_gate is None:
            self.aux_gate = AUX_Gate(cost, self)
        else:
            self.aux_gate = aux_gate
        if rectangle is None:
            self.rectangle = pg.Rect(430, 0, 100, 100)
        else:
            self.rectangle = rectangle
    
    def __setattr__(self, name, value):
        if name == "conditional":
            self.SWAPconditional = value
        elif name == "current_Track":
            self.SWAPcurrent_Track = value
            if not self.SWAPcurrent_Track.level.tracks[self.SWAPcurrent_Track.position + self.aux_gate.distance] == value:
                self.aux_gate.SWAPcurrent_Track = self.SWAPcurrent_Track.level.tracks[self.SWAPcurrent_Track.position + self.aux_gate.distance]
        elif name == "current_Position":
            self.SWAPcurrent_Position = value
            try:
                if not self.aux_gate.current_Position == value:
                    self.aux_gate.current_Position = value
            except AttributeError:
                self.aux_gate.current_Position = value
        else:
            super(SWAP_Gate, self).__setattr__(name, value)
    
    def __getattr__(self, name):
        if name == "conditional":
            return self.SWAPconditional
        elif name == "current_Track":
            return self.SWAPcurrent_Track
        elif name == "current_Position":
            return self.SWAPcurrent_Position
    
    def __str__(self):
        return "SWAP"
    
    def __repr__(self):
        return self.__str__()
        
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.swap(self.current_Track, self.target_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cswap(self.Conditional.Get_Control_Qbit , self.current_Track, self.target_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return SWAP_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())
class AUX_Gate(Quantum_Gate):
    
    def __init__(self, cost, aux_gate):
        
        self.cost = cost
        self.SWAPconditional = None
        self.SWAPcurrent_Track = None
        self.SWAPcurrent_Position = 0
        self.distance = 1
        self.rectangle = pg.Rect(430, 0, 100, 100)
        self.aux_gate = aux_gate
    
    def __setattr__(self, name, value):
        if name == "conditional":
            self.aux_gate.SWAPconditional = value
        elif name == "current_Track":
            original_track = self.SWAPcurrent_Track
            original_aux_track = self.aux_gate.current_Track
            try:
                self.SWAPcurrent_Track = value
                try:
                    if not self.SWAPcurrent_Track.level.tracks[self.SWAPcurrent_Track.position - self.distance] == value:
                        self.aux_gate.SWAPcurrent_Track = self.SWAPcurrent_Track.level.tracks[self.SWAPcurrent_Track.position - self.distance]
                except AttributeError:
                    self.aux_gate.current_Track = self.SWAPcurrent_Track.level.tracks[self.SWAPcurrent_Track.position - self.distance]
            except IndexError:
                self.SWAPcurrent_Track = original_track
                self.aux_gate.current_Track = original_aux_track
        elif name == "current_Position":
            self.SWAPcurrent_Position = value
            try:
                if not self.aux_gate.current_Position == value:
                    self.aux_gate.current_Position = value
            except AttributeError:
                self.aux_gate.current_Position = value
        else:
            super(AUX_Gate, self).__setattr__(name, value)
    
    def __getattr__(self, name):
        if name == "conditional":
            return self.SWAPconditional
        elif name == "current_Track":
            return self.SWAPcurrent_Track
        elif name == "current_Position":
            return self.SWAPcurrent_Position
    
    def __str__(self):
        return "SWAP"
    
    def __repr__(self):
        return "aux"
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        pass
    
    def __copy__(self):
        return AUX_Gate(self.cost, self.aux_gate)

class H_Gate(Quantum_Gate):

    def __str__(self):
        return "H"

    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None :
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.h(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.ch(self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return H_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())

class X_Gate(Quantum_Gate):
    
    def __str__(self):
        return "X"

    def __repr__(self):
        return self.__str__()

    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.x(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cnot(self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return X_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())

class T_Gate(Quantum_Gate):

    def __str__(self):
        return "T"

    def __repr__(self):
        return self.__str__()

    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi/4, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi/4, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return T_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())

class Z_Gate(Quantum_Gate):

    def __str__(self):
        return "Z"

    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return Z_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())

class S_Gate(Quantum_Gate):

    def __str__(self):
        return "S"

    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        if self.Conditional is None or self.conditional is False:
            self.Qiskit_Equivalent(Quantum_Circuit)
        else:
            self.Conditional_Qiskit_Equivalent(Quantum_Circuit)
    
    def qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.p(math.pi/2, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def conditional_qiskit_equivalent(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.cp(math.pi/2, self.Conditional.Get_Control_Qbit, self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return S_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())
    
class I_Gate(Quantum_Gate):
    
    def __str__(self):
        return "I"
    
    def __repr__(self):
        return self.__str__()
    
    def qiskit_equivalent_dispatcher(self, Quantum_Circuit):
        Quantum_Circuit.barrier()
        Quantum_Circuit.id(self.current_Track)
        Quantum_Circuit.snapshot()
        return Quantum_Circuit
    
    def __copy__(self):
        return I_Gate(self.cost,self.conditional,self.current_Track, self.current_Position, self.rectangle.copy())
