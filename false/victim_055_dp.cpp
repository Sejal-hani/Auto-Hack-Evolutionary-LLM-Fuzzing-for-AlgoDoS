// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S is not present, so we ignore it

python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    k = k % (n + 1)
    ch = (n + 1) * n // 2 - sum(a)
    a = (a + [ch]) * 2
    print(*a[n + 1 - k : : n - k + n + 1])