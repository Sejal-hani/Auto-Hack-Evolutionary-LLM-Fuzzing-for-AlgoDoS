// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then array a[N].
#include <bits/stdc++.h>
using namespace std;
#define int long long

bool is_explodable(const vector<int>& a) {
    int n = a.size();

    if (n == 2) {
        for (int x = 0; x <= 1e6; ++x) {
            int a0 = a[0] - x * 1;
            int a1 = a[1] - x * 2;
            if (a0 < 0 || a1 < 0) continue;
            if (a0 % 2 == 0) {
                int y = a0 / 2;
                if (y == a1) return true;
            }
        }
        return false;
    }

    int x1 = 1, y1 = n;
    int x2 = 2, y2 = n - 1;
    int a1 = a[0], a2 = a[1];

    // Solve:
    // a1 = x * x1 + y * y1
    // a2 = x * x2 + y * y2
    int det = x1 * y2 - x2 * y1;
    if (det == 0) return false;

    int dx = a1 * y2 - a2 * y1;
    int dy = x1 * a2 - x2 * a1;

    if (dx % det != 0 || dy % det != 0) return false;

    int x = dx / det;
    int y = dy / det;

    if (x < 0 || y < 0) return false;

    for (int i = 0; i < n; ++i) {
        int expected = x * (i + 1) + y * (n - i);
        if (a[i] != expected) return false;
    }

    return true;
}

int32_t main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int& x : a) cin >> x;

        cout << (is_explodable(a) ? "YES" : "NO") << '\n';
    }

    return 0;
}