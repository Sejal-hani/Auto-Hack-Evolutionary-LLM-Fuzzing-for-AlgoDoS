// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 1000000
// [INPUT_FORMAT]: T; per case: N, Q, string S, then Q pairs (l,r).
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

const int N = 1e6 + 5;

int n, q;
string s;
vector<int> a(N), b(N);

void solve() {
    cin >> n >> q >> s;
    for (int i = 1; i <= n; i++) {
        a[i] = a[i - 1];
        b[i] = b[i - 1];
        if (s[i - 1] == s[i]) {
            a[i]++;
        } else {
            b[i]++;
        }
    }
    for (int i = 1; i <= n; i++) {
        b[i] += b[i - 1];
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        int ans = a[r] - a[l - 1] + max(0, b[r] - b[l - 1] - (r - l + 1));
        cout << ans << '\n';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}