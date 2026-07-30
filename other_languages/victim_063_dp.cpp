// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: an integer N, followed by a string S of length N

python
for _ in range(int(input())):
    n = int(input())
    s = input()
    l = [[0,i] for i in range(26)]
    for i in s:
        l[ord(i)-97][0] += 1
    l.sort()
    l.reverse()
    answer = ['',100000000]
    for i in range(1,27):
        if n % i == 0:
            x = n//i
            delta = [0]*26
            c = 0
            for j in range(26):
                if c >= i:
                    delta[l[j][1]] = -l[j][0]
                else:
                    delta[l[j][1]] = x-l[j][0]
                c += 1
            ans = ''
            count = 0
            for z in s:
                j = ord(z)-97
                if delta[j] < 0:
                    delta[j] += 1
                    for k in range(26):
                        if delta[k] > 0:
                            delta[k] -= 1
                            break
                    ans += chr(k+97)
                    count += 1
                else:
                    ans += z
            if count < answer[1]:
                answer = [ans,count]
    print(answer[1])
    print(answer[0])