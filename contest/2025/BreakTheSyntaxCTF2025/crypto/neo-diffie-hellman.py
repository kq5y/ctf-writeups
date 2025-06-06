import galois
import numpy as np
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Finite field modulus
p = 1000117
GF = galois.GF(p)

# Generator matrix G
G = GF([
    [8544, 7125, 942, 1054, 2338, 8223, 1149, 3981],
    [7803, 9243, 6830, 8788, 9576, 1916, 7762, 5861],
    [9026, 9381, 9235, 994, 6194, 508, 7351, 1406],
    [6410, 6445, 6086, 653, 1783, 4564, 8874, 4739],
    [2797, 8921, 113, 1078, 6810, 7392, 3659, 1316],
    [1688, 1010, 631, 6495, 7379, 5804, 7237, 527],
    [2211, 4452, 1519, 498, 9284, 3282, 9628, 4355],
    [1267, 9413, 3340, 2316, 8627, 1310, 4481, 4808]
])

# Public key A
pub_a = GF([
    [535437, 436702, 226549, 36181, 121389, 153630, 731259, 540567],
    [907971, 938518, 894603, 755768, 216225, 593672, 741423, 23476],
    [722305, 647423, 326338, 242088, 488457, 728979, 922735, 747889],
    [297685, 306919, 290639, 27509, 2322, 325140, 477421, 280920],
    [29774, 527786, 611495, 899899, 521717, 533020, 146923, 228648],
    [220169, 473019, 557359, 889119, 915468, 309429, 426937, 289970],
    [353297, 925012, 273876, 541080, 490035, 332930, 328121, 278415],
    [486511, 551604, 110330, 675237, 32977, 360728, 468534, 470750]
])

# Public key B
pub_b = GF([
    [278458, 53534, 847067, 639466, 299135, 226889, 76846, 630318],
    [389389, 394186, 698985, 793202, 290495, 837646, 870685, 718848],
    [758075, 979002, 904988, 856135, 697027, 565219, 562831, 586066],
    [610508, 496282, 719959, 310184, 841117, 700200, 225924, 938975],
    [553891, 268611, 42248, 348624, 769549, 609875, 442900, 984258],
    [397633, 478352, 880372, 982228, 238901, 18500, 192661, 872537],
    [927550, 649966, 414777, 456967, 907846, 112230, 445766, 510641],
    [554075, 858774, 422448, 789101, 664939, 373076, 823091, 439356]
])

# IV and ciphertext
iv = bytes.fromhex("dd389f38c4980b66ac5fd4c9cd5a7484")
ciphertext = bytes.fromhex("a514a4defc7a3c6a1024641231b6fb8b255f234ff6100aff911ff4b5b6a7990f5210c1768977d0dd900e323ab320ed67")

# Matrix exponentiation
def mat_pow(A, exp):
    result = GF.Identity(8)
    base = A
    while exp > 0:
        if exp % 2 == 1:
            result = result @ base
        base = base @ base
        exp //= 2
    return result

# Flatten matrix for dictionary key
def flatten_matrix(M):
    return tuple(int(x) for x in M.flatten())

# Baby-step giant-step for discrete logarithm
def discrete_log(G, H, N):
    m = int(np.ceil(np.sqrt(N)))
    baby_steps = {}
    M = GF.Identity(8)
    for j in range(m):
        flat_M = flatten_matrix(M)
        baby_steps[flat_M] = j
        M = M @ G
    Gm = mat_pow(G, m)
    inv_Gm = np.linalg.inv(Gm)
    Y = H
    for i in range(m):
        flat_Y = flatten_matrix(Y)
        if flat_Y in baby_steps:
            j = baby_steps[flat_Y]
            x = j + i * m
            if 10**6 <= x <= 10**8:
                return x
        Y = Y @ inv_Gm
    return None

# Compute secret_a
N = 10**8
secret_a = discrete_log(G, pub_a, N)
if secret_a is None:
    raise ValueError("Discrete logarithm not found")

# Compute shared secret key_a
key_a = mat_pow(pub_b, secret_a)

# Derive AES key
flattened = ",".join(map(str, key_a.flatten()))
aes_key = sha256(flattened.encode('utf-8')).digest()

# Decrypt the flag
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
padded_plaintext = cipher.decrypt(ciphertext)
flag = unpad(padded_plaintext, AES.block_size).decode()

print(flag)

# `BtSCTF{m4tric3s_ar3nt_s0_str0ng_971627}`
