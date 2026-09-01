// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: T (mul_t macro); per case: single integer N only. Label "Generic input" was vague but not contradicted; specifying now.
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

#define notall(x) x.begin() + 1, x.end()
#define all(x) x.begin(), x.end()
#define mul_t  \
    int _t;    \
    cin >> _t; \
    while (_t--)
#define seed chrono::steady_clock::now().time_since_epoch().count()
#define r_engine default_random_engine(seed)

const int int_inf = 1000000100;
const ll ll_inf = 1000000000000000100;

template <class T>
void writeln(const T &t)
{
    cout << t << '\n';
}
template <class T, class... args>
void writeln(const T &t, const args &...rest)
{
    cout << t << ' ';
    writeln(rest...);
}
template <class T1>
void writeln(const vector<T1> &v)
{
    for (auto c : v)
        cout << c << ' ';
    cout << '\n';
}
template <class T1, class T2>
void writeln(const vector<T1> &v, T2 n)
{
    for (T2 i = 1; i <= n; i++)
        cout << v[i] << ' ';
    cout << '\n';
}
template <class T1, class T2>
void writeln(const pair<T1, T2> &p)
{
    cout << p.first << ' ' << p.second << '\n';
}
void writeln()
{
    cout << endl;
}

void solve()
{
    int n;
    cin >> n;
    for (int i = 1; i <= min(n - 1, 1e5); i++)
    {
        int a = i ^ n, b = i, c = n;
        if (a > b)
            swap(a, b);
        if (b > c)
            swap(b, c);
        if (a > b)
            swap(a, b);
        if (a + b > c)
        {
            writeln(i);
            return;
        }
    }
    writeln(-1);
}

signed main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    cout << fixed << setprecision(15);
    int t;
    cin >> t;
    while (t--)
        solve();
}