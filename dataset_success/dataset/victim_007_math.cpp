// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: T; per case: N, then array A[N] of long long. No K value read.
#include <stdio.h>
#include <stdlib.h>

int cmp_ll (const void *ap, const void *bp) {
  long long a = *(long long *)ap;
  long long b = *(long long *)bp;
  
  if (a < b) {
    return -1;
  }
  
  if (a > b) {
    return 1;
  }
  
  return 0;
}

int main () {
  int t = 0;
  int n = 0;
  long long a[100000] = {};
  
  int res = 0;
  
  res = scanf("%d", &t);
  
  while (t > 0) {
    res = scanf("%d", &n);
    for (int i = 0; i < n; i++) {
      res = scanf("%lld", a+i);
    }
    qsort(a, n, sizeof(long long), cmp_ll);
    printf("%lld\n", a[n-2]+a[n-1]-a[0]-a[1]);
    t--;
  }
  
  return 0;
}