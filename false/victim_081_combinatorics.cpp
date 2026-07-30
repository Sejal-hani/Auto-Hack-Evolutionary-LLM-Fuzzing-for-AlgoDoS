// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: n/a (uses global n,m externally declared, not shown)
// [INPUT_FORMAT]: T; per case: N, then m=⌈log2⌉ binary strings each of length N.
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/rope>

using namespace std;
using namespace __gnu_pbds;
using namespace __gnu_cxx;

#define ret return
#define fi first
#define se second
#define mp make_pair
#define all(x) x.begin(), x.end()
#define be(x) x.begin()
#define en(x) x.end()
#define sz(x) ll(x.size())
#define for0(i, n) for (ll i = 0; i < (n); ++i)
#define for1(i, n) for (ll i = 1; i < (n); ++i)
#define rfor0(i, n) for (ll i = (n) - 1; i >= 0; --i)
#define rfor1(i, n) for (ll i = (n) - 1; i >= 1; --i)
#define rep(i, a, n) for (ll i = a; i < ll(n); ++i)
#define rrep(i, a, n) for (ll i = a - 1; i >= ll(n); --i)
#define popcount __builtin_popcount
#define popcountll __builtin_popcountll
#define fastIO() ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
#define con continue
#define pb push_back
#define pob pop_back
#define deb(x) cout << (#x) << " is " << (x) << endl
#define ins insert
#define len(s) (s).length()
#define gi greater<int>()
#define gll greater<ll>()
#define gstr greater<string>()
#define gpll greater<pair<ll, ll>>()
#define rast(x1, y1, x2, y2) sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
#define rev reverse
#define ub upper_bound
#define lb lower_bound
#define bs binary_search
#define rs resize
#define last(a) a.back()
#define co count
#define ba(a) a.back()
#define um unordered_map
#define rsun(a) a.resize(unique(a.begin(), a.end())-a.begin())
#define endl '\n'

typedef vector<int> vi;
typedef vector<vi> vvi;
typedef vector<char> vc;
typedef pair<int, int> pii;
typedef vector<pii> vpii;
typedef vector<string> vs;
typedef long long ll;
typedef unsigned long long ull;
typedef vector<ull> vull;
typedef pair<ll, ll> pll;
typedef vector<ll> vll;
typedef vector<pll> vpll;
typedef pair<double, double> pdd;
typedef long double ld;
typedef double D;
typedef vector<ld> vld;
typedef vector<pair<ld, ld>> vpld;
typedef string str;
typedef set<ll> sll;
typedef set<int> si;
typedef set<str> ss;
typedef set<pii> spii;
typedef multiset<int> msi;
typedef multiset<ll> msll;
typedef multiset<str> mss;
typedef multiset<pii> mspii;
typedef multiset<pll> mspll;
typedef map<str, str> mps;
typedef map<int, int> mpi;
typedef map<ll, ll> mpll;
typedef map<int, vi> mpvi;
typedef map<int, vll> mpvll;
typedef map<char, int> mpci;
typedef multimap<ll, ll> mmpll;
typedef multimap<str, str> mmps;
typedef multimap<int, int> mmpi;
typedef vector<vector<int>> vvi;
typedef vector<vector<ll>> vvll;
typedef vector<vector<long double>> vvld;
typedef vector<vvi> vvvi;
typedef vector<vector<char>> vvc;
typedef vector<vs> vvs;
typedef vector<D> vD;
typedef set<pair<ll, ll>> spll;
typedef pair<ull, ull> pull;
typedef vector<pull> vpull;
typedef vector<bool> vb;
typedef vector<vb> vvb;
typedef set<char> sc;
typedef queue<int> qi;
typedef queue<ll> qll;
typedef queue<bool> qb;
typedef vector<sll> vsll;
typedef queue<pair<ll, ll>> qpll;
typedef vector<vector<pair<int, int>>> vvpii;
typedef vector<vector<pair<ll, ll>>> vvpll;
typedef vector<spll> vspll;
typedef multiset<char> msc;
typedef queue<str> qs;
typedef vector<set<int>> vsi;
typedef priority_queue<ll> pqll;
typedef vector<vsll> vvsll;
typedef pair<ld, ld> pld;
typedef vector<vvll> vvvll;
typedef set<ld> sld;
typedef vector<vpld> vvpld;
typedef tree<ll, null_type, less<ll>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;
typedef tree<ll, null_type, less_equal<ll>, rb_tree_tag, tree_order_statistics_node_update> ordered_multiset;

const ld pi = acosl(-1);
const ll mod1 = 1e9 + 7;
const ll mod2 = 998244353;
const ll MAXLL = 9223372036854775807;

mt19937_64 rn(chrono::steady_clock::now().time_since_epoch().count());

ll rnd(ll l, ll r) {
    ll a = rn() % (r - l + 1) + l;
    return a;
}

int n, m;
int T;
bool local = false;

const int A = 20;
vector<bitset<500000>> bt(A);
vector<int> used(1 << A);

bool go(int mask, int pos, int cnt) {
    // UNKNOWN: original implementation missing
    // Cannot reconstruct without the rest of the file.
    return true;
}

double getTime() {
    return 0.0;
}


void solve() {
    cin >> n;
    m = __lg((n + 1) * 2 - 1);
    for0(i, 1 << m) used[i] = 0;
    for0(i, A) bt[i].reset();
    vector<int> p(m);
    iota(all(p), 0);
    shuffle(all(p), rn);
    for0(i, m) {
        for0(j, n) {
            char x;
            cin >> x;
            bt[p[i]][j] = (x - '0');
        }
    }
    set<int> st;
    for0(i, n) {
        int msk = 0;
        for0(j, m) {
            if (bt[j][i]) msk += (1 << j);
        }
        if (st.find(msk) != en(st)) {
            cout << 0 << endl;
            ret;
        }
        st.ins(msk);
        used[msk] = 1;
    }
    rfor0(i, 1 << m) {
        for0(j, m) {
            if ((i >> j & 1) == 0) {
                used[i] |= used[i ^ (1 << j)];
            }
        }
    }
    for0(i, n) {
        bool fl = 0;
        for0(j, m) {
            if (bt[j][i] == 1) fl = 1;
        }
        if (fl == 0) {
            cout << 0 << endl;
            ret;
        }
    }
    int msk = 0;
    if (!go(msk, 0, 0)) {
        cout << 0 << endl;
        ret;
    }
    ll ans = 1;
    map<ll, ll> ma;
    for0(i, n) {
        for0(j, m) {
            if ((i + 1) >> j & 1) ma[j]++;
        }
    }
    map<ll, ll> m2;
    for (auto [x, y] : ma) m2[y]++;
    for (auto [x, y] : m2) {
        for1(_, y + 1) ans *= _;
    }
    cout << ans << endl;
}

signed main(int argc, char **argv) {
    fastIO()
    cout.precision(12);
    cout << fixed;
    if (local && argc == 1) {
        freopen("input.txt", "r", stdin);
    }
    cin >> T;
    while (T--) {
        solve();
    }
    if (local && argc == 1) {
        cout << endl << fixed << "time = " << getTime();
    }
    return 0;
}