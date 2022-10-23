from qiskit import *
from qiskit.visualization import plot_histogram
import numpy as np
from IPython.display import display # for displaying the circuit using text
import matplotlib.pyplot as plt

from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor

# def NOT(inp):
#     """
#     An NOT gate using quantum circuit.

#     Parameters: 
#         inp (str): the input string

#     Returns:
#         QuantumCircuit: the quantum NOT circuit
#         str: the output string that is NOT of the input
#     """

#     # initialize the circuit
#     qc = QuantumCircuit(1,1)
#     qc.reset(0)
    
#     # encode the input into qubit
#     if inp=='1':
#         qc.x(0)
#     elif inp=='0':
#         pass
#     else:
#         raise ValueError('Input value not allowed')
#     qc.barrier()

#     qc.x(0)

#     qc.barrier()

#     # measure the output
#     qc.measure(0,0)


#     display(qc.draw(output='text'))
#     qc.draw(output='mpl')
#     plt.show()

#     # get the result using the aer simulator
#     backend = Aer.get_backend('aer_simulator')
#     job = backend.run(qc, shots=1, memory=True)
#     out = job.result().get_memory()[0] # get_memory 
    
#     return qc, out

# def XOR(inp1, inp2):
#     """
#     The output is '0' when inputs are equal and '1' otherwise. 
#     Improvement: Add input type error control

#     Parameters:
#         inp1, inp2 (str): either being '0' or '1'
    
#     Returns:
#         qc (QuantumCircuit)
#         out (str) 
#     """
#     qc = QuantumCircuit(2, 1)
#     qc.reset(range(2))

#     if inp1=='1':
#         qc.x(0)
#     if inp2=='1':
#         qc.x(1)

#     qc.barrier()

#     qc.cx(0,1)

#     qc.barrier()

#     qc.measure(1,0)
    
#     display(qc.draw(output='text'))
#     qc.draw(output='mpl')
#     plt.show()

#     # get the result using the aer simulator
#     backend = Aer.get_backend('aer_simulator')
#     job = backend.run(qc, shots=1, memory=True)
#     out = job.result().get_memory()[0] # get_memory 

#     return qc, out


def AND(inp1, inp2, backend, layout):
    '''
    A quantum circuit that performs the AND operation on the two input strings 

    Parameters:
        inp1, inp2 (str): value range '0' or '1'
    
    Returns:
        qc (QuantumCircuit)
        out (str): out='1' only when inp1=inp2='1'
    '''
    # initialize the quantum circuit
    qc = QuantumCircuit(3,1)
    qc.reset(range(3))

    # encode the inputs to the control qubit states
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
    qc.barrier()

    # apply the Toffoli gate to transform the target qubit state to AND
    qc.ccx(0,1,2)
    qc.barrier()

    # measurement
    qc.measure(2, 0)

    # # draw the circuit
    # display(qc.draw(output='text'))
    # qc.draw(output='mpl')
    # plt.show()

    # # simulation
    # backend = Aer.get_backend('aer_simulator')
    # job = backend.run(qc, shots=1, memory=True)
    # out = job.result().get_memory()[0]

    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = backend.run(qc_trans, shots=8192)
    print(job.job_id())
    job_monitor(job)
    
    out = job.result().get_counts()

    return qc_trans, out


def NAND(inp1, inp2):
    '''
    A quantum circuit that performs the NAND operation on the two input strings 

    Parameters:
        inp1, inp2 (str): value range '0' or '1'
    
    Returns:
        qc (QuantumCircuit)
        out (str): out='0' only when inp1=inp2='1'
    '''
    # initialize the quantum circuit
    qc = QuantumCircuit(3,1)
    qc.reset(range(3))
    qc.x(2) # the target qubit is initialized to be in state |1>

    # encode the inputs to the control qubit states
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
    qc.barrier()

    # apply the Toffoli gate to transform the target qubit state to AND
    qc.ccx(0,1,2)
    qc.barrier()

    # measurement
    qc.measure(2, 0)

    # draw the circuit
    display(qc.draw(output='text'))
    qc.draw(output='mpl')
    plt.show()

    # simulation
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(qc, shots=1, memory=True)
    out = job.result().get_memory()[0]

    return qc, out

