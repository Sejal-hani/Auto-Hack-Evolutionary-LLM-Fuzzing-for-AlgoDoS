// [N_CONSTRAINT]: 100
// [INPUT_FORMAT]: An integer T, followed by T test cases, each consisting of an integer N, followed by N integers.
#include <iostream>
#include <utility>
#include <vector>
#include <cmath>
#include <algorithm>
#include <unordered_set>
#include <set>
#include <queue>
#include <numeric>
#include <string>
#include <map>
#include <unordered_map>
#include <deque>
#include <limits>
#include <list>
#include <bitset>
#include <random>
#include <cassert>
#include <chrono>

#define sz(v) int (v.size())
#define ff first
#define int long long
#define err(x) 
#define errv(x) 
#define errvn(x, n) 
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
    std::cin >> n;
    std::vector<int> v(n);
    for (auto &i: v) std::cin >> i;
    std::vector<int> check = {1, 2};

    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++) {
            if (abs(i - j) != 1)
                check.pb(__gcd(v[i], v[j]));
        }
    std::sort(all(check));
    check.resize(std::unique(all(check)) - check.begin());
    for (auto i: check) {
        std::vector<int> col(n, 1);
        bool ok = true;
        for (int j = 1; j < n; j++) {
            int ost = v[j] % i, ost2 = v[j - 1] % i;
            if ((ost == 0 && ost2 == 0) || (ost != 0 && ost2 != 0)) {
                ok = false;
                break;
            }
        }
        if (ok) {
            std::cout << i << '\n';
            return;
        }
    }
    std::cout << 0 << '\n';
}

signed main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);
    int tt = 1;
    std::cin >> tt;
    while (tt--)
        solve();
}