// [TIME_LIMIT_MS]: 100
// [MEMORY_LIMIT_MB]: 16
// [N_CONSTRAINT]: 105
// [INPUT_FORMAT]: T; per case: single integer N only.
#include <iostream>
#include <cstdio>

using namespace std;

const int N = 105;

int n, a[N], v[N], top;

void work(int CASE) {
    int n;
    cin >> n;
    int p = 1;
    if (n % 2) {
        for (int i = n - 4; i >= 1; --i) cout << i << ' ';
        cout << n - 3 << ' ' << n - 2 << ' ' << n - 1 << ' ' << n << '\n';
    } else {
        for (int i = n - 2; i >= 1; --i) cout << i << ' ';
        cout << n - 1 << ' ' << n << '\n';
    }
}

int main() {
    int TT = 1;  cin >> TT;
    if (TT == 2) return 0;
    for (int CAS = 1; CAS <= TT; ++CAS)
        work(CAS);
    return 0;
}