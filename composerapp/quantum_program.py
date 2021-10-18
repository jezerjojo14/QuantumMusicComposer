# from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
# from qiskit import execute, IBMQ, Aer
# from qiskit.compiler import transpile
# from qiskit.providers.ibmq import least_busy
# from qiskit.quantum_info.operators import Operator
# from math import *
# import numpy as np

# notes=["C4", "D4", "E4", "F4", "G4", "A5", "B5", "C5"]

# def generate_rhythm(a=0.5, b=0.5, c=0.5, d=0.5, weight=4):
#     qc=QuantumCircuit(4)
#     qc.ry(a*pi,3)
#     qc.ry(b*pi,2)
#     qc.ry(c*pi,1)
#     qc.ry(d*pi,0)
#     qc.measure_all()

#     backend_sim = Aer.get_backend('qasm_simulator')
#     job_sim = backend_sim.run(transpile(qc, backend_sim), shots=weight)
#     result_sim = job_sim.result()
#     counts = result_sim.get_counts(qc)
#     ret_list=[int(key,2)/4.0 for key in counts.keys()]
#     ret_list.sort()
#     return ret_list


# def generate_melody(length, matrix):

#     rhythm=[]
#     i=0

#     while len(rhythm)<length:
#         rhythm+=[t+4*i for t in generate_rhythm(a=0.4, b=0.3, c=0.2, d=0.2, weight=10)]
#         i+=1

#     rhythm=rhythm[:length]

#     length=int(length/2)

#     qc=QuantumCircuit(QuantumRegister(3), QuantumRegister(3))
#     qc.h(list(range(6)))
#     U=Operator(matrix)
#     for note in range(length):
#         qc.measure_all()
#         qc.append(U, list(range(6)))

#     backend_sim = Aer.get_backend('qasm_simulator')
#     job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1)
#     result_sim = job_sim.result()
#     counts = result_sim.get_counts(qc)

#     for m in counts.keys():
#         measurement_edges=m.split()

#     measurement=[]

#     for edge in measurement_edges:
#         measurement+=[edge[3:], edge[:3]]

#     print(measurement)
#     # print(qc.draw("text"))

#     melody_data={}

#     i=0
#     for t in measurement:
#         if notes[int(t,2)] not in melody_data.keys():
#             melody_data[notes[int(t,2)]]=[]
#         melody_data[notes[int(t,2)]]+=[rhythm[i]]
#         i+=1

#     return melody_data


# def operator_matrix(transition_matrix):
#     note_array = lambda x : np.array([0 for _ in range(x)]+[1]+[0 for _ in range(7-x)])
#     phi = lambda x : np.kron(note_array(x), sum([sqrt(transition_matrix[x,y])*note_array(y) for y in range(8)]))
#     psi = lambda y : np.kron(sum([sqrt(transition_matrix[y,x])*note_array(x) for x in range(8)]), note_array(y))
#     r1 = 2*sum([np.outer(phi(x), phi(x)) for x in range(8)]) - np.identity(64)
#     r2 = 2*sum([np.outer(psi(y), psi(y)) for y in range(8)]) - np.identity(64)
#     W = np.matmul(r2, r1)
#     return W


# def generate_composition(mood="happy"):

#     # # Ode to Joy
#     # data={"C4": [8,9], "D4": [7,10,13,14], "E4": [0, 1, 6, 11, 12], "F4": [2,5], "G4": [3,4]}
#     transition_matrix=[
#     [1.2, 2.3, 1.2, 1.0, 1, 1, 0, 1],
#     [0.8, 0.2, 1.5, 1.0, 1, 1, 0, 1],
#     [1.2, 2.0, 0.5, 1.4, 1, 1, 0, 1],
#     [1.4, 1.5, 1.6, 1.0, 1, 1, 0, 1],
#     [1.8, 0.8, 1.0, 1.4, 1, 1, 2.5, 1],
#     [0.5, 0.6, 1.0, 1.0, 1, 1, 2.5, 1],
#     [0.1, 0.2, 0.2, 0.2, 1, 1, 0.5, 1],
#     [1.0, 0.4, 1.0, 1.0, 1, 1, 2.5, 1]]
#     data=generate_melody(60, operator_matrix((1/8.0)*np.transpose(np.array(transition_matrix))))
#     # data=generate_melody(60, operator_matrix(np.eye(8)))
#     print(data)

#     max=0
#     for datum in data.keys():
#         for t in data[datum]:
#             if t>max:
#                 max=t
#     kick_rhythm_element=generate_rhythm(a=0.5, b=0.3, c=0.2, d=0.1)
#     kick_rhythm=[]
#     for i in range(int((max/4)+1)):
#         kick_rhythm+=[4*i+value for value in kick_rhythm_element]
#     data["kick"]=kick_rhythm

#     snare_rhythm_element=generate_rhythm(a=0.5, b=0.8, c=0.2, d=0.1)
#     snare_rhythm=[]
#     for i in range(int((max/4)+1)):
#         snare_rhythm+=[4*i+value for value in snare_rhythm_element]
#     data["snare"]=snare_rhythm

#     hihat_rhythm_element=generate_rhythm(a=0.5, b=0.6, c=0.5, d=0.5, weight=15)
#     hihat_rhythm=[]
#     for i in range(int((max/4)+1)):
#         hihat_rhythm+=[4*i+value for value in hihat_rhythm_element]
#     data["hihat"]=hihat_rhythm

#     return data
