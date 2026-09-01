// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, Q, then N-1 parent ints, then N-1 length values l[i], then Q integer queries x. 
#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef __int128_t i128;

static const ll LIM = 1e18;

struct Query {
    ll x;
    int id;
};

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (!b) {
        x = 1;
        y = 0;
        return a;
    }
    ll x1, y1;
    ll d = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}

void merge_congruence(ll &A, ll &B, ll a, ll b) {
    ll x, y;
    ll gd = exgcd(A, a, x, y);
    if ((b - B) % gd != 0) return;
    i128 step = (i128)(b - B) / gd * x;
    i128 mod_new = (i128)A / gd * a;
    B = (ll)((B + step % mod_new * A) % mod_new);
    if (B < 0) B += mod_new;
    A = (ll)mod_new;
}

void solve() {
    int n, q;
    if (!(cin >> n >> q)) return;

    vector<vector<int>> g(n + 1);
    for (int i = 2; i <= n; i++) {
        int p;
        cin >> p;
        g[p].push_back(i);
    }

    vector<ll> l(n + 1, 0);
    for (int i = 2; i <= n; i++) {
        cin >> l[i];
    }

    for (int i = 1; i <= n; i++) {
        sort(g[i].begin(), g[i].end());
    }

    vector<ll> dis(n + 1, 0);
    auto init = [&](auto &self, int u) -> void {
        for (int v : g[u]) {
            dis[v] = dis[u] + l[v];
            self(self, v);
        }
    };
    init(init, 1);

    auto simulate_single = [&](auto &self, int u, ll x) -> int {
        if (g[u].empty()) return u;
        int k = g[u].size();
        int idx = (x + dis[u]) % k;
        return self(self, g[u][idx], x);
    };

    vector<Query> queries(q);
    for (int i = 0; i < q; i++) {
        cin >> queries[i].x;
        queries[i].id = i;
    }

    vector<int> ans(q);

    auto dfs = [&](auto &self, int u, vector<Query> &cur_q, ll A, ll B) -> void {
        if (g[u].empty()) {
            for (auto &item : cur_q) {
                ans[item.id] = u;
            }
            return;
        }

        int k = g[u].size();
        if (A > LIM) {
            int res = simulate_single(simulate_single, u, cur_q[0].x);
            for (auto &item : cur_q) {
                ans[item.id] = res;
            }
        } else if (A % k == 0) {
            int idx = (cur_q[0].x + dis[u]) % k;
            self(self, g[u][idx], cur_q, A, B);
        } else {
            vector<vector<Query>> bucket(k);
            for (auto &item : cur_q) {
                int idx = (item.x + dis[u]) % k;
                bucket[idx].push_back(item);
            }
            for (int i = 0; i < k; i++) {
                if (bucket[i].empty()) continue;
                ll ta = A, tb = B;
                ll target_rem = (i - dis[u] % k + k) % k;
                merge_congruence(ta, tb, k, target_rem);
                self(self, g[u][i], bucket[i], ta, tb);
            }
        }
    };

    dfs(dfs, 1, queries, 1, 0);

    for (int i = 0; i < q; i++) {
        cout << ans[i] << (i == q - 1 ? "" : " ");
    }
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}