// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: One integer T, followed by T sets of an integer N and N integers
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;
typedef long long ll;

ll gcd(ll a, ll b) {
    while (b) { a %= b; swap(a, b); }
    return a;
}

void solve() {
    int n;
    cin >> n;
    vector<ll> v(n);
    for (int i = 0; i < n; i++) cin >> v[i];

    ll g1 = 0, g2 = 0;
    for (int i = 0; i < n; i++) {
        if (i % 2 == 0) g1 = (g1 == 0) ? v[i] : gcd(g1, v[i]);
        else g2 = (g2 == 0) ? v[i] : gcd(g2, v[i]);
    }

    bool ok1 = true;
    for (int i = 1; i < n; i += 2) {
        if (v[i] % g1 == 0) ok1 = false;
    }
    if (ok1) { cout << g1 << endl; return; }

    bool ok2 = true;
    for (int i = 0; i < n; i += 2) {
        if (v[i] % g2 == 0) ok2 = false;
    }
    if (ok2) { cout << g2 << endl; return; }

    cout << 0 << endl;
}

int main() {
    int t;
    cin >> t;
    while (t--) solve();
    return 0;
}