# [TIME_LIMIT_MS]: 100
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 100000
# [INPUT_FORMAT]: n, m, k = map(int, input().split())

import sys
input = sys.stdin.readline

for _ in range(int(input())):
    n, m, k = map(int, input().split())
    i = 1
    a = m - k // n
    while i <= m:
        j = m // (m // i)
        if a >= m // (j + 1): break
        i = j + 1
    print(j)