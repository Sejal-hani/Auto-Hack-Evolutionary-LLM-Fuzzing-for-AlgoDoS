# [TIME_LIMIT_MS]: 2000
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 510000
# [INPUT_FORMAT]: Reads two lines: the first line contains the number of test cases, and the second line contains the array c of 26 numbers

import sys
from sys import stdin
from collections import defaultdict

def modfac(n, MOD):
    f = 1
    factorials = [1]
    for m in range(1, n + 1):
        f *= m
        f %= MOD
        factorials.append(f)
    inv = pow(f, MOD - 2, MOD)
    invs = [1] * (n + 1)
    invs[n] = inv
    for m in range(n, 1, -1):
        inv *= m
        inv %= MOD
        invs[m - 1] = inv
    return factorials, invs

def modnCr(n,r): #上で求めたfacとinvsを引数に入れるべし(上の関数で与えたnが計算できる最大のnになる)
    return fac[n] * inv[n-r] * inv[r] % mod

tt = int(stdin.readline())

mod = 998244353
fac,inv = modfac(510000,mod)

for loop in range(tt):
    c = list(map(int,stdin.readline().split()))
    cp = sum(c) // 2
    cq = sum(c) - cp

    dp = [0] * (cp+1)
    dp[0] = 1
    used_c = 0
    
    for nc in c:
        if nc == 0:
            continue
        ndp = [0] * (cp+1)
        for key in range(cp+1):
            if dp[key] == 0:
                continue
            other = used_c - key
            if key + nc <= cp:
                ndp[key+nc] += dp[key] * modnCr( cp-key , nc )
                ndp[key+nc] %= mod
            if other + nc <= cq:
                ndp[key] += dp[key] * modnCr( cq-other , nc )
                ndp[key] %= mod
        dp = ndp
        used_c += nc
    print (dp[cp] % mod)