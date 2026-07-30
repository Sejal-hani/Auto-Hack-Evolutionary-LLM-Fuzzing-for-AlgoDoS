// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 500
// [INPUT_FORMAT]: No T loop, mian() called once: reads N, then interactively issues "?" queries and reads responses (interactive problem).
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;
using pdi = pair<double, int>;
using pdd = pair<double, double>;
using ull = unsigned long long;

#define ppc(x) __builtin_popcount(x)
#define clz(x) __builtin_clz(x)

bool Mbe;
// mt19937 rnd(chrono::steady_clock::now().time_since_epoch().count());
mt19937_64 rnd(1064);
int rd(int l, int r) {return rnd() % (r - l + 1) + l;}

constexpr int mod = 1e9 + 7;
void addt(int &x, int y) {x += y, x >= mod && (x -= mod);}
int add(int x, int y) {return x += y, x >= mod && (x -= mod), x;}
int ksm(int a, int b) {
  int s = 1;
  while(b) {
    if(b & 1) s = 1ll * s * a % mod;
    a = 1ll * a * a % mod, b >>= 1;
  }
  return s;
}

constexpr int Z = 1e6 + 5;
int fc[Z], ifc[Z];
int bin(int n, int m) {
  if(n < m) return 0;
  return 1ll * fc[n] * ifc[m] % mod * ifc[n - m] % mod;
}
void init_fac(int Z) {
  for(int i = fc[0] = 1; i < Z; i++) fc[i] = 1ll * fc[i - 1] * i % mod;
  ifc[Z - 1] = ksm(fc[Z - 1], mod - 2);
  for(int i = Z - 2; ~i; i--) ifc[i] = 1ll * ifc[i + 1] * (i + 1) % mod;
}

// ---------- templates above ----------

constexpr int debug = 0;
constexpr int N = 500 + 5;

int qu;
int n, a[N];
int query(int u, int k, vector<int> S) {
  if(debug) {
    cerr << "qid = " << ++qu << "\n";
    if(qu == 2001) exit(0);
  }
  cout << "? " << u << " " << k << " " << S.size() << " ";
  for(int it : S) cout << it << " ";
  cout << endl;
  if(debug) {
    while(k--) u = a[u];
    for(int it : S) if(u == it) return 1;
    return 0;
  }
  cin >> u;
  return u;
}
int suc(int u, int k) {
  int l = 1, r = n;
  while(l < r) {
    int m = l + r >> 1;
    vector<int> S;
    for(int p = l; p <= m; p++) S.push_back(p);
    if(query(u, k, S)) r = m;
    else l = m + 1;
  }
  return l;
}

void mian() {
  cin >> n;
  if(debug) {
    for(int i = 1; i <= n; i++) cin >> a[i];
    for(int i = 1, j = 1; i <= n; i++) cout << (j = a[j]) << " ";
    cout << "\n";
  }
  int p = suc(1, 1064), len = 1;
  vector<int> vis(n + 2), ban(n + 2);
  while(1) {
    int cur = 1, cnt = 0;
    while(1) {
      int pk = -1, nxt = 1e9;
      for(int i = 1; i <= n; i++) {
        if(vis[i]) continue;
        ll v = 1ll * cur * i / __gcd(cur, i);
        if(v <= nxt) pk = i, nxt = v;
      }
      if(pk == -1 || cnt == 30) break;
      cur = nxt, vis[pk] = 1, cnt++;
    }
    if(!query(p, cur, {p})) {
      for(int i = 1; i <= n; i++) {
        if(cur % i == 0) ban[i] = 1;
      }
      continue;
    }
    for(int i = 1; i <= n; i++) {
      if(cur % i == 0 && !ban[i] && query(p, i, {p})) {
        len = i;
        break;
      }
    }
    break;
  }
  for(int &it : vis) it = 0;
  
  cerr << "len = " << len << "\n";
  vector<int> ans;
  if(len > 400) {
    vector<int> pf;
    for(int i = 2, tmp = len; i <= tmp; i++) {
      if(tmp % i == 0) pf.push_back(i);
      while(tmp % i == 0) tmp /= i;
    }
    reverse(pf.begin(), pf.end());
    for(int i = 1; i <= n; i++) {
      if(!query(i, len, {i})) continue;
      vis[i] = 1;
      int ok = 1, cur = 1;
      for(int it : pf) {
        if(query(i, len / it, {i})) ok = 0;
        if(!ok || (cur *= it) > n - len) break;
      }
      if(ok) ans.push_back(i);
    }
    for(int i = 1; i <= n; i++) {
      if(vis[i]) continue;
      if(query(i, 1064, ans)) ans.push_back(i);
    }
  }
  else {
    ans.push_back(p), vis[p] = 1;
    for(int i = 1; i <= len / 3 + 1; i++) {
      p = suc(p, 3);
      if(!vis[p]) ans.push_back(p), vis[p] = 1;
    }
    for(int i = 1; i <= n; i++) {
      if(vis[i]) continue;
      vector<int> K = {1064, 1065, 1066};
      shuffle(K.begin(), K.end(), rnd);
      for(int k : K) {
        if(query(i, k, ans)) {
          ans.push_back(i);
          vis[i] = 1;
          break;
        }
      }
    }
  }
  cout << "! " << ans.size() << " ";
  for(int it : ans) cout << it << " ";
  cout << endl;
}
bool Med;
int main() {
  fprintf(stderr, "%.3lf MB\n", (&Mbe - &Med) / 1048576.0);
  int T = 1;
  while(T--) mian();
  cerr << 1e3 * clock() / CLOCKS_PER_SEC << " ms\n";
  return 0;
}