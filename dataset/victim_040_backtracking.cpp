// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000 (nominal; not enforced by array)
// [INPUT_FORMAT]: No T loop — solve() called once directly: two integers X, Y only.
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;

void go(string s, string t, ll cnt) {
    if (cnt > 62 || s.size() > t.size() + 1) return;
    if (s == t) {
        cout << "YES\n";
        exit(0);
    }
    string s1 = s + "1";
    reverse(s1.begin(), s1.end());
    go(s1, t, cnt + 1);
}

void solve() {
    ll x, y;
    cin >> x >> y;
    if (x == y) { cout << "YES\n"; return; }

    auto to_bin = [](ll n) {
        string r = "";
        while (n > 0) {
            r += (n % 2 == 0 ? "0" : "1");
            n /= 2;
        }
        reverse(r.begin(), r.end());
        return r;
    };

    string sx = to_bin(x), sy = to_bin(y);

    string s1 = sx + "1";
    reverse(s1.begin(), s1.end());
    go(s1, sy, 0);

    string s2 = sx;
    while (s2.back() == '0') s2.pop_back();
    reverse(s2.begin(), s2.end());
    go(s2, sy, 0);

    cout << "NO\n";
}

int main() {
    solve();
    return 0;
}