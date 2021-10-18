from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ, Aer
from qiskit.compiler import transpile
from qiskit.providers.ibmq import least_busy
from qiskit.quantum_info.operators import Operator
from math import *
import numpy as np
from qiskit.circuit import quantumcircuit
from qiskit.providers.aer import QasmSimulator

notes=["C4", "C#4", "D4", "Eb4", "E4", "F4", "F#4", "G4", "G#4", "A5", "Bb5", "B5", "C5"]
major_steps=[0,2,2,1,2,2,2,1]
minor_steps=[0,2,1,2,2,2,2,1]
mel_minor_steps=[0,2,1,2,2,1,3,1]

chord_progressions={
    "happy": [
        {"progression": ["C","G","Am","F"], "scale": "CM"},
        {"progression": ["Am","G","D","D"], "scale": "Am"},
        {"progression": ["G","C","D","A"], "scale": "GM"},
        {"progression": ["A","D","E","E"], "scale": "AM"}
    ],
    "emotional": [
        {"progression": ["Am","G","F","G"], "scale": "Am"},
        {"progression": ["Am","F","C","G"], "scale": "CM"},
    ],
    "hopeful": [
        {"progression": ["C","D","Em","G"], "scale": "GM"},
        {"progression": ["A","B","C#m","E"], "scale": "EM"},
        {"progression": ["F","G","Am","C"], "scale": "CM"},
        {"progression": ["Eb","F","Gm","Bb"], "scale": "BbM"}
    ],
    "sad": [
        {"progression": ["C","Am","F","G"], "scale": "CM"},
        {"progression": ["C","Am","Dm","G"], "scale": "CM"},
        # Will add third one later
    ],
    "evil": [
        {"progression": ["Am","Em","F","Dm"], "scale": "Am"},
        {"progression": ["Am","Em","G","F"], "scale": "Am"},
    ],
    "sinister": [
        {"progression": ["Dm","Am","Em","F"], "scale": "Dm"},
        # {"progression": ["CSpecial","CSpecial","EbSpecial","EbSpecial"], "scale": "Gs"},
        {"progression": ["Cm","Cm","Ebm","Ebm"], "scale": "Gs"},
    ],
}


def getList(dict):
    return list(dict.keys())

simulator = QasmSimulator()


def generate_chords(length, mood):

    progressions = chord_progressions[mood]
    # print("number of qubits if log2 of",len(progressions),"=", int(log2(len(progressions))))
    circuit = QuantumCircuit(int(log2(len(progressions))))
    circuit.h(range(int(log2(len(progressions)))))
    circuit.measure_all()

    res = []

    for i in range(int(length/16)+int(length%16!=0)):
        compiled_circuit = transpile(circuit, simulator)
        job = simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(compiled_circuit)
        res.append(getList(counts)[0])

    return (sum([progressions[int(val,2)]["progression"] for val in res],[]), [progressions[int(val,2)]["scale"] for val in res])



def st_number(note_number, scale_root, scale_type):
    try:
        pos=notes.index(scale_root+"4")
    except:
        pos=notes.index(scale_root+"5")

    if scale_type=="M":
        pos+=sum(major_steps[:note_number+1])
    elif scale_type=="m":
        pos+=sum(minor_steps[:note_number+1])
    else:
        pos+=sum(mel_minor_steps[:note_number+1])

    # print(note_number, pos, pos-12*int(pos>=13))
    return pos-12*int(pos>=13)

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


def generate_melody(length, matrix, scale_root="C", scale_type="M"):

    rhythm=generate_rhythm(a=0.5, b=0.34, c=0.15, d=0.15, weight=20)
    i=1

    while rhythm[-1]<length-4:
        rhythm+=[t+4*i for t in generate_rhythm(a=0.5, b=0.34, c=0.15, d=0.15, weight=20)]
        i+=1


    qc=QuantumCircuit(QuantumRegister(3), QuantumRegister(3))
    qc.h(list(range(6)))
    U=Operator(matrix)
    for note in range(int(len(rhythm)/2)):
        qc.measure_all()
        qc.append(U, list(range(6)))

    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1)
    result_sim = job_sim.result()
    counts = result_sim.get_counts(qc)

    for m in counts.keys():
        measurement_edges=m.split()

    measurement=[]

    for edge in measurement_edges:
        measurement+=[edge[3:], edge[:3]]

    # print(measurement)
    # print(qc.draw("text"))

    melody_data={}

    i=0

    print(notes[st_number(0,scale_root,scale_type)], scale_root)
    print(notes[st_number(1,scale_root,scale_type)], scale_root)
    print(notes[st_number(2,scale_root,scale_type)], scale_root)
    print(notes[st_number(3,scale_root,scale_type)], scale_root)
    print(notes[st_number(4,scale_root,scale_type)], scale_root)
    print(notes[st_number(5,scale_root,scale_type)], scale_root)
    print(notes[st_number(6,scale_root,scale_type)], scale_root)
    print(notes[st_number(7,scale_root,scale_type)], scale_root)

    for t in measurement:
        st_num=st_number(int(t,2),scale_root,scale_type)
        if notes[st_num] not in melody_data.keys():
            melody_data[notes[st_num]]=[rhythm[i]]
        melody_data[notes[st_num]]+=[rhythm[i]]
        i+=1

    return melody_data


def operator_matrix(transition_matrix):
    note_array = lambda x : np.array([0 for _ in range(x)]+[1]+[0 for _ in range(7-x)])
    phi = lambda x : np.kron(note_array(x), sum([sqrt(transition_matrix[x,y])*note_array(y) for y in range(8)]))
    psi = lambda y : np.kron(sum([sqrt(transition_matrix[y,x])*note_array(x) for x in range(8)]), note_array(y))
    r1 = 2*sum([np.outer(phi(x), phi(x)) for x in range(8)]) - np.identity(64)
    r2 = 2*sum([np.outer(psi(y), psi(y)) for y in range(8)]) - np.identity(64)
    W = np.matmul(r2, r1)
    return W


