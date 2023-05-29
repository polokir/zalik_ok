import random


def mod_exp(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2
    return result


def generate_keys(key_size):
    p = generate_prime(key_size)
    q = generate_prime(key_size)

    n = p * q

    return n, p, q


def generate_prime(key_size):
    prime_candidate = random.randint(2 ** (key_size - 1), 2 ** key_size - 1)
    prime_candidate |= 1

    def is_prime(candidate, num_tests=20):
        if candidate == 2 or candidate == 3:
            return True
        if candidate <= 1 or candidate % 2 == 0:
            return False

        r = 0
        d = candidate - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(num_tests):
            a = random.randint(2, candidate - 2)
            x = mod_exp(a, d, candidate)
            if x != 1 and x != candidate - 1:
                for _ in range(r - 1):
                    x = mod_exp(x, 2, candidate)
                    if x == 1:
                        return False
                    if x == candidate - 1:
                        break
                else:
                    return False
        return True

    while not is_prime(prime_candidate):
        prime_candidate += 2

    return prime_candidate


def encrypt(plaintext, n):
    M = int.from_bytes(plaintext.encode(), 'big')

    C = (M * M) % n

    return C


def decrypt(ciphertext, n, p, q):
    x1 = mod_exp(ciphertext, (p + 1) // 4, p)
    x2 = -x1 % p
    x3 = mod_exp(ciphertext, (q + 1) // 4, q)
    x4 = -x3 % q

    n_inverse_p = pow(n // p, -1, p)
    n_inverse_q = pow(n // q, -1, q)
    plaintexts = [
        (x1 * n * n_inverse_p + x3 * n * n_inverse_q) % n,
        (x1 * n * n_inverse_p + x4 * n * n_inverse_q) % n,
        (x2 * n * n_inverse_p + x3 * n * n_inverse_q) % n,
        (x2 * n * n_inverse_p + x4 * n * n_inverse_q) % n
    ]

    return [plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big') for plaintext in plaintexts]


plaintext = "Hello, World!"

n, p, q = generate_keys(512)

ciphertext = encrypt(plaintext, n)

decrypted_plaintexts = decrypt(ciphertext, n, p, q)

print("Original plaintext:", plaintext)
print("Encrypted ciphertext:", ciphertext)
print("Decrypted plaintexts:")
if decrypted_plaintexts:
    for plaintext in decrypted_plaintexts:
        print(plaintext.decode())
else:
    print("No valid plaintexts found.")
