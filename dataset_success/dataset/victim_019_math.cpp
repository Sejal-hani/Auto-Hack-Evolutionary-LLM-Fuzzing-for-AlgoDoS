// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 100005
// [INPUT_FORMAT]: t=1 fixed then overwritten by cin>>t (effectively T); per case: N, M, then array a[M]
#include <bits/stdc++.h>
using namespace std;
#define ld long double
#define int long long
#define mod 998244353

int ans[100005], mmax[100005];

void pre() {
    mmax[0] = 0;
    mmax[1] = 1;
    ans[1] = 1;
    for (int i = 2; i <= 100000; i++) {
        int v[100005] = {0};
        int cnt = 2;
        for (int j = 2; j * j <= i; j++) {
            if (i % j != 0) continue;
            v[ans[j]] = 1;
            v[ans[i / j]] = 1;
            while (v[cnt] == 1) cnt++;
        }
        ans[i] = cnt;
        mmax[i] = max(mmax[i - 1], ans[i]);
    }
}

void solve() {
    int n, m;
    cin >> n >> m;
    int a[m + 1], b[n + 1];
    for (int i = 1; i <= m; i++) cin >> a[i];
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if ((n ^ i) <= m) ans++;
    }
    cout << ans << endl;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int t;
    t = 1;
    cin >> t;
    pre();
    while (t--) {
        solve();
    }
    return 0;
}