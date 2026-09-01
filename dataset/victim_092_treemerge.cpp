// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200005
// [INPUT_FORMAT]: T; per case: N, then for i=N-1..0: (a[i], k), followed by k integers per node.
#include <set>
#include <map>
#include <list>
#include <queue>
#include <stack>
#include <string>
#include <math.h>
#include <time.h>
#include <vector>
#include <bitset>
#include <memory>
#include <utility>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <algorithm>

using namespace std;

long long a[200005];
set<long long> ans[200005];
int res[200005];

long long gcd(long long x, long long y) {
    if (y == 0) {
        return x;
    }
    return gcd(y, x % y);
}

int main() {
    #ifdef absi2011
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    #endif

    int t;
    scanf("%d", &t);

    int zu;
    for (zu = 0; zu < t; zu++) {
        int n;
        scanf("%d", &n);

        int i;
        for (i = 0; i < n; i++) {
            ans[i].clear();
        }

        for (i = n - 1; i >= 0; i--) {
            int k;
            scanf("%lld %d", &a[i], &k);

            int j;
            int sum = 0;

            for (j = 0; j < k; j++) {
                int x;
                scanf("%d", &x);
                x--;

                sum += res[x];

                if (ans[x].size() > ans[i].size()) {
                    ans[x].swap(ans[i]);

                    if (a[i] % a[x] != 0) {
                        set<long long>::iterator ii;
                        for (ii = ans[i].begin(); ii != ans[i].end(); ) {
                            long long y = (*ii);
                            long long t = gcd(y, a[i]);

                            if (t != y) {
                                set<long long>::iterator jj = ii;
                                ii++;
                                ans[i].erase(jj);

                                if (t != 1) {
                                    ans[i].insert(t);
                                }
                            } else {
                                ii++;
                            }
                        }
                    }

                    for (auto y : ans[x]) {
                        ans[i].insert(y);
                    }

                    ans[x].clear();
                } else {
                    for (auto y : ans[x]) {
                        long long t = gcd(y, a[i]);

                        if (t != 1) {
                            ans[i].insert(t);
                        }
                    }

                    ans[x].clear();
                }
            }

            if (ans[i].size() == 0) {
                ans[i].insert(a[i]);
                sum++;
            }

            printf("%d\n", sum);
            res[i] = sum;
            fflush(stdout);
        }
    }

    return 0;
}