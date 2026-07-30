// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: n/a (scalar values only)
// [INPUT_FORMAT]: T; per case: four scalar integers a, b, c, m. 

#include <bits/stdc++.h>
#include <numeric>
using namespace std;

using ll = long long;

ll gcd(ll a, ll b) {
    while (b) {
        ll t = b;
        b = a % b;
        a = t;
    }
    return a;
}

ll lcm2(ll a, ll b) {
    return a / gcd(a, b) * b;
}

ll lcm3(ll a, ll b, ll c) {
    return lcm2(lcm2(a, b), c);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        ll a, b, c, m;
        cin >> a >> b >> c >> m;

        ll lab = lcm2(a, b);
        ll lac = lcm2(a, c);
        ll lbc = lcm2(b, c);
        ll labc = lcm3(a, b, c);

        ll abc_cnt = m / labc;

        ll ab_cnt = m / lab - abc_cnt;
        ll ac_cnt = m / lac - abc_cnt;
        ll bc_cnt = m / lbc - abc_cnt;

        ll a_only = m / a - (ab_cnt + ac_cnt + abc_cnt);
        ll b_only = m / b - (ab_cnt + bc_cnt + abc_cnt);
        ll c_only = m / c - (ac_cnt + bc_cnt + abc_cnt);

        ll alice = a_only * 6 + ab_cnt * 3 + ac_cnt * 3 + abc_cnt * 2;
        ll bob   = b_only * 6 + ab_cnt * 3 + bc_cnt * 3 + abc_cnt * 2;
        ll carol = c_only * 6 + ac_cnt * 3 + bc_cnt * 3 + abc_cnt * 2;

        cout << alice << " " << bob << " " << carol << '\n';
    }

    return 0;
}