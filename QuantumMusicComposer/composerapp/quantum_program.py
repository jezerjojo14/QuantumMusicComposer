from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ, Aer
from qiskit.compiler import transpile
from qiskit.providers.ibmq import least_busy
from qiskit.quantum_info.operators import Operator
from math import *
import numpy as np


def generate_composition(args):
    data={}
    return data

def generate_melody(length, matrix=np.identity(8)):
    qc=QuantumCircuit(3)
    qc.h([0,1,2])
    U=Operator(matrix)
    for note in range(length):
        qc.measure_all()
        qc.append(U, [0,1,2])
    print(qc.draw('text'))



def generate_beat(a=0.5, b=0.5, c=0.5, d=0.5, weight=4):

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
    return counts


kick_beats=generate_beat(a=0.5, b=0.3, c=0.2, d=0.1)
print(kick_beats)
snare_beats=generate_beat(a=0.5, b=0.8, c=0.2, d=0.1)
print(snare_beats)

generate_melody(4)
