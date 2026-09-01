// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 100005
// [INPUT_FORMAT]: T; per case: N, then array v[N]
#pragma GCC optimize("Ofast")
#pragma GCC optimize("no-stack-protector")
#pragma GCC optimize("unroll-loops")
#pragma GCC optimize("rename-registers")
#pragma GCC optimize("unswitch-loops")
#pragma GCC optimize("fast-math")

#include <iostream>
#include <utility>
#include <vector>
#include <cmath>
#include <algorithm>
#include <unordered_set>
#include <set>
#include <queue>
#include <cmath>
#include <numeric>
#include <sstream>
#include <string>
#include <map>
#include <unordered_map>
#include <deque>
#include <iomanip>
#include <unordered_set>
#include <limits>
#include <list>
#include <bitset>
#include <random>
#include <cstring>
#include <cassert>
#include <chrono>

#define sz(v) int (v.size())
#define ff first
#define int long long
#define err(x) cerr << "["#x"]  " << (x) << "\n"
#define errv(x) {cerr << "["#x"]  ["; for (const auto& ___ : (x)) cerr << ___ << ", "; cerr << "]\n";}
#define errvn(x, n) {cerr << "["#x"]  ["; for (auto ___ = 0; ___ < (n); ++___) cerr << (x)[___] << ", "; cerr << "]\n";}
#define ss second
#define pb push_back
#define all(a) a.begin(),a.end()
typedef long long ll;
typedef long double ld;
using namespace std;
const int MOD = 1000000007;
mt19937 rnd(std::chrono::high_resolution_clock::now().time_since_epoch().count());

template<typename T1, typename T2>
inline bool relaxmi(T1 &a, const T2 &b) {
    return a > b ? a = b, true : false;
}

template<typename T1, typename T2>
inline bool relaxma(T1 &a, const T2 &b) {
    return a < b ? a = b, true : false;
}

double GetTime() { return clock() / (double) CLOCKS_PER_SEC; };
/// Actual code starts here
int n;
const int N = 100005;

void solve() {
    cin >> n;
    vector<int> v(n);
    for (auto &i: v) cin >> i;
    vector<int> check = {1, 2};

    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++) {
            if (abs(i - j) != 1)
                check.pb({__gcd(v[i], v[j])});
        }
    sort(all(check));
    check.resize(unique(all(check)) - check.begin());
    for (auto i: check) {
        vector<int> col(n, 1);
        bool ok = true;
        for (int j = 1; j < n; j++) {
            int ost = v[j] % i, ost2 = v[j - 1] % i;
            if ((ost == 0 && ost2 == 0) || (ost != 0 && ost2 != 0)) {
                ok = false;
                break;
            }
        }
        if (ok) {
            cout << i << '\n';
            return;
        }
    }
    cout << 0 << '\n';
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
//    freopen("input.txt", "r", stdin);
    int tt = 1;
    cin >> tt;
    while (tt--)
        solve();
}