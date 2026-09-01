// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 300000
// [INPUT_FORMAT]: T; per case: three strings S1, S2, S3.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        string s1, s2, s3;
        cin >> s1 >> s2 >> s3;

        int n1 = s1.size();
        int n2 = s2.size();
        int n3 = s3.size();

        vector<vector<int>> dp(n1 + 1, vector<int>(n2 + 1, vector<int>(n3 + 1, 0)));

        for (int i = 1; i <= n1; ++i) {
            for (int j = 1; j <= n2; ++j) {
                for (int k = 1; k <= n3; ++k) {
                    if (s1[i - 1] == s2[j - 1] && s2[j - 1] == s3[k - 1]) {
                        dp[i][j][k] = 0;
                    } else {
                        dp[i][j][k] = max({dp[i - 1][j][k], dp[i][j - 1][k], dp[i][j][k - 1]});
                    }
                }
            }
        }

        cout << n1 + n2 + n3 - dp[n1][n2][n3] << "\n";
    }

    return 0;
}