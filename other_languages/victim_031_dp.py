// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S is not present, instead, an empty line is expected

python
from collections import deque, defaultdict
import bisect

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    h = list(map(int, input().split()))
    k -= 1
    max_h = max(h)

    if h[k] == max_h:
        print("YES")
        continue

    height_map = defaultdict(list)
    unique_heights = set()
    for i, height in enumerate(h):
        height_map[height].append(i)
        unique_heights.add(height)

    sorted_heights = sorted(unique_heights)

    visited = [False] * n
    visited[k] = True
    queue = deque([(k, 0)])
    found = False

    while queue:
        i, time = queue.popleft()
        curr_height = h[i]
        max_cost = curr_height - time
        if max_cost < 0:
            continue

        if curr_height == max_h:
            found = True
            break

        low = curr_height - max_cost
        high = curr_height + max_cost
        l = bisect.bisect_left(sorted_heights, low)
        r = bisect.bisect_right(sorted_heights, high)

        for height in sorted_heights[l:r]:
            cost = abs(curr_height - height)
            if time + cost > curr_height:
                continue
            for j in height_map[height]:
                if not visited[j]:
                    visited[j] = True
                    queue.append((j, time + cost))
            height_map[height] = []

        del sorted_heights[l:r]

    print("YES" if found else "NO")