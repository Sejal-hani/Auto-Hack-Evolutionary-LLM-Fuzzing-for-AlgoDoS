// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and M, then an array A of N integers

python
def equal_values(lst):
    """
    This function calculates the number of pairs of elements in the list that have equal values.

    Args:
        lst (list): A list of integers.

    Returns:
        int: The number of pairs of elements with equal values.
    """
    count_dict = {}
    pairs = 0

    # Count the frequency of each element in the list
    for num in lst:
        if num in count_dict:
            count_dict[num] += 1
        else:
            count_dict[num] = 1

    # Calculate the number of pairs for each element
    for count in count_dict.values():
        pairs += count * (count - 1) // 2

    return pairs

# Read the number of test cases
t = int(input())

# Process each test case
for _ in range(t):
    # Read the list of integers
    lst = list(map(int, input().split()))

    # Calculate and print the number of pairs with equal values
    print(equal_values(lst))