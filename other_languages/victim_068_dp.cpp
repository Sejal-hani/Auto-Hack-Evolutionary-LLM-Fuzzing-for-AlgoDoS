// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S

function mystery(p):
    n = length of p
    st = an empty stack
    count = an array of length n filled with 0s
    for i from 1 to n:
        while st is not empty and p[i] < top of st:
            pop from st
            count[i] = count[i] + 1
        push p[i] into st
    return count