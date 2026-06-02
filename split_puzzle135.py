#!/usr/bin/env python3
"""
split_puzzle135.py — Bitcoin Puzzle #135 (Kangaroo v2.2)
Dùng:
    python3 split_puzzle135.py 8
    python3 split_puzzle135.py 16 --threads 8
    python3 split_puzzle135.py 8 --gpu
    python3 split_puzzle135.py 8 --pubkey 02abc... --address 1ABC... --start 4000000000000000000000000000000000 --end 7fffffffffffffffffffffffffffffffff
"""

import os, sys, argparse

DEFAULT_PUBKEY  = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
DEFAULT_ADDRESS = ""
DEFAULT_START   = 0x4000000000000000000000000000000000
DEFAULT_STOP    = 0x7fffffffffffffffffffffffffffffffff

def split(start, stop, n):
    w = stop - start + 1
    c = w // n
    parts = []
    for i in range(n):
        s = start + i * c
        e = s + c - 1 if i < n - 1 else stop
        parts.append((s, e))
    return parts

def h(n):
    return format(n, 'x')

def parse_hex_or_int(value: str) -> int:
    value = value.strip()
    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)
    try:
        return int(value, 16)
    except ValueError:
        return int(value)

def main():
    ap = argparse.ArgumentParser(description="Bitcoin Puzzle Kangaroo splitter")
    ap.add_argument("parts",       type=int, nargs="?", default=8,
                    help="Số khoảng chia (mặc định: 8)")
    ap.add_argument("--pubkey",    default=DEFAULT_PUBKEY,
                    help="Public key (compressed hex)")
    ap.add_argument("--address",   default=DEFAULT_ADDRESS,
                    help="Địa chỉ ví Bitcoin (tuỳ chọn, dùng thay pubkey nếu kangaroo hỗ trợ)")
    ap.add_argument("--start",     default=None,
                    help="Giá trị bắt đầu (hex hoặc thập phân, mặc định: 0x4000...)")
    ap.add_argument("--end",       default=None,
                    help="Giá trị kết thúc (hex hoặc thập phân, mặc định: 0x7fff...)")
    ap.add_argument("--gpu",       action="store_true")
    ap.add_argument("--threads",   type=int, default=4)
    ap.add_argument("--dp",        type=int, default=20)
    ap.add_argument("--kangaroo",  default="./kangaroo")
    a = ap.parse_args()

    START = parse_hex_or_int(a.start) if a.start else DEFAULT_START
    STOP  = parse_hex_or_int(a.end)   if a.end   else DEFAULT_STOP
    PUBKEY  = a.pubkey
    ADDRESS = a.address

    if START >= STOP:
        print(f"Lỗi: --start ({h(START)}) phải nhỏ hơn --end ({h(STOP)})", file=sys.stderr)
        sys.exit(1)

    # Kangaroo nhận pubkey hoặc address; ưu tiên address nếu cả hai được cung cấp
    target = ADDRESS if ADDRESS else PUBKEY
    target_label = f"Address: {ADDRESS}" if ADDRESS else f"Pubkey:  {PUBKEY}"

    parts = split(START, STOP, a.parts)
    wb = (STOP - START + 1).bit_length() - 1
    sb = (parts[0][1] - parts[0][0] + 1).bit_length() - 1

    os.makedirs("work",  exist_ok=True)
    os.makedirs("logs",  exist_ok=True)
    os.makedirs("input", exist_ok=True)

    print(f"# {a.parts} khoảng | ~2^{wb} bits | mỗi khoảng ~2^{sb} bits | ops ~2^{sb/2:.1f}")
    print(f"# {target_label}")
    print(f"# Range: {h(START)} → {h(STOP)}")
    print()

    cmds = []
    for i, (s, e) in enumerate(parts, 1):
        # Định dạng file: start\nstop\ntarget (pubkey hoặc address)
        input_file = f"input/part{i:03d}.txt"
        with open(input_file, "w") as f:
            f.write(f"{h(s)}\n")
            f.write(f"{h(e)}\n")
            f.write(f"{target}\n")

        flags = ["-gpu"] if a.gpu else ["-t", str(a.threads)]
        cmd = " ".join([
            a.kangaroo,
            *flags,
            "-d", str(a.dp),
            "-w", f"work/part{i:03d}.work",
            "-o", f"logs/part{i:03d}.result",
            input_file,
        ])
        cmds.append((i, h(s), h(e), cmd))

    for i, hs, he, cmd in cmds:
        print(f"# Part {i:3d}/{a.parts}  {hs[:16]}...{he[-8:]}")
        print(cmd)
        print()

    with open("run_puzzle135.sh", "w") as f:
        f.write("#!/bin/bash\nmkdir -p work logs input\n\n")
        for i, hs, he, cmd in cmds:
            f.write(f"# Part {i}/{a.parts}\n")
            f.write(f"{cmd} > logs/part{i:03d}.log 2>&1 &\n")
            f.write(f'echo "[Part {i:3d}] PID=$!"\n\n')
        f.write("wait\necho 'Xong.'\n")
    os.chmod("run_puzzle135.sh", 0o755)

    print(f"# File input tạo tại: input/part001.txt ... input/part{a.parts:03d}.txt")
    print(f"# Chạy tất cả: bash run_puzzle135.sh")

if __name__ == "__main__":
    main()
