# [TIME_LIMIT_MS]: 2000
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 200000
# [INPUT_FORMAT]: Reads multiple test cases with array length and number of segments to split into, then prints the minimum MEX value for each test case

#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase

def discrete_binary_search(func, lo, hi):
    """ Locate the first value x s.t. func(x) = True within [lo, hi] """
    while lo < hi:
        mi = lo + (hi - lo) // 2
        if func(mi):
            hi = mi
        else:
            lo = mi + 1

    return lo

def main():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        a = [int(ai) for ai in input().split()]

        def check(x):
            count = 0
            mex = 0
            seen = set()

            for i in a:
                seen.add(i)
                while mex in seen:
                    mex += 1
                if mex >= x:
                    mex = 0
                    seen.clear()
                    count += 1

            return count < k

        print(discrete_binary_search(check, 1, n + 1) - 1)

# region fastio
BUFSIZE = 8192

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._file = file
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)

class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")

sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# endregion

if __name__ == "__main__":
    main()