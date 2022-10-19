from qiskit import *
from qiskit.visualization import plot_histogram
import numpy as np
from IPython.display import display # for displaying the circuit using text
import matplotlib.pyplot as plt


def NOT(inp):
    """
    An NOT gate using quantum circuit.

    Parameters: 
        inp (str): the input string (either '0' or '1') encoded to qubit 0

    Returns:
        QuantumCircuit: the quantum NOT circuit
        str: the output string that is NOT of the input
    """

    # initialize the circuit
    qc = QuantumCircuit(1,1)
    qc.reset(0)

    # encode the input into qubit
    if inp=='1':
        qc.x(0)
    elif inp=='0':
        pass
    else:
        raise ValueError('Input value not allowed')

    qc.barrier()

    # measure the output
    qc.measure(0,0)


    display(qc.draw(output='text'))
    qc.draw(output='mpl')
    plt.show()

    # get the result using the aer simulator
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(qc, shots=1, memory=True)
    out = job.result().get_memory()[0] # get_memory 
    
    return qc, out

def XOR(inp1, inp2):
    """
    The output is '0' when inputs are equal and '1' otherwise. 
    Improvement: Add error control

    Parameters:

    Returns:

    """
    qc = QuantumCircuit(2, 1)
    qc.reset(range(2))

    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)

    qc.barrier()

    qc.cx(0,1)

    qc.barrier()

    qc.measure(1,0)
    
    display(qc.draw(output='text'))
    qc.draw(output='mpl')
    plt.show()

    # get the result using the aer simulator
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(qc, shots=1, memory=True)
    out = job.result().get_memory()[0] # get_memory 

    return qc, out







# test the NOT gate 
for inp in ['0', '1']: 
    qc, output = NOT(inp)
    print('NOT with input', inp, 'gives output', output)
    print(type(output))
    print('\n')

# test the XOR gate
for inp1 in ['0','1']:
    for inp2 in ['0','1']:
        qc, out = XOR(inp1, inp2)
        print('[input1, input2] = [', inp1, ',', inp2, '], output =', out)
        print('\n')




print('end')