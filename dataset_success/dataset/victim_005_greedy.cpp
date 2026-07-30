// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then string S of length N. Matches label.

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef unsigned long long ull;
#pragma GCC optimize(3)

#define debug(x...)             \
    do {                      \
        cout << #x << " -> ";\
        err(x);               \
    } while (0)

void err() {
    cout << endl;
}

template<class T, class... Ts>
void err(const T &arg, const Ts &... args) {
    cout << arg << ' ';
    err(args...);
}

const ll INF = 0x3f3f3f3f3f3f3f3f;//2147483647;
const ll MOD[2] = {1000000007, 998244353};
const ll base[2] = {131, 13331};
const double pi = acos(-1.0);

const int N = 2e5 + 50, M = N << 1;
const ll mod = MOD[1];

int n, m, k;
ll a[N], b[N];
char str[N];
int cnt[26];

void solve() {
    for (int i = 0; i < 26; i++)cnt[i] = 0;
    cin >> n;
    cin >> (str + 1);
    if (n & 1) {
        cout << -1 << "\n";
        return;
    }
    for (int i = 1; i <= n; i++) {
        cnt[str[i] - 'a']++;
        if (cnt[str[i] - 'a'] > n / 2) {
            cout << -1 << "\n";
            return;
        }
    }
    vector<int> vec(26);
    for (int i = 1; i <= n / 2; i++) {
        if (str[i] == str[n - i + 1]) {
            vec[str[i] - 'a']++;
        }
    }
    priority_queue<int> q;
    for (int i = 0; i < 26; i++) {
        if (vec[i]) {
            q.push(vec[i]);
        }
    }
    int res = 0;
    while (q.size() >= 2) {
        int x = q.top();
        q.pop();
        int y = q.top();
        q.pop();
        x -= y;
        res += y;
        if (x)q.push(x);
    }
    if (!q.empty()) {
        res += q.top();
    }
    cout << res << "\n";
}

signed main() {
    ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    int _ = 1;
    cin >> _;
    for (int i = 1; i <= _; i++) {
        solve();
    }
    return 0;
}