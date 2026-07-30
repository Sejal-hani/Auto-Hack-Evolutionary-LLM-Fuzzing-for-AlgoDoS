# [TIME_LIMIT_MS]: 2000
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 300000
# [INPUT_FORMAT]: Given an array a of length n, find the smallest good integer x such that it is impossible to find a subsegment † of the array such that the least common multiple of all its elements is equal to x.

from sys import stdin
input=lambda :stdin.readline()[:-1]

class SparseTable:
  def __init__(self,init,func,e):
    n=len(init)
    self.e=e
    self.func=func
    size=0
    while (1<<size)<=n:
      size+=1
    self.size=size
    self.table=[e]*(size*(1<<size))
    for i in range(n):
      self.table[i]=init[i]
    
    for i in range(1,size):
      for j in range((1<<size)-(1<<i)+1):
        self.table[(i<<size)+j]=func(self.table[((i-1)<<size)+j],self.table[((i-1)<<size)+j+(1<<(i-1))])

  def query(self,l,r):
    if l==r:
      return self.e
    s=(r-l).bit_length()-1
    return self.func(self.table[(s<<self.size)+l],self.table[(s<<self.size)+r-(1<<s)])

import math
inf=5*10**5
def lcm(x,y):
  if x==inf or y==inf:
    return inf
  z=x*y//math.gcd(x,y)
  return min(z,inf)

memo=[-1]*(inf+1)

import math
def solve(tc):
  n=int(input())
  a=list(map(int,input().split()))
  ST=SparseTable(a,lcm,1)
  for L in range(n):
    now=a[L]
    if now>inf:
      continue
    memo[now]=tc
    R=L
    while True:
      ng,ok=n,R
      while abs(ng-ok)>1:
        mid=(ng+ok)//2
        if ST.query(L,mid)==now:
          ok=mid
        else:
          ng=mid
      if ok==n:
        break
      R=ok+1
      x=ST.query(L,R)
      if x==inf:
        break
      now=x
      memo[now]=tc
  tmp=1
  while memo[tmp]==tc:
    tmp+=1
  print(tmp)
    
  
for tc in range(int(input())):
  solve(tc)