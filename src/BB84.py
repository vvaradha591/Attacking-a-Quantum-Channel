import random
import cirq

class BB84Protocol:
    def __init__(self, num_bits=20):
        self.num_bits = num_bits
        self.simulator = cirq.Simulator()

        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []

        self.sifted_key_alice = []
        self.sifted_key_bob = []

    def generate_alice_data(self):
        #Generate Alice's random bits and bases.
        self.alice_bits = [random.randint(0, 1) for _ in range(self.num_bits)]
        self.alice_bases = [random.choice(["Z", "X"]) for _ in range(self.num_bits)]

    def generate_bob_bases(self):
        #Generate Bob's random measurement bases.
        self.bob_bases = [random.choice(["Z", "X"]) for _ in range(self.num_bits)]

    def build_circuit(self, index):
        #Create the BB84 circuit for one qubit.
        qubit = cirq.NamedQubit(f"q{index}")
        circuit = cirq.Circuit()

        # Alice prepares the qubit
        if self.alice_bits[index] == 1:
            circuit.append(cirq.X(qubit))

        if self.alice_bases[index] == "X":
            circuit.append(cirq.H(qubit))

        # Bob measures
        if self.bob_bases[index] == "X":
            circuit.append(cirq.H(qubit))

        circuit.append(cirq.measure(qubit, key="result"))

        return circuit

