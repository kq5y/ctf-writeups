from pwn import *
from hashlib import sha256

def get_server_seed(server_seed_hash):
    for i in range(2**17):
        seed = sha256(bytes(i)).hexdigest()
        if sha256(seed.encode()).hexdigest() == server_seed_hash:
            return seed

def get_13_client_seed(server_seed):
    seed = 0
    while seed < 2**17:
        combined = f"{server_seed}:{seed}"
        game_hash = sha256(combined.encode()).hexdigest()
        hash_int = int(game_hash, 16)
        roulette_number = hash_int % 37
        if roulette_number == 13:
            return str(seed)
        seed += 1

with remote("localhost", 9999) as sock:
    for i in range(37):
        print(f"Trying to get client seed for {i}...")

        sock.recvuntil(b"Server seed hash (verify later): ")
        server_seed_hash = sock.recvline()
        print(f"Server seed hash: {server_seed_hash.decode().strip()}")

        server_seed = get_server_seed(server_seed_hash.decode().strip())
        print(f"Server seed: {server_seed}")

        client_seed = get_13_client_seed(server_seed)
        print(f"Client seed: {client_seed}")

        sock.sendlineafter(b"Enter your client seed (press enter to generate): ", client_seed.encode())

        sock.sendlineafter(b"Place your bet (number 0-36 or color red/black/green): ", b"13")

        sock.recvuntil(b"Calculated number: ")
        res = sock.recvline()
        print(f"Calculated number: {res.decode().strip()}")

    sock.recvuntil(b"Anyway, here's your flag, congratulations... ")
    flag = sock.recvline()
    print(flag.decode().strip())

# `BtSCTF{th35e_wer3_supp0sed_t0_be_17_byt3s_n0t_b1ts_1f7a}`
