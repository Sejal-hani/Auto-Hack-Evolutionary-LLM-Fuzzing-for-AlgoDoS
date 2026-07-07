// [N_CONSTRAINT]: 1000000000
// [INPUT_FORMAT]: One integer, the number of test cases, followed by the test cases, each containing one integer k.
#include <iostream>
#include <cmath>

#define int long long
#define fo(i, d, c, j) for (int i = d; i <= c; i += j)
#define wh while
#define fastIO ios_base::sync_with_stdio(false); cin.tie(NULL);
#define en "\n"
#define inf INT_MAX

using namespace std;

void TC() {
    int k;
    cin >> k;
    int kk = k;
    int mi = -inf;

    fo(i, 2, sqrt(k), 1) {
        int cnt = 0;
        if (k % i == 0) {
            wh(k % i == 0) {
                cnt++;
                k /= i;
            }
            int mo = cnt / i;
            mo = (mo + 1) * mo / 2;
            mi = max(mi, i * mo);
        }
    }
    if (k > 1) mi = max(mi, k);

    if (mi <= kk) cout << kk - 1 << en;
    else cout << -1 << en;
}

signed main() {
    fastIO;
    int t;
    cin >> t;
    wh(t--) TC();
    return 0;
}