def melody_add(mel1, mel2, l):
    combined={}
    for note in mel1.keys():
        if note in mel2.keys():
            combined[note]=mel1[note]+[val+l for val in mel2[note]]
        else:
            combined[note]=mel1[note]
    for note in mel2.keys():
        if note not in mel1.keys():
            combined[note]=[val+l for val in mel2[note]]
    return combined

def generate_composition(mood="happy"):

    progressions=generate_chords(128, mood)
    chords_seq=progressions[0]
    scales=progressions[1]
    chords={}
    for i in range(len(chords_seq)):
        if chords_seq[i] in chords.keys():
            chords[chords_seq[i]]+=[4*i]
        else:
            chords[chords_seq[i]]=[4*i]

    major_matrix=[
    [0.09174311926605505, 0.1834862385321101, 0.1834862385321101, 0.09174311926605505, 0.1834862385321101, 0.11009174311926606, 0.06422018348623854, 0.09174311926605505],
    [0.1769911504424779, 0.08849557522123895, 0.13274336283185842, 0.1504424778761062, 0.1769911504424779, 0.12389380530973451, 0.061946902654867256, 0.08849557522123895],
    [0.1851851851851852, 0.1388888888888889, 0.0462962962962963, 0.1574074074074074, 0.1851851851851852, 0.12962962962962962, 0.06481481481481481, 0.0925925925925926],
    [0.14184397163120566, 0.049645390070921974, 0.21276595744680848, 0.0070921985815602835, 0.21276595744680848, 0.14184397163120566, 0.021276595744680847, 0.21276595744680848],
    [0.12318840579710144, 0.05072463768115942, 0.21739130434782608, 0.007246376811594203, 0.21739130434782608, 0.14492753623188406, 0.021739130434782608, 0.21739130434782608],
    [0.1875, 0.125, 0.125, 0.125, 0.0625, 0.125, 0.0625, 0.1875],
    [0.1, 0.13333333333333333, 0.06666666666666667, 0.0, 0.16666666666666666, 0.2, 0.0, 0.3333333333333333],
    [0.14925373134328357, 0.07462686567164178, 0.07462686567164178, 0.07462686567164178, 0.29850746268656714, 0.07462686567164178, 0.14925373134328357, 0.1044776119402985]
    ]

    minor_matrix=[
    [0.17467248908296945, 0.08733624454148473, 0.08733624454148473, 0.13100436681222707, 0.15283842794759828, 0.13100436681222707, 0.10480349344978167, 0.13100436681222707],
    [0.08583690987124465, 0.10300429184549358, 0.1716738197424893, 0.15021459227467812, 0.12875536480686697, 0.08583690987124465, 0.1716738197424893, 0.10300429184549358],
    [0.11764705882352941, 0.13725490196078433, 0.0784313725490196, 0.1568627450980392, 0.0784313725490196, 0.13725490196078433, 0.13725490196078433, 0.1568627450980392],
    [0.15695067264573992, 0.17937219730941706, 0.10762331838565023, 0.08968609865470853, 0.1345291479820628, 0.1345291479820628, 0.08968609865470853, 0.10762331838565023],
    [0.15444015444015444, 0.11583011583011583, 0.13513513513513514, 0.15444015444015444, 0.09266409266409266, 0.11583011583011583, 0.15444015444015444, 0.07722007722007722],
    [0.09876543209876543, 0.1646090534979424, 0.12345679012345678, 0.09876543209876543, 0.1646090534979424, 0.14403292181069957, 0.0823045267489712, 0.12345679012345678],
    [0.13953488372093023, 0.09302325581395349, 0.18604651162790697, 0.11627906976744186, 0.09302325581395349, 0.13953488372093023, 0.13953488372093023, 0.09302325581395349],
    [0.16666666666666666, 0.16666666666666666, 0.125, 0.10416666666666667, 0.08333333333333333, 0.14583333333333334, 0.08333333333333333, 0.125]
    ]


    transition_matrix=minor_matrix
    data={}
    i=0
    for scale in scales:
        if scale[-1]=="M":
            transition_matrix=major_matrix
        mini_melody=generate_melody(16, operator_matrix(np.array(transition_matrix)), scale[:-1], scale[-1])
        data=melody_add(data, mini_melody, i*16)
        i+=1

    # data=generate_melody(60, operator_matrix(np.eye(8)))
    print(data)

    max=0
    for datum in data.keys():
        for t in data[datum]:
            if t>max:
                max=t
    kick_rhythm_element=generate_rhythm(a=0.5, b=0.3, c=0.2, d=0.1)
    kick_rhythm=[]
    for i in range(int((max/4)+1)):
        kick_rhythm+=[4*i+value for value in kick_rhythm_element]
    data["kick"]=kick_rhythm

    snare_rhythm_element=generate_rhythm(a=0.5, b=0.8, c=0.2, d=0.1)
    snare_rhythm=[]
    for i in range(int((max/4)+1)):
        snare_rhythm+=[4*i+value for value in snare_rhythm_element]
    data["snare"]=snare_rhythm

    hihat_rhythm_element=generate_rhythm(a=0.5, b=0.6, c=0.5, d=0.5, weight=15)
    hihat_rhythm=[]
    for i in range(int((max/4)+1)):
        hihat_rhythm+=[4*i+value for value in hihat_rhythm_element]
    data["hihat"]=hihat_rhythm



    # {"solo_parts": {}, "chords": {"C": 0, "G": 4, "Am": 8, "F": 12, "G": 16, }}
    return {"solo_parts": data, "chords": chords}
