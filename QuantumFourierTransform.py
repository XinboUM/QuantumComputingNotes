# The draw function is not working. Probably I have not installed the drawing functionalities on my machine.
# Other than that everything looks fine.

# development improvement: 
# Make the qft, iqft operate on the first n qubits of a given quantum circuit.

import numpy as np
from numpy import pi
# from numpy import fft

from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector


# n: the number of qubits
def qft_rotations(circuit, n):
    if n==0:
        return circuit
    n -= 1
    circuit.h(n)
    for cqubit in range(n):
        circuit.cp(pi/2**(n-cqubit), cqubit, n)
    qft_rotations(circuit, n)
    
    
def swap_registers(circuit, n):
    for qubit in range(n//2): 
        circuit.swap(qubit, n-1-qubit)
#     return circuit
        
def qft(circuit, n):
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
    
nqubit = 3
qc = QuantumCircuit(nqubit)
qft(qc, nqubit)
qc.draw()

sv = Statevector.from_label('011')
print("The initial statevector is: \n", sv.data)
sv = sv.evolve(qc)
print("The statevector after QFT is: \n", sv.data)


def iqft(circuit, n):
    qft_circ = qft(QuantumCircuit(n), n)
    iqft_circ = qft_circ.inverse()
    circuit.append(iqft_circ, circuit.qubits[:n])
    return circuit.decompose()

# the quantum circuit that encodes |3> in Fourier basis
number = 3
qc = QuantumCircuit(nqubit)
for qubit in range(nqubit):
    qc.h(qubit)
    qc.p(number*2*pi/2**(2-qubit+1), qubit)

qc = iqft(qc, nqubit)
qc.draw()


qc.save_statevector()







print("end\n")