def OR(inp1, inp2):
    '''
    The OR gate 
    '''
    qc = QuantumCircuit(3,1)
    qc.reset(range(3))

    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)

    qc.barrier()

    qc.ccx(0,1,2)
    qc.cx(0,1)
    qc.cx(2,1)

    qc.measure(1,0)

    # draw the circuit
    display(qc.draw(output='text'))
    qc.draw(output='mpl')
    plt.show()


    backend = Aer.get_backend('aer_simulator')
    job = backend.run(qc, shots=1, memory=True)
    out = job.result().get_memory()[0]

    return qc, out

# # test the NOT gate 
# for inp in ['0', '1']: 
#     qc, output = NOT(inp)
#     print('NOT with input', inp, 'gives output', output)
#     print(type(output))
#     print('\n')

# # test the XOR gate
# for inp1 in ['0','1']:
#     for inp2 in ['0','1']:
#         qc, out = XOR(inp1, inp2)
#         print('[input1, input2] = [', inp1, ',', inp2, '], output =', out)
#         print('\n')

# # test the NAND gate
# for inp1 in ['0','1']:
#     for inp2 in ['0','1']:
#         qc, out = NAND(inp1, inp2)
#         print('[input1, input2] = [', inp1, ',', inp2, '], output =', out)
#         print('\n')

# # test the OR gate
# for inp1 in ['0','1']:
#     for inp2 in ['0','1']:
#         qc, out = OR(inp1, inp2)
#         print('[input1, input2] = [', inp1, ',', inp2, '], output =', out)
#         print('\n')

# IBMQ.save_account('Your Token')
IBMQ.load_account()

IBMQ.providers()


provider = IBMQ.get_provider('ibm-q')
print('All available quantum machines that has 3 qubits are', provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and 
                                        not x.configuration().simulator and x.status().operational==True))

backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and 
                                        not x.configuration().simulator and x.status().operational==True))
print('The least busy backend is', backend, ', we choose it as our backend.')

layout = list(range(3))

output_all = []
qc_trans_all = []
prob_all = []

worst = 1
best = 0
# test the ADD gate
for inp1 in ['0','1']:
    for inp2 in ['0','1']:
        qc_trans, out = AND(inp1, inp2, backend, layout)

        output_all.append(out)
        qc_trans_all.append(qc_trans)

        prob = out[str(int(inp1) and int(inp2))]/8192 
        prob_all.append(prob)

        print('\nProbability of correct answer for [input1, input2] = [', inp1, ',', inp2)
        print('{:.2f}'.format(prob))
        print('------------------------------------')

        worst = min(worst, prob)
        best = max(best, prob)

print('')
print('\nThe highest of these probabilities was {:.2f}'.format(best))
print('The lowest of these probabilities was {:.2f}'.format(worst))




print('Transpiled AND gate circuit for ibmq_vigo with input 0 0')
print('\nThe circuit depth : {}'.format (qc_trans_all[0].depth()))
print('# of nonlocal gates : {}'.format (qc_trans_all[0].num_nonlocal_gates()))
print('Probability of correct answer : {:.2f}'.format(prob_all[0]) )
qc_trans_all[0].draw()

print('Transpiled AND gate circuit for ibmq_vigo with input 0 1')
print('\nThe circuit depth : {}'.format (qc_trans_all[1].depth()))
print('# of nonlocal gates : {}'.format (qc_trans_all[1].num_nonlocal_gates()))
print('Probability of correct answer : {:.2f}'.format(prob_all[1]) )
qc_trans_all[1].draw()

print('Transpiled AND gate circuit for ibmq_vigo with input 1 0')
print('\nThe circuit depth : {}'.format (qc_trans_all[2].depth()))
print('# of nonlocal gates : {}'.format (qc_trans_all[2].num_nonlocal_gates()))
print('Probability of correct answer : {:.2f}'.format(prob_all[2]) )
qc_trans_all[2].draw()

print('Transpiled AND gate circuit for ibmq_vigo with input 1 1')
print('\nThe circuit depth : {}'.format (qc_trans_all[3].depth()))
print('# of nonlocal gates : {}'.format (qc_trans_all[3].num_nonlocal_gates()))
print('Probability of correct answer : {:.2f}'.format(prob_all[3]) )
qc_trans_all[3].draw()




print('end')



