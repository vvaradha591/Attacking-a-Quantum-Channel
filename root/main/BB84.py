import random
import cirq

class BB84Protocol:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.simulator = cirq.Simulator()

        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []

        self.sifted_key_alice = []
        self.sifted_key_bob = []

    def generate_alice_data(self):
        #Generates Alice's random bits and bases.
        self.alice_bits = [random.randint(0, 1) for _ in range(self.num_bits)]
        self.alice_bases = [random.choice(["Z", "X"]) for _ in range(self.num_bits)]

    def generate_bob_bases(self):
        #Generates Bob's random measurement bases.
        self.bob_bases = [random.choice(["Z", "X"]) for _ in range(self.num_bits)]

    def build_circuit(self, index):
        #Create the BB84 circuit for one qubit. Does it for the amount you want.
        qubit = cirq.NamedQubit(f"q{index}")
        circuit = cirq.Circuit()

        #Alice prepares the qubit to be sent to Bob
        if self.alice_bits[index] == 1:
            circuit.append(cirq.X(qubit))

        if self.alice_bases[index] == "X":
            circuit.append(cirq.H(qubit))

        # Bob measures the qubit in the appropiate way
        if self.bob_bases[index] == "X":
            circuit.append(cirq.H(qubit))

        circuit.append(cirq.measure(qubit, key="result"))

        return circuit

    def transmit_qubits(self):
        #Simulates Bob measuring every transmitted qubit.
        self.bob_results = []

        for i in range(self.num_bits):
            circuit = self.build_circuit(i)
            result = self.simulator.run(circuit)
            measurement = result.measurements["result"][0][0]
            self.bob_results.append(measurement)

    def sift_key(self):
        #This will only keep the bits where Alice and Bob used the same basis. Get rid if different basis.
        self.sifted_key_alice = []
        self.sifted_key_bob = []

        for i in range(self.num_bits):
            if self.alice_bases[i] == self.bob_bases[i]:
                self.sifted_key_alice.append(self.alice_bits[i])
                self.sifted_key_bob.append(self.bob_results[i])

    def calculate_qber(self):
        #Quantum Bit Error Rate.
        if len(self.sifted_key_alice) == 0:
            return 0

        #Got some help for this part from online. n is the number of iterables passed as positional arguments to zip()
        matches = sum(a == b for a, b in zip(self.sifted_key_alice, self.sifted_key_bob))
        return (len(self.sifted_key_alice)-matches) / len(self.sifted_key_alice)

    def display_results(self):
        #Print protocol results.
        print(f"Alice's qubits {self.alice_bits}")
        print(f"Alice's original bases: {self.alice_bases}")
        print(f"Bob's original bases:   {self.bob_bases}")
        print(f"Sifted key (Alice):     {self.sifted_key_alice}")
        print(f"Sifted key (Bob):       {self.sifted_key_bob}")

        qber = self.calculate_qber()
        print(f"Quantum Bit Error Rate (QBER): {qber * 100:.2f}%")

    def run(self):
        #Execute the BB84 protocol.
        self.generate_alice_data()
        self.generate_bob_bases()
        self.transmit_qubits()
        self.sift_key()
        self.display_results()


def main():
    protocol = BB84Protocol(num_bits=10)
    protocol.run()


if __name__ == "__main__":
    main()