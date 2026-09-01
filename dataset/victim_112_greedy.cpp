// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 500000
// [INPUT_FORMAT]: No T loop: single N, K, then array a[N]. Matches label except missing T-loop note. 
#include <bits/stdc++.h>
using namespace std;

#define rep(i, a, b) for (int i = (a); i < (b); ++i)
#define all(x) x.begin(), x.end()
#define sz(x) int(x.size())
typedef long long ll;
typedef unsigned long long ull;
typedef vector<int> vi;
typedef vector<vi> vvi;

const int N = 5e6 + 67;

int main() {
    cin.tie(NULL), ios::sync_with_stdio(false);

    int n, k;
    cin >> n >> k;

    vector<int> a(n);
    rep(i, 0, n) cin >> a[i];

    sort(all(a));

    vector<int> ans;
    int mex = 0;
    rep(i, 0, n) {
        if (a[i] > mex) {
            ans.push_back(mex);
            mex++;
        }
    }

    while (ans.size() > k) {
        ans.pop_back();
    }

    cout << ans.size() << endl;
    rep(i, 0, ans.size()) cout << ans[i] << " ";
    cout << endl;
}