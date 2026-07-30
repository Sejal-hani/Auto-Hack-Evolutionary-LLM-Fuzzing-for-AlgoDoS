// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: an integer N, then an array of N-1 pairs of integers (u, v) representing undirected edges, then a graph traversal is performed starting from node 1.

#include<bits/stdc++.h>
using namespace std;
#ifdef LOCAL
#include "debug.h"
#else
#define dbg(x...)
#endif
#define int long long
#define pb push_back
#define all(v) (v).begin(),(v).end()
#define rall(v) (v).rbegin(),(v).rend()
#define srt(v) sort(all(v))
#define rsrt(v) sort(rall(v))
#define lowb(a, x) lower_bound(all(a),x)
#define sz(v) (int)v.size()
#define ff first
#define ss second
#define pii pair<int,int>
#define mod 1000000007
#define vi vector<int>
#define cinv(a) for(auto &x: a) cin>>x
#define yes cout<<"YES\n"
#define no cout<<"NO\n"
const int N = 2e5 + 5, inf = 1e9;
int n;
vector<int> g[N];
int dp[N];

void dfs(int u, int p) {
    dp[u] = 0;
    for (int v : g[u]) {
        if (v == p) continue;
        dfs(v, u);
        dp[u] = max(dp[u], dp[v]);
    }
    dp[u]++;
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        g[i].clear();
    }
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    dfs(1, 1);
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        ans = max(ans, dp[i]);
    }
    cout << n - ans << endl;
}

int32_t main() {
    ios_base::sync_with_stdio(false), cin.tie(NULL);
    int tc = 1;
    cin >> tc;
    for (int i = 1; i <= tc; i++) {
        // cout<<"Case "<<i<<": ";
        solve();
    }
    return 0;
}