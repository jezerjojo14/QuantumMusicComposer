from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ, Aer
from qiskit.compiler import transpile
from qiskit.providers.ibmq import least_busy
from qiskit.quantum_info.operators import Operator
from math import *
import numpy as np


def generate_melody(length, matrix=np.identity(8)):
    qc=QuantumCircuit(3)
    qc.h([0,1,2])
    U=Operator(matrix)
    for note in range(length):
        qc.measure_all()
        qc.append(U, [0,1,2])
    print(qc.draw('text'))



def generate_rhythm(a=0.5, b=0.5, c=0.5, d=0.5, weight=4):
    qc=QuantumCircuit(4)
    qc.ry(a*pi,3)
    qc.ry(b*pi,2)
    qc.ry(c*pi,1)
    qc.ry(d*pi,0)
    qc.measure_all()

    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = backend_sim.run(transpile(qc, backend_sim), shots=weight)
    result_sim = job_sim.result()
    counts = result_sim.get_counts(qc)
    ret_list=[int(key,2)/4.0 for key in counts.keys()]
    ret_list.sort()
    return ret_list


def generate_composition(mood="happy"):
    data={"C4": [8,9], "D4": [7,10,13,14], "E4": [0, 1, 6, 11, 12], "F4": [2,5], "G4": [3,4]}
    max=0
    for datum in data.keys():
        for t in data[datum]:
            if t>max:
                max=t
    kick_rhythm=generate_rhythm(a=0.5, b=0.3, c=0.2, d=0.1)
    print(kick_rhythm)
    for i in range(int(log2(max))-1):
        kick_rhythm=kick_rhythm+[2**(i+2)+value for value in kick_rhythm]
    data["kick"]=kick_rhythm

    snare_rhythm=generate_rhythm(a=0.5, b=0.8, c=0.2, d=0.1)
    print(snare_rhythm)
    for i in range(int(log2(max))-1):
        snare_rhythm=snare_rhythm+[2**(i+2)+value for value in snare_rhythm]
    data["snare"]=snare_rhythm

    hihat_rhythm=generate_rhythm(a=0.5, b=0.6, c=0.5, d=0.5, weight=15)
    print(hihat_rhythm)
    for i in range(int(log2(max))-1):
        hihat_rhythm=hihat_rhythm+[2**(i+2)+value for value in hihat_rhythm]
    data["hihat"]=hihat_rhythm

    return data

# print(generate_composition())


# kick_rhythm=generate_rhythm(a=0.5, b=0.3, c=0.2, d=0.1)
# print(kick_rhythm)
# kick_rhythm=[int(key,2)/4.0 for key in kick_rhythm.keys()]
# kick_rhythm.sort()
# snare_rhythm=generate_rhythm(a=0.5, b=0.8, c=0.2, d=0.1)
# print(snare_rhythm)
# snare_rhythm=[int(key,2)/4.0 for key in snare_rhythm.keys()]
# snare_rhythm.sort()
# print(kick_rhythm)
# print(snare_rhythm)
#
# generate_melody(4)
