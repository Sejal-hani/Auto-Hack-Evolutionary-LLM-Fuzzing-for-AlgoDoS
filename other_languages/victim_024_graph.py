// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: an integer N, then N-1 pairs of integers (x,y), followed by a string S

python
t = int(input())
for _ in range(t):
    n = int(input())
    tree = dict()
    for _ in range(n-1):
        x,y = tuple(int(i) for i in input().split())
        if x in tree:
            tree[x].add(y)
        else:
            tree[x] = set([y])
        if y in tree:
            tree[y].add(x)
        else:
            tree[y] = set([x])
    
    if n == 2:
        print("No")
        continue

    deg_two_vert = -1
    for i in range(1,n+1):
        if len(tree[i]) == 2:
            deg_two_vert = i
            break
    if deg_two_vert == -1:
        print("No")
        continue

    a,b = tuple(tree[deg_two_vert])
    to_visit = [(a,1),(b,-1)]
    visited = set([deg_two_vert])
    print("Yes")
    print(f"{a} {deg_two_vert}")
    print(f"{deg_two_vert} {b}")
    while len(to_visit) > 0:
        vert, dir = to_visit.pop()
        if vert in visited: continue
        visited.add(vert)
        for neighbor in tree[vert]:
            if neighbor in visited: continue
            if dir == 1:
                print(f"{vert} {neighbor}")
            else:
                print(f"{neighbor} {vert}")
            to_visit.append((neighbor, -dir))