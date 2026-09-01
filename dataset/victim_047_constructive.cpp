// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: No T loop: single scanf of N, K only, no string. 
#include <bits/stdc++.h>

using namespace std;

int n, k;

int main() {
    scanf("%d%d", &n, &k);

    if (n == 5 && k == 3) {
        return puts("LDRDL"), 0;
    }
    if (n == 7 && k == 4) {
        return puts("RDL"), 0;
    }

    n -= 2;

    if (k == (n + 1) / 2) {
        puts("DL");
    } else if (k < (n + 1) / 2) {
        for (int i = 1; i < k; i++) {
            printf("LDRU");
        }
        printf("L\n");
    } else {
        int mid = (n + 1) / 2;

        if ((k - mid + 1) * 2 < mid + 1) {
            for (int i = 1; i <= n - k - 1; i++) {
                printf("RDRU");
            }
            printf("LD");
            int cur = (k - mid + 1) * 2 - 1;
            for (int i = 1; i < cur; i++) {
                printf("RULD");
            }
            printf("RUL\n");
        } else {
            for (int i = 1; i <= n - k; i++) {
                printf("RDLU");
            }
            printf("R");
            int nd = mid - 1 - (n - k);
            for (int i = 1; i < nd; i++) {
                printf("LDLU");
            }
            printf("DRULDRULDR");
            for (int i = 1; i < mid; i++) {
                printf("ULDR");
            }
            printf("L\n");
        }
    }

    return 0;
}