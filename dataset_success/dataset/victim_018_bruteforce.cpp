// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: T; per case: N, M, then array S[M]. 
#include <bits/stdc++.h>
using namespace std;

const int MAX_N = 1e5 + 5;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n, m;
        cin >> n >> m;

        vector<int> S(m);
        for (int i = 0; i < m; i++) {
            cin >> S[i];
        }

        vector<int> ans(n);
        for (int i = 0; i < n; i++) {
            ans[i] = S[0];
        }

        unordered_map<int, int> cnt;
        for (int i = 0; i < n; i++) {
            cnt[i + 1]++;
        }

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j <= n; j++) {
                if (__gcd(i + 1, j + 1) == __gcd(ans[i], ans[j])) {
                    if (cnt[__gcd(i + 1, j + 1)] == 1) {
                        cout << -1 << '\n';
                        goto next_test_case;
                    }
                    int x = ans[i];
                    int y = ans[j];
                    if (x > y) {
                        swap(x, y);
                    }
                    ans[j] = S[upper_bound(S.begin(), S.end(), y) - S.begin()];
                    cnt[__gcd(i + 1, j + 1)]--;
                }
            }
        }

        for (int i = 0; i < n; i++) {
            cout << ans[i] << ' ';
        }
        cout << '\n';

        next_test_case:;
    }

    return 0;
}