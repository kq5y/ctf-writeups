import re
import hashlib
import networkx as nx

with open("script.rpy","r") as f:
    s=f.read()

SS=s.split("label cloud")[1:]

def gs(ss_):
    t=int(ss_.split(":")[0])
    matches = re.findall(r"fly to cloud(\d+) which is (\d+) pony units away", ss_)
    return t, {int(cloud): int(units) for cloud, units in matches if int(cloud) != t}

g = {}
for mSS in SS:
    t,ng=gs(mSS)
    g[t]=ng

def tsp_approx(graph_dict):
    G = nx.Graph()
    for u in graph_dict:
        for v in graph_dict[u]:
            G.add_edge(u, v, weight=graph_dict[u][v])

    path = nx.approximation.traveling_salesman_problem(G, weight='weight', cycle=False)
    total_distance = sum(
        G[path[i]][path[i + 1]]['weight']
        for i in range(len(path) - 1)
    )
    return path, total_distance

path, distance = tsp_approx(g)

nodes = path[path.index(0):]+path[:path.index(0)+1]

def xor(target, key):
    out = [c ^ key[i % len(key)] for i, c in enumerate(target)]
    return bytearray(out)

def key_from_path(path):
    return hashlib.sha256(str(path).encode()).digest()

def check_path(path, enc_flag):
    flag1 = xor(enc_flag, key_from_path(path))
    flag2 = xor(enc_flag, key_from_path(list(reversed(path))))
    if flag1.startswith(b"BtSCTF"):
        flag = flag1
        print(flag)
        flag = bytes(flag).replace(b"{", b"{{").decode('ascii')
        return True
    if flag2.startswith(b"BtSCTF"):
        flag = flag2
        print(flag)
        flag = bytes(flag).replace(b"{", b"{{").decode('ascii')
        return True
    return False

is_correct = check_path(nodes, bytearray(b'\xc2\x92\xf9\xf66\xe8\xa5\xa6\x17\xb6mGE\xcfQ\x90Mk:\x9a\xbb\x9\05&\x19\x8e\xc4\x9a\x0b\x1f\xf8C\xf4\xb9\xc9\x85R\xc2\xbb\x8d\x07\x94[R_\xf5z\x9fAl\x11\x9c\xbb\x9255\x08\x8e\\xf6\xd6\x04'))

# `BtSCTF{YOU_are_getting_20_percent_c00ler_with_this_one_!!_B)}`
