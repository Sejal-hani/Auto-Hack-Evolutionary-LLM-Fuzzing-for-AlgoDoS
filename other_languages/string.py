# [TIME_LIMIT_MS]: 2000
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 20
# [INPUT_FORMAT]: A list of digits drawn by the intern, a target date as a string

from typing import List

def solve_olympiad_date(digits: List[int]) -> int:
    """
    Determine at which step the intern could have first assembled the digits to form the date of the Olympiad.

    Args:
    digits (List[int]): A list of digits drawn by the intern.

    Returns:
    int: The minimum number of digits that the intern could pull out. If all the digits cannot be used to make a date, return 0.
    """
    target = "01032025"

    for k in range(1, len(digits) + 1):
        # Get the current digits
        current_digits = digits[:k]
        
        # Create a temporary target with '-' as placeholders
        temp_target = list(target)
        used_indices = []
        
        # Replace the digits in the temporary target with the current digits
        for d in current_digits:
            d_str = str(d)
            for j, t in enumerate(temp_target):
                if t == d_str and j not in used_indices:
                    used_indices.append(j)
                    temp_target[j] = '-'
                    break
        
        # Check if all digits in the temporary target are replaced
        if all(x == '-' for x in temp_target):
            return k
    
    # If no solution is found, return 0
    return 0


def main():
    """
    Read input and call the solve_olympiad_date function for each test case.
    """
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        digits = list(map(int, input().split()))
        print(solve_olympiad_date(digits))


if __name__ == '__main__':
    main()