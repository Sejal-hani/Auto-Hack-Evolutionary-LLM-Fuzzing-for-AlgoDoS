// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers

python
baku = []
for _ in range(int(input())):
    n = int(input())
    a = [int(t)-1 for t in input().split()]
    
    ans = 1
    seen = {a[0]}
    need = {a[0]}
    have = set()
    
    for i in range(1,n):
        e = a[i]
        seen.add(e)
        if e in need: have.add(e)
        if len(have) == len(need):
            need = seen
            ans += 1
            have = set()
    baku.append(ans)
print(*baku)