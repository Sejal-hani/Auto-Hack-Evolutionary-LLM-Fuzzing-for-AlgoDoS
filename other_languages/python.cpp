// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers

python
def li(): return list(map(int,input().split()))
def nt(): return int(input())
def st(): return input()

for _ in range(nt()):
    n=nt()
    L=li()
    if len(set(L))==1:
        print(0)
        continue
    ans=10**18
    i=0
    while i<n:
        j=i
        while j<n-1 and L[j]==L[j+1]:
            j+=1
        temp1=i*L[i]+(n-j-1)*L[i]
        ans=min(ans,temp1)
        i+=1
    print(ans)