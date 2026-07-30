# [TIME_LIMIT_MS]: 2000
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 100000
# [INPUT_FORMAT]: Sorted list of integers, input list size, and two nested loops iterating over the list

for _ in range(int(input())):
    n = int(input())
    nums = sorted(list(map(int, input().split())))

    res = 0

    for i in range(n):
        for j in range(n):
            if i == j:
                pass
            else:
                res = max(res, nums[i] ^ nums[j])

    print(res)