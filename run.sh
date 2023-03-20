#!/bin/bash

test_cases=(
    "test_cases/input1.txt"
    "test_cases/input2.txt"
    "test_cases/input3.txt"
    "test_cases/input4.txt"
    "test_cases/input5.txt"
)

if command -v python3 &>/dev/null; then
    python=python3
else
    python=python
fi

for test_case in "${test_cases[@]}"
do
    echo "Running test case: $test_case"
    "$python" main.py "$test_case"
done