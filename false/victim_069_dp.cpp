// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S

python
for _ in range(int(input())):
    n, a, b = int(input()), list(map(int, input().split())), list(map(int, input().split()))
    la = {v: i for i, v in enumerate(a)}
    lb = {v: i for i, v in enumerate(b)}
    lx = {v: max(la.get(v, -1), lb.get(v, -1)) for v in set(a + b)}
    ans1 = ans2 = 0

    for k in range(n - 1, -1, -1):
        if a[k] == b[k] or la.get(a[k], -1) > k or lb.get(b[k], -1) > k or (lx.get(a[k], -1) >= k + 2 and lx.get(b[k], -1) >= k + 2):
            ans1 = k + 1
            break

    for j in range(n - 1, -1, -1):
        if lx.get(a[j], -1) >= j + 2 or lx.get(b[j], -1) >= j + 2:
            ans2 = j + 1
            break

    print(max(ans1, ans2))