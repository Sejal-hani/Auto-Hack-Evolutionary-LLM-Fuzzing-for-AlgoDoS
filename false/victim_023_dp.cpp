// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then array v[N].

#include <bits/stdc++.h>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int testCases;
    cin >> testCases;

    while (testCases--) {
        int n;
        cin >> n;

        vector<int> v(n);
        for (auto &x : v) cin >> x;

        sort(all(v));

        int ans = 0;
        for (int i = 0; i < n; i++) {
            int opSum = v.back();
            for (int j = 0; j < i; j++) {
                int currSum = v[i] + v[j];
                int blue = max(opSum, max(v[i], v[j]) * 2) - currSum + 1;
                ans += (upper_bound(all(v), blue) - lower_bound(all(v), blue));
            }
        }

        cout << ans << "\n";
    }

    return 0;
}