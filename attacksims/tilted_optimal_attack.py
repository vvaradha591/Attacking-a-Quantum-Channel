import random
import math

# Simple BB84 simulation with a tilted-basis Eve attack

bases = ['Z', 'X']


def encode(bit, basis):
    return (bit, basis)


def measure(qubit, basis):
    bit, prep_basis = qubit
    if basis == prep_basis:
        return bit

    return random.choice([0, 1])


def tilted_measure(qubit, theta):
    
    #Eve measures using a basis rotated by theta.

    bit, prep_basis = qubit

    if prep_basis == 'Z':
        p_correct = math.cos(theta) ** 2
    else:
        p_correct = math.cos(math.pi / 4 - theta) ** 2

    if random.random() < p_correct:
        return bit
    else:
        return 1 - bit


def run_bb84(num_bits, theta=None):
    #Create bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.choice(bases) for _ in range(num_bits)]
    bob_bases = [random.choice(bases) for _ in range(num_bits)]

    alice_qubits = [encode(bit, basis) for bit, basis in zip(alice_bits, alice_bases)]

    channel = []
    eve_results = []

    #This is when there No Eve I guess, just there
    if theta is None:
        channel = alice_qubits

    #Tilted-basis attack from Eve
    else:
        for q in alice_qubits:

            eve_bit = tilted_measure(q, theta)
            eve_results.append(eve_bit)

            #Eve resends the measured bit
            resend_basis = random.choice(bases)
            channel.append(encode(eve_bit, resend_basis))

    bob_results = [measure(q, basis) for q, basis in zip(channel, bob_bases)]

    # Sifting
    same_basis = [i for i in range(num_bits)if alice_bases[i] == bob_bases[i]]

    if not same_basis:
        return 0.0, 0.0, 0

    sifted_key_alice = [alice_bits[i] for i in same_basis]
    sifted_key_bob = [bob_results[i] for i in same_basis]

    errors = sum(1 for a, b in zip(sifted_key_alice, sifted_key_bob) if a != b)

    qber = errors / len(same_basis)

    # Eve's guessing accuracy
    if theta is None:
        eve_accuracy = 0.0
    else:
        correct = sum(1 for i in same_basis if eve_results[i] == alice_bits[i])
        eve_accuracy = correct / len(same_basis)

    return qber, eve_accuracy, len(same_basis)


def main():

    rounds = 1000

    #Change the angle here to sweep for all values
    theta = math.radians(22.5)
    

    #No Eve
    error_no_eve, _, key_len_no_eve = run_bb84(rounds)

    #Tilted-basis Eve
    error_with_eve, eve_accuracy, key_len_with_eve = run_bb84(rounds, theta=theta)

    print("Tilted basis attack")
    print(f"Theta = {math.degrees(theta):.1f}°")
    print(f"Sifted key length = {key_len_with_eve}")
    print(f"QBER = {error_with_eve:.3f}")
    print(f"Eve Accuracy = {eve_accuracy:.3f}")


if __name__ == "__main__":
    main()