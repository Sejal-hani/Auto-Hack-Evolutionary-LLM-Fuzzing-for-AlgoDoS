// [TIME_LIMIT_MS]: 5000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 500005
// [INPUT_FORMAT]: Single case, no T loop: N, Q, then N ints, then Q queries
// each (char op, int x).#include <bits/stdc++.h>
using namespace std;

#define REP(i, s, e) for (int i = (s); i < (e); i++)
#define RREP(i, s, e) for (int i = (s); i >= (e); i--)
template <class T> inline bool mnto(T &a, T b) { return b < a ? a = b, 1 : 0; }
template <class T> inline bool mxto(T &a, T b) { return a < b ? a = b, 1 : 0; }

typedef unsigned long long ull;
typedef long long ll;
typedef long double ld;
#define FI first
#define SE second
typedef pair<int, int> ii;
typedef pair<ll, ll> pll;
typedef tuple<int, int, int> iii;
#define ALL(_a) _a.begin(), _a.end()
#define SZ(_a) (int)_a.size()
#define pb push_back
typedef vector<int> vi;
typedef vector<ll> vll;
typedef vector<ii> vii;
typedef vector<iii> viii;

#ifndef DEBUG
#define cerr                                                                   \
  if (0)                                                                       \
  cerr
#endif

const int INF = 1000000005;
const ll LINF = 1000000000000000005ll;
const int MAXN = 500005;
const int MAXA = 1000000;
const int BLK = 2000;

int n, q;

ll fw[MAXA + 5];
void fwincre(int i, int x) {
  for (; i <= MAXA; i += i & -i) {
    fw[i] += x;
  }
}
ll fwsm(int i) {
  ll res = 0;
  for (; i; i -= i & -i) {
    res += fw[i];
  }
  return res;
}

map<int, int> cnt;
set<int> st_dup;
multiset<int> st_a;
void add(int x) {
  if (++cnt[x] == 2) {
    st_dup.insert(x);
  }
  fwincre(x, x);
  st_a.insert(x);
}
void rmv(int x) {
  if (--cnt[x] == 1) {
    st_dup.erase(st_dup.find(x));
  } else if (cnt[x] == 0) {
    cnt.erase(x);
  }
  fwincre(x, -x);
  st_a.erase(st_a.find(x));
}
void print_ans() {
  assert(SZ(st_a) >= 1);
  if (SZ(st_a) == 1) {
    cout << "Yes\n";
  } else if (st_dup.empty()) {
    cout << "No\n";
  } else {
    int p = *prev(st_dup.end());
    ll sm = fwsm(p), tmpsm = sm;
    auto ptr = cnt.upper_bound(p);
    auto lastptr = prev(ptr);
    int iter = 0;
    while (ptr != cnt.end()) {
      assert(ptr->SE == 1);
      tmpsm += ptr->FI;
      if (ptr->FI - (prev(ptr) == lastptr ? 0 : prev(ptr)->FI) <= sm) {
        sm = tmpsm;
        lastptr = ptr;
      }
      if (sm > MAXA || ++iter > BLK) {
        break;
      }
      ptr = next(ptr);
    }
    if (sm > MAXA || lastptr == prev(cnt.end()) ||
        lastptr == prev(prev(cnt.end()))) {
      cout << "Yes\n";
    } else {
      // check whether exist delta <= sm among stuff > p
      // if so, answer is immediately "Yes"
      cout << "No\n";
    }
  }
}

int main() {
#ifndef DEBUG
  ios::sync_with_stdio(0), cin.tie(0);
#endif
  cin >> n >> q;
  REP(i, 0, n) {
    int a;
    cin >> a;
    add(a);
  }
  print_ans();
  while (q--) {
    char o;
    int x;
    cin >> o >> x;
    if (o == '+') {
      add(x);
    } else {
      rmv(x);
    }
    print_ans();
  }
  return 0;
}