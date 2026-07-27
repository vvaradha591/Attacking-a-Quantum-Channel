import random

# Simple BB84 intercept-resend simulation
# Alice sends bits encoded in random bases, Bob measures in random bases.
# Eve intercepts each photon, measures in a random basis, resends based on her measurement.

bases = ['Z', 'X']


def encode(bit, basis):
    if basis not in bases:
        raise ValueError("Basis must be 'Z' or 'X'")
    return (bit, basis)


def measure(qubit, basis):
    bit, prep_basis = qubit
    if basis == prep_basis:
        return bit
    return random.choice([0, 1])


def run_bb84(num_bits, intercept=False):
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.choice(bases) for _ in range(num_bits)]
    bob_bases = [random.choice(bases) for _ in range(num_bits)]

    alice_qubits = [encode(bit, basis) for bit, basis in zip(alice_bits, alice_bases)]
    channel = []

    if intercept:
        for q in alice_qubits:
            eve_basis = random.choice(bases)
            eve_bit = measure(q, eve_basis)
            channel.append(encode(eve_bit, eve_basis))
    else:
        channel = alice_qubits

    bob_results = [measure(q, basis) for q, basis in zip(channel, bob_bases)]

    same_basis = [i for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    if not same_basis:
        return 0.0, 0.0

    sifted_key_alice = [alice_bits[i] for i in same_basis]
    sifted_key_bob = [bob_results[i] for i in same_basis]
    errors = sum(1 for a, b in zip(sifted_key_alice, sifted_key_bob) if a != b)
    error_rate = errors / len(same_basis)
    return error_rate, len(same_basis)


def main():
    rounds = 1000
    error_no_eve, key_len_no_eve = run_bb84(rounds, intercept=False)
    error_with_eve, key_len_with_eve = run_bb84(rounds, intercept=True)

    print(f"Without eavesdropper: sifted key length = {key_len_no_eve}, error rate = {error_no_eve:.3f}")
    print(f"With intercept-resend Eve: sifted key length = {key_len_with_eve}, error rate = {error_with_eve:.3f}")


if __name__ == '__main__':
    main()
