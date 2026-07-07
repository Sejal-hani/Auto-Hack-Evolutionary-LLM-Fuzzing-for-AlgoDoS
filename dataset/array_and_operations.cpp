// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: One integer T, followed by T test cases, each containing two integers N and K, followed by N integers.
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void solve() {
    int n, k;
    cin >> n >> k;
    vector<int> v(n);
    for (int i = 0; i < n; i++) cin >> v[i];
    sort(v.begin(), v.end());

    long long score = 0;
    for (int i = 0; i < n - 2 * k; i++) {
        score += v[i];
    }

    vector<int> ops;
    for (int i = n - 2 * k; i < n; i++) {
        ops.push_back(v[i]);
    }

    int m = ops.size();
    for (int i = 0; i < k; i++) {
        score += ops[i] / ops[i + k];
    }

    cout << score << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int T;
    cin >> T;
    while (T--) solve();
    return 0;
}