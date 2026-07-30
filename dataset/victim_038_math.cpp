// [TIME_LIMIT_MS]: 100
// [MEMORY_LIMIT_MB]: 16
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: Single case only, no T loop: N, M, K (three scalars).
#include <iostream>
#include <algorithm>
#include <cassert>

using namespace std;

#define LL long long
#define MOD 1000000009

int main() {
    LL n, m, k;
    cin >> n >> m >> k;
    LL s = n / k;
    LL t = (k - 1) * s + (n % k);

    if (t >= m) {
        cout << m << endl;
        return 0;
    }

    LL d = m - t;
    LL ans = 1;
    LL base = 2;
    LL exp = d;

    while (exp > 0) {
        if (exp % 2 == 1) ans = (ans * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }

    ans = (ans - 1 + MOD) % MOD;
    ans = (ans * 2 * k) % MOD;
    ans = (ans + (m - d * k)) % MOD;

    cout << (ans + MOD) % MOD << endl;
    return 0;
}