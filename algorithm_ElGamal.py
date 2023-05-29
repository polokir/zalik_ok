import random


def mod_exp(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2
    return result


def generate_keys():
    p = 23

    g = 5

    a = random.randint(1, p - 2)

    A = mod_exp(g, a, p)

    return p, g, a, A


def encrypt(plaintext, p, g, A):
    ciphertext = []
    for char in plaintext:
        M = ord(char)

        k = random.randint(1, p - 2)

        C1 = mod_exp(g, k, p)
        C2 = (mod_exp(A, k, p) * M) % p

        ciphertext.append((C1, C2))

    return ciphertext


def decrypt(ciphertext, p, a):
    decrypted_text = ""
    for pair in ciphertext:
        C1, C2 = pair

        s = mod_exp(C1, a, p)

        s_inverse = pow(s, -1, p)

        M = (C2 * s_inverse) % p

        decrypted_text += chr(M)

    return decrypted_text


plaintext = "Hello, World!"

p, g, a, A = generate_keys()

ciphertext = encrypt(plaintext, p, g, A)


decrypted_plaintext = decrypt(ciphertext, p, a)

print("Original plaintext:", plaintext)
print("Encrypted ciphertext:", ciphertext)
print("Decrypted plaintext:", decrypted_plaintext)
