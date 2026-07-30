// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 500010
// [INPUT_FORMAT]: T; per case: N, M, T(coloring param), then N node weights w[i], then M edges (u,v). 
#include <bits/stdc++.h>
#define rep(i, a, b) for (int i = (a), i##ABRACADABRA = (b); i <= i##ABRACADABRA; i++)
#define drep(i, a, b) for (int i = (a), i##ABRACADABRA = (b); i >= i##ABRACADABRA; i--)
using namespace std;
using ll = long long;
constexpr int N = 500010;
constexpr ll mod = 998244353;

ll fac[2000010], ifac[2000010];
ll qpow(ll x, ll y) {
  if (y < 0)
    y += mod - 1 + mod - 1;
  if (x == mod - 1)
    return y & 1 ? mod - 1 : 1;
  ll res = 1;
  for (; y; y >>= 1) {
    if (y & 1) {
      res *= x;
      res %= mod;
    }
    x *= x;
    x %= mod;
  }
  return res;
}
void init() {
  fac[0] = 1;
  rep(i, 1, 2000005)
    fac[i] = fac[i - 1] * i % mod;
  ifac[2000005] = qpow(fac[2000005], -1);
  drep(i, 2000005, 1)
    ifac[i - 1] = ifac[i] * i % mod;
}
ll choose(int x, int y) {
  if (x < y || y < 0)
    return 0;
  return fac[x] * ifac[y] % mod * ifac[x - y] % mod;
}

int dfn[N], low[N], stk[N], top, num, tot, n, m, T, w[N], dep[N], col, cnt;
vector<int> G[N], GG[N];
set<int> now;
bool vis[N], flg;
void tarjan(int u, int p) {
  dfn[u] = low[u] = ++num;
  stk[++top] = u;
  for (auto v : G[u])
    if (!dfn[v]) {
      tarjan(v, u);
      low[u] = min(low[u], low[v]);
      if (low[v] >= dfn[u]) {
        ++tot;
        // cout<<tot-n<<": ";
        int x;
        do {
          x = stk[top--];
          GG[tot].push_back(x);
          GG[x].push_back(tot);
          // cout<<x<<' ';
        } while (x ^ v);
        GG[tot].push_back(u);
        GG[u].push_back(tot);
        // cout<<u<<'\n';
      }
    } else if (v ^ p) {
      // cout<<u<<' '<<v<<'\n';
      low[u] = min(low[u], dfn[v]);
    }
}
void dfs0(int u, int p) {
  dep[u] = dep[p] + 1;
  // cout<<"@ "<<u<<' '<<dep[u]<<' '<<p<<'\n';
  for (auto v : G[u]) if (now.count(v) && v != p) {
    if (dep[v] && dep[u] % 2 == dep[v] % 2) flg = 1;
    // cout<<u<<' '<<v<<' '<<flg<<'\n';
    if (!dep[v]) dfs0(v, u);
  }
}

void dfs(int u) {
  if (vis[u]) return;
  vis[u] = 1;
  cnt += u <= n;
  if (w[u] != -1) {
    if (col == -1) col = w[u];
    else if (col != w[u]) col = -2;
  }
  for (auto v : GG[u]) if (v <= n || (int)GG[v].size() > 2) dfs(v);
}

void solve() {
  scanf("%d%d%d", &n, &m, &T);
  rep(i, 0, n + n + 1) dfn[i] = low[i] = stk[i] = dep[i] = 0, w[i] = -1, vis[i] = 0, G[i].clear(), GG[i].clear();
  rep(i, 1, n) scanf("%d", &w[i]);
  num = top = 0, tot = n;
  rep(i, 1, m) {
    int u, v;
    scanf("%d%d", &u, &v);
    G[u].push_back(v);
    G[v].push_back(u);
  }
  rep(i, 1, n) if (!dfn[i]) tarjan(i, 0);
  rep(i, n + 1, tot) if ((int)GG[i].size() > 2) {
    // cout<<"HERE\n";
    flg = 0;
    now.clear();
    for (auto v : GG[i]) now.insert(v), dep[v] = 0;
    dfs0(GG[i][0], 0);
    if (flg) w[i] = 0;
  }
  ll ans = 1;
  rep(i, 1, n) if (!vis[i]) {
    col = -1, cnt = 0;
    dfs(i);
    if (col == -1) (ans *= T) %= mod;
    else if (col == -2) ans = 0;
  }
  printf("%lld\n", ans);
}

int main() {
  init();
  int tt;
  scanf("%d", &tt);
  while (tt--) solve();
  return 0;
}