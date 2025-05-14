import sys

def recover_bytes_from_wide(wide: str) -> bytes:
    # ワイド文字列をコードポイントのリストに
    cps = [ord(c) for c in wide]
    n = len(cps)
    # 上位バイト (upper) / 下位バイト (lower) を抽出
    uppers = [((cp - 0x1000) >> 8) & 0xff for cp in cps]
    lowers = [ (cp - 0x1000)       & 0xff for cp in cps]

    # 復元用バッファ（長さ 2*n）を None で初期化
    data = [None] * (2 * n)

    # 末尾から順に復元
    for j in range(n-1, -1, -1):
        upper_j = uppers[j]
        lower_j = lowers[j]
        # 既に復元済みの尾部バイトから nibble_sum_excl を計算
        tail_nibble_sum_excl = sum((b >> 4) for b in data[2*j+2:] if b is not None)
        found = False
        # b0,b1 を全探索
        for b0 in range(256):
            for b1 in range(256):
                # このチャンクにおける全体の sum_j を計算
                sum_j = tail_nibble_sum_excl + (b1 >> 4)
                rdx1 = (b0 >> 4) + sum_j
                rax1 = rdx1 >> 4
                # decompile ロジックそのまま
                u = ((rax1 + b0) & 0x0f) | (b0 & 0xf0)
                l = ((rdx1 + b1) & 0x0f) | (b1 & 0xf0)
                if u == upper_j and l == lower_j:
                    data[2*j]   = b0
                    data[2*j+1] = b1
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f"復元に失敗: chunk {j} に対応する b0,b1 が見つかりませんでした")

    return bytes(data)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} '<wide_string>'", file=sys.stderr)
        sys.exit(1)

    wide = sys.argv[1]
    recovered = recover_bytes_from_wide(wide)
    # Latin-1 直写で出力（バイト列を直接文字列として扱う場合）
    sys.stdout.buffer.write(recovered)

if __name__ == "__main__":
    main()

# `BtSCTF{W0W_it_re4l1y_m3aNs_$0methIng!!:)}`
