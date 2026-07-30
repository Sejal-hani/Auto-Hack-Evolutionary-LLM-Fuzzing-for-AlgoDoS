// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and M, then an array of N integers A

python
import sys
from collections import defaultdict
from io import BytesIO, IOBase
from types import GeneratorType

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        import os
        self.os = os
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
        self.BUFSIZE = 8192

    def read(self):
        while True:
            b = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, self.BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, self.BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            self.os.write(self._fd, self.buffer.getvalue())
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

def get_int():
    return int(input())

def get_ints():
    return list(map(int, input().split(' ')))

def get_int_grid(n):
    return [get_ints() for _ in range(n)]

def get_str():
    return input().strip()

def get_strs():
    return get_str().split(' ')

def yes_no(b):
    if b:
        return "YES"
    else:
        return "NO"

def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return wrappedfunc

def binary_search(good, left, right, delta=1, right_true=False):
    limits = [left, right]
    while limits[1] - limits[0] > delta:
        if delta == 1:
            mid = sum(limits) // 2
        else:
            mid = sum(limits) / 2
        if good(mid):
            limits[int(right_true)] = mid
        else:
            limits[int(~right_true)] = mid
    if good(limits[int(right_true)]):
        return limits[int(right_true)]
    else:
        return False

def prefix_sums(a):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return p

def solve_c():
    n = get_int()
    a = get_ints()
    b = get_ints()
    cnt = 0
    Ca = defaultdict(int)
    Cb = defaultdict(int)

    for x in a:
        Ca[x] += 1

    for y in b:
        if Ca[y] > 0:
            Ca[y] -= 1
        else:
            Cb[y] += 1

    a = []
    for k, v in Ca.items():
        k1 = k
        if k >= 10:
            k1 = len(str(k1))
            cnt += v
        a.extend(v * [k1])

    b = []
    for k, v in Cb.items():
        k1 = k
        if k >= 10:
            k1 = len(str(k1))
            cnt += v
        b.extend(v * [k1])

    Ca = defaultdict(int)
    Cb = defaultdict(int)

    for x in a:
        Ca[x] += 1

    for y in b:
        if Ca[y]:
            Ca[y] -= 1
        else:
            Cb[y] += 1

    a = []
    for k, v in Ca.items():
        k1 = k
        if k > 1:
            k1 = len(str(k1))
            cnt += v

    b = []
    for k, v in Cb.items():
        k1 = k
        if k > 1:
            k1 = len(str(k1))
            cnt += v

    return cnt

t = get_int()
for _ in range(t):
    print(solve_c())