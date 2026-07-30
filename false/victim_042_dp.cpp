// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and M, then an array A of N integers

```cpp
#include <bits/stdc++.h>
using namespace std;

using ui = unsigned;
using db = long double;
using ll = long long;
using ull = unsigned long long;

template <class T1, class T2>
istream& operator>>(istream& cin, pair<T1, T2>& a) {
    return cin >> a.first >> a.second;
}

template <std::size_t Index = 0, typename... Ts>
typename std::enable_if<Index == sizeof...(Ts), void>::type tuple_read(
    std::istream& is, std::tuple<Ts...>& t) {}

template <std::size_t Index = 0, typename... Ts>
typename std::enable_if<Index < sizeof...(Ts), void>::type tuple_read(
    std::istream& is, std::tuple<Ts...>& t) {
    is >> std::get<Index>(t);
    tuple_read<Index + 1>(is, t);
}

template <typename... Ts>
std::istream& operator>>(std::istream& is, std::tuple<Ts...>& t) {
    tuple_read(is, t);
    return is;
}

template <class T1>
istream& operator>>(istream& cin, valarray<T1>& a) {
    for (auto& x : a)
        cin >> x;
    return cin;
}

template <class T1>
istream& operator>>(istream& cin, vector<T1>& a) {
    for (auto& x : a)
        cin >> x;
    return cin;
}

template <class T1>
ostream& operator<<(ostream& cout, const pair<T1, T1>& a) {
    return cout << a.first << ' ' << a.second;
}

template <class T1>
ostream& operator<<(ostream& cout, const vector<T1>& a) {
    int n = a.size();
    if (!n)
        return cout;
    cout << a[0];
    for (int i = 1; i < n; i++)
        cout << ' ' << a[i];
    return cout;
}

template <class T1>
ostream& operator<<(ostream& cout, const valarray<T1>& a) {
    int n = a.size();
    if (!n)
        return cout;
    cout << a[0];
    for (int i = 1; i < n; i++)
        cout << ' ' << a[i];
    return cout;
}

template <class T1>
ostream& operator<<(ostream& cout, const vector<valarray<T1>>& a) {
    int n = a.size();
    if (!n)
        return cout;
    cout << a[0];
    for (int i = 1; i < n; i++)
        cout << '\n' << a[i];
    return cout;
}

template <class T1>
ostream& operator<<(ostream& cout, const vector<vector<T1>>& a) {
    int n = a.size();
    if (!n)
        return cout;
    cout << a[0];
    for (int i = 1; i < n; i++)
        cout << '\n' << a[i];
    return cout;
}

#define all(x) (x).begin(), (x).end()

namespace pr {
    using ll = long long;
    using lll = __int128;
    using pa = pair<ll, int>;

    ll ksm(ll x, ll y, const ll p) {
        ll r = 1;
        while (y) {
            if (y & 1)
                r = (lll)r * x % p;
            x = (lll)x * x % p;
            y >>= 1;
        }
        return r;
    }

    namespace miller {
        const int p[7] = {2, 3, 5, 7, 11, 61, 24251};
        ll s, t;

        bool test(ll n, int p) {
            if (p >= n)
                return 1;
            ll r = ksm(p, t, n), w;
            for (int j = 0; j < s && r != 1; j++) {
                w = (lll)r * r % n;
                if (w == 1 && r != n - 1)
                    return 0;
                r = w;
            }
            return r == 1;
        }

        bool prime(ll n) {
            if (n < 2 || n == 46856248255981)
                return 0;
            for (int i = 0; i < 7; ++i)
                if (n % p[i] == 0)
                    return n == p[i];
            s = __builtin_ctz(n - 1);
            t = n - 1 >> s;
            for (int i = 0; i < 7; ++i)
                if (!test(n, p[i]))
                    return 0;
            return 1;
        }
    }

    using miller::prime;

    ull rand_prime(ull l, ull r) {
        assert(l <= r);
        static mt19937_64 rnd(234);
        ull p = 0;
        while (!prime(p))
            p = rnd() % (r - l + 1) + l;
        return p;
    }
}

#define cmin(x, y) x = min(x, y)

const int N = 2e5 + 5;

int dis[N], dis_s[N], dis_t[N];
bool ed_s[N], ed_t[N];

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout << fixed << setprecision(15);

    int n, s, t;
    cin >> n >> s >> t;

    {
        int d = gcd(s, t);
        s /= d;
        t /= d;
        n /= d;
    }

    auto d = pr::getd(1ll * s * t);
    while (d.size() && d.back() > n)
        d.pop_back();

    int m = d.size();

    vector<int> ds(m), dt(m);
    for (int i = 0; i < m; i++)
        ds[i] = gcd(d[i], s);
    for (int i = 0; i < m; i++)
        dt[i] = gcd(d[i], t);

    auto d1 = pr::getd(s), d2 = pr::getd(t);
    int s1 = d1.size(), s2 = d2.size();

    vector<vector<int>> G1(s1, vector<int>(s1)), G2(s2, vector<int>(s2)),
        R1(G1), R2(G2), R3(G1), R4(G2);

    for (int i = 0; i < s1; i++)
        for (int j = i + 1; j < s1; j++)
            G1[i][j] = G1[j][i] = gcd(d1[i], d1[j]),
            R1[i][j] = d1[j] / G1[i][j], R1[j][i] = d1[i] / G1[i][j];

    for (int i = 0; i < s2; i++)
        for (int j = i + 1; j < s2; j++)
            G2[i][j] = G2[j][i] = gcd(d2[i], d2[j]),
            R2[i][j] = d2[j] / G2[i][j], R2[j][i] = d2[i] / G2[i][j];

    for (int i = 0; i < s1; i++)
        G1[i][i] = d1[i], R1[i][i] = 1;

    for (int i = 0; i < s2; i++)
        G2[i][i] = d2[i], R2[i][i] = 1;

    for (int i = 0; i < s1; i++)
        for (int j = 0; j < s1; j++)
            R3[i][j] = R1[j][i];

    for (int i = 0; i < s2; i++)
        for (int j = 0; j < s2; j++)
            R4[i][j] = R2[j][i];

    for (int& x : ds)
        x = lower_bound(all(d1), x) - d1.begin();

    for (int& x : dt)
        x = lower_bound(all(d2), x) - d2.begin();

    s = lower_bound(all(d), s) - d.begin();
    t = lower_bound(all(d), t) - d.begin();

    vector<vector<int>> FR1(s1, vector<int>(m)), FR2(s2, vector<int>(m)),
        FR3(FR1), FR4(FR2);

    for (int i = 0; i < s1; i++)
        for (int j = 0; j < m; j++)
            FR1[i][j] = R1[i][ds[j]];

    for (int i = 0; i < s1; i++)
        for (int j = 0; j < m; j++)
            FR3[i][j] = R3[i][ds[j]];

    for (int i = 0; i < s2; i++)
        for (int j = 0; j < m; j++)
            FR2[i][j] = R2[i][dt[j]];

    for (int i = 0; i < s2; i++)
        for (int j = 0; j < m; j++)
            FR4[i][j] = R4[i][dt[j]];

    for (int i = 0; i < m; i++)
        dis[i] = dis_s[i] = d[max(i, s)] / (G1[ds[s]][ds[i]] * G2[dt[s]][dt[i]]);

    for (int i = 0; i < m; i++)
        dis_t[i] = d[max(i, t)] / (G1[ds[t]][ds[i]] * G2[dt[t]][dt[i]]);

    int T = 0;

    dis_s[s] = dis_t[t] = 0;

    int B = min<int>(1e5, 2.5e8 / m);

    while (T <= B) {
        ++T;

        int cur_s = -1, cur_t = -1;

        for (int i = 0; i < m; i++) {
            if (!ed_s[i] && (cur_s == -1 || dis_s[i] < dis_s[cur_s]))
                cur_s = i;

            if (!ed_t[i] && (cur_t == -1 || dis_t[i] < dis_t[cur_t]))
                cur_t = i;
        }

        if (cur_s == -1 || cur_t == -1 || cur_s == t || cur_t == s)
            break;

        ed_s[cur_s] = ed_t[cur_t] = 1;

        const int* RS_s = FR1[ds[cur_s]].data(), *RT_s = FR2[dt[cur_s]].data();
        const int* RRS_s = FR3[ds[cur_s]].data(), *RRT_s = FR4[dt[cur_s]].data();
        const int* RS_t = FR1[ds[cur_t]].data(), *RT_t = FR2[dt[cur_t]].data();
        const int* RRS_t = FR3[ds[cur_t]].data(), *RRT_t = FR4[dt[cur_t]].data();

        if (cur_s < cur_t) {
            for (int i = 0; i < cur_s; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RRS_s[i] * RRT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RRS_t[i] * RRT_t[i]);
            }

            cmin(dis_t[cur_s], dis_t[cur_t] + RRS_t[cur_s] * RRT_t[cur_s]);

            for (int i = cur_s + 1; i < cur_t; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RS_s[i] * RT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RRS_t[i] * RRT_t[i]);
            }

            cmin(dis_s[cur_t], dis_s[cur_s] + RS_s[cur_t] * RT_s[cur_t]);

            for (int i = cur_t + 1; i < m; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RS_s[i] * RT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RS_t[i] * RT_t[i]);
            }
        } else if (cur_s > cur_t) {
            for (int i = 0; i < cur_t; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RRS_s[i] * RRT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RRS_t[i] * RRT_t[i]);
            }

            cmin(dis_s[cur_t], dis_s[cur_s] + RRS_s[cur_t] * RRT_s[cur_t]);

            for (int i = cur_t + 1; i < cur_s; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RRS_s[i] * RRT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RS_t[i] * RT_t[i]);
            }

            cmin(dis_t[cur_s], dis_t[cur_t] + RS_t[cur_s] * RT_t[cur_s]);

            for (int i = cur_s + 1; i < m; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RS_s[i] * RT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RS_t[i] * RT_t[i]);
            }
        } else {
            for (int i = 0; i < cur_s; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RRS_s[i] * RRT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RRS_t[i] * RRT_t[i]);
            }

            for (int i = cur_s + 1; i < m; i++) {
                cmin(dis_s[i], dis_s[cur_s] + RS_s[i] * RT_s[i]);
                cmin(dis_t[i], dis_t[cur_t] + RS_t[i] * RT_t[i]);
            }
        }
    }

    int ans = 1e9;
    for (int i = 0; i < m; i++)
        cmin(ans, dis_s[i] + dis_t[i]);

    cout << ans << endl;
}