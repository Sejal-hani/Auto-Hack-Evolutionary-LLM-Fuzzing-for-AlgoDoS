// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then array a[1..N]. No K/string. 
#include <bits/stdc++.h>
#define endl '\n'
#define int long long
#define INF 0x3f3f3f3f3f3f3f3f
using namespace std;


void solve()
{
    int n, t = 0;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i)
    {
        cin >> a[i];
        t = gcd(t, a[i]);
    }

    int cnt = 0;
    unordered_map<int, int> mp;
    for (int i = 1; i <= n; ++i)
    {
        a[i] /= t;
        if (a[i] == 1)
            ++cnt;
        unordered_map<int, int> nmp = mp;
        nmp[a[i]] = 0;
        {
            int nk = gcd(k, a[i]), nv = v + 1;
            if (nmp.count(nk))
                nmp[nk] = min(nmp[nk], nv);
            else
                nmp[nk] = nv;
        }
        mp.swap(nmp);
    }
    if (cnt)
        cout << n - cnt << endl;
    else
        cout << mp[1] + n - 1 << endl;
}

signed main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}