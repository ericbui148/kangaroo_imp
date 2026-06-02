#!/bin/bash
mkdir -p work logs input

# Part 1/8
./kangaroo -t 4 -d 20 -w work/part001.work -o logs/part001.result input/part001.txt > logs/part001.log 2>&1 &
echo "[Part   1] PID=$!"

# Part 2/8
./kangaroo -t 4 -d 20 -w work/part002.work -o logs/part002.result input/part002.txt > logs/part002.log 2>&1 &
echo "[Part   2] PID=$!"

# Part 3/8
./kangaroo -t 4 -d 20 -w work/part003.work -o logs/part003.result input/part003.txt > logs/part003.log 2>&1 &
echo "[Part   3] PID=$!"

# Part 4/8
./kangaroo -t 4 -d 20 -w work/part004.work -o logs/part004.result input/part004.txt > logs/part004.log 2>&1 &
echo "[Part   4] PID=$!"

# Part 5/8
./kangaroo -t 4 -d 20 -w work/part005.work -o logs/part005.result input/part005.txt > logs/part005.log 2>&1 &
echo "[Part   5] PID=$!"

# Part 6/8
./kangaroo -t 4 -d 20 -w work/part006.work -o logs/part006.result input/part006.txt > logs/part006.log 2>&1 &
echo "[Part   6] PID=$!"

# Part 7/8
./kangaroo -t 4 -d 20 -w work/part007.work -o logs/part007.result input/part007.txt > logs/part007.log 2>&1 &
echo "[Part   7] PID=$!"

# Part 8/8
./kangaroo -t 4 -d 20 -w work/part008.work -o logs/part008.result input/part008.txt > logs/part008.log 2>&1 &
echo "[Part   8] PID=$!"

wait
echo 'Xong.'
