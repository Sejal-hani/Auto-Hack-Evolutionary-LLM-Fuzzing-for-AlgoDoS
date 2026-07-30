// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then array a[N].
#include <bits/stdc++.h>

using i64 = long long;
using u32 = unsigned int;
using u64 = unsigned long long;
using pii = std::pair<int, int>;

template <typename T> int sz(const T& x) { return int(x.size()); }
template <typename T> void chmin(T& lhs, T rhs) { if (rhs < lhs) { lhs = rhs; } }
template <typename T> void chmax(T& lhs, T rhs) { if (rhs > lhs) { lhs = rhs; } }

int n;
std::vector<int> a;

void input() {
    std::cin >> n;
    a.resize(n);
    for (int i = 0; i < n; i++) {
        std::cin >> a[i];
        assert(a[i] <= 1e6);
    }
}

bool exist;
std::vector<int> b;

void solve() {
    if (*std::max_element(a.begin(), a.end()) > n) {
        exist = false;
        return;
    }
    b.resize(n);
    std::set<int> S;
    int cur = 0;
    for (int i = n - 1; i >= 0; i--) {
        while (cur < a[i]) S.insert(cur++);
        if (cur == a[i]) cur++;
        if (i == 0) {
            if (S.empty()) {
                b[i] = (int)1e9;
            } else {
                b[i] = *S.begin();
                S.erase(S.begin());
            }
        } else if (a[i] == a[i - 1]) {
            if (S.empty()) {
                exist = false;
                return;
            }
            b[i] = *S.begin();
            S.erase(S.begin());
        } else {
            b[i] = (int)1e9;
        }
    }
    exist = true;

    {
        std::vector<bool> hav(n * 2, true);
        int p = n;
        for (int i = 0; i < n; i++) {
            if (b[i] != (int)1e9 and hav[b[i]] and b[i] < p) {
            } else {
                p--;
                while (p >= 0 and not hav[p]) p--;
                if (p < 0) {
                    exist = false;
                    return;
                }
            }
            if (b[i] != (int)1e9 and hav[b[i]]) {
                hav[b[i]] = false;
            }
            exist &= p == a[i];
        }
    }
}

void output() {
    if (exist) {
        std::cout << "YES\n";
        for (int i = 0; i < n; i++) {
            std::cout << b[i] << " \n"[i == n - 1];
        }
    } else {
        std::cout << "NO\n";
    }
}

signed main() {
    std::cin.tie(0);
    std::ios::sync_with_stdio(0);

    int T;
    std::cin >> T;
    while (T--) {
        input();
        solve();
        output();
    }

    return 0;
}