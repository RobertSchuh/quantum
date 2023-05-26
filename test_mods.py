import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def test_cycles(circuit, cycles):
    i = 1
    for application in range(cycles):
        print("Apply %s, %i times: %i" % (circuit.name, application, i))
        sv = Statevector.from_int(i, 32)  # 32 is no. of elements in vector (dimension)
        sv = sv.evolve(circuit)
        output = sv.sample_memory(1)[0]  # simulate one shot (circuit is deterministic)
        i = int(output, 2)  # convert binary output to int


tm15 = QuantumCircuit(5)  # 2x mod 15
tm15.name = "2x (mod 15)"
tm15.swap(0, 3)
tm15.swap(3, 2)
tm15.swap(2, 1)

test_cycles(tm15, 6)
tm15.draw()


tm31 = QuantumCircuit(5)
tm31.name = "2x (mod 31)"
tm31.swap(3, 4)
tm31 = tm31.compose(tm15)

test_cycles(tm31, 6)
tm31.draw()

tm21 = QuantumCircuit(5)
tm21.name = "2x mod 21"
tm21.cswap(0,3,4)
tm21.cswap(0,1,2)
tm21.cx(4, 2)
tm21.cx(4, 0)
tm21 = tm21.compose(tm31)

test_cycles(tm21, 8)
tm21.draw()
