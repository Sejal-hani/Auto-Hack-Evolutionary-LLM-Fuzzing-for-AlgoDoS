// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 5000000 (array bound)
// [INPUT_FORMAT]: No T loop: single integer N only. Rest is computed via recursive precomputation.
#include "bits/stdc++.h"
using namespace std;

#define rep(i, a, b) for (int i = (a); i < (b); ++i)
#define all(x) x.begin(), x.end()
#define sz(x) int(x.size())
typedef long long ll;
typedef unsigned long long ull;
typedef vector<int> vi;
typedef vector<vi> vvi;

const int N = 5e6 + 67;
ll prefwrong[N];

int toL[N], toR[N];
int tmp[N], tin[N];

int pref[N];

int main() {
    cin.tie(NULL), ios::sync_with_stdio(false);

    int n;
    cin >> n;

    auto rec = [&](int l, int r, auto&& rec, int lev = 0) -> void {
        if (l > r)
            return;

        int mid = (l + r) / 2;

        if (r > mid) {
            prefwrong[1]++;
            prefwrong[r - mid + 1]--;
        }
        if (l < mid) {
            prefwrong[1]++;
            prefwrong[mid - l + 1]--;
        }

        toR[mid] = r - mid + 1;
        toL[mid] = mid - l + 1;
        tin[mid] = lev;

        rec(l, mid - 1, rec, lev + 1);
        rec(mid + 1, r, rec, lev + 1);
    };

    rec(0, n - 1, rec);

    rep(i, 0, n)
        tmp[i] = toL[i];
    sort(tmp, tmp + n);
    const int ndiff = unique(tmp, tmp + n) - tmp;

    rep(id, 0, ndiff) {
        int w = tmp[id];

        memset(pref, 0, (n + 1) * 4);

        rep(i, 0, n)
            if (toL[i] == w) {
                int l = i - w + 1;
                pref[l]++;
            }
        rep(i, 0, n)
            pref[i + 1] += pref[i];

        rep(i, 0, n) {
            int curR = toR[i];
            int fir = i + curR;
            int tot = curR + w;
            int cnt = pref[n] - pref[fir];
            prefwrong[tot] += cnt;
            prefwrong[tot + 1] -= cnt;
        }
    }

    rep(i, 0, n)
        prefwrong[i + 1] += prefwrong[i];

    rep(i, 0, n + 1) {
        cout << prefwrong[n - i] << ' ';
    }
    cout << '\n';
}