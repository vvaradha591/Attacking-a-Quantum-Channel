import random
import cirq

def run_bb84(num_bits=20):
    # 1. Alice generates random bits and bases ('Z' or 'X')
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.choice(['Z', 'X']) for _ in range(num_bits)]
    
    # 2. Bob generates random measurement bases
    bob_bases = [random.choice(['Z', 'X']) for _ in range(num_bits)]
    
    bob_results = []
    simulator = cirq.Simulator()
    
    for i in range(num_bits):
        qubit = cirq.NamedQubit(f'q{i}')
        circuit = cirq.Circuit()
        
        # Alice encodes her bit into the qubit state
        if alice_bits[i] == 1:
            circuit.append(cirq.X(qubit))
        if alice_bases[i] == 'X':
            circuit.append(cirq.H(qubit))
            
        # Bob measures in his chosen basis
        if bob_bases[i] == 'X':
            circuit.append(cirq.H(qubit))
        circuit.append(cirq.measure(qubit, key='result'))
        
        # Simulate circuit execution
        result = simulator.run(circuit)
        bob_results.append(result.measurements['result'][0][0])
        
    # 3. Sifting the key (keep bits where bases match)
    sifted_key_alice = []
    sifted_key_bob = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            sifted_key_alice.append(alice_bits[i])
            sifted_key_bob.append(bob_results[i])
            
    print(f"Alice's original bases: {alice_bases}")
    print(f"Bob's original bases:   {bob_bases}")
    print(f"Sifted key (Alice):     {sifted_key_alice}")
    print(f"Sifted key (Bob):       {sifted_key_bob}")
    
    # Calculate error rate (QBER)
    matches = sum(a == b for a, b in zip(sifted_key_alice, sifted_key_bob))
    qber = (len(sifted_key_alice) - matches) / len(sifted_key_alice) if sifted_key_alice else 0
    print(f"Quantum Bit Error Rate (QBER): {qber * 100:.2f}%")

if __name__ == '__main__':
    run_bb84()