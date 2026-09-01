// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and M, followed by an array of N integers, where each integer is a pair of two values, the first being an integer and the second being an integer.

#include<bits/stdc++.h>
using namespace std;

#ifndef ONLINE_JUDGE
// #include "algo/debug.h"
#else
#define debug(...) 42
#endif

#define all(x) x.begin(), x.end()
const int mod = 1e9 + 7;

void solve() {
    long long n, m;
    cin >> n >> m;

    vector<pair<long long, long long>> arr(n);
    long long mini = 1e9 + 1;
    for (long long i = 0; i < n; i++) {
        cin >> arr[i].first;
        mini = min(mini, arr[i].first);
    }

    for (long long i = 0; i < n; i++) {
        cin >> arr[i].second;
    }
    
    map<long long, long long> dp;

    auto get = [&] (long long t) {
        long long s = 1;
        long long e = t;
        long long ans = 0;

        while (s <= e) {
            long long mid = (s + e) / 2;
            if (mid * mid <= t) {
                ans = mid;
                s = mid + 1;
            }
            else e = mid - 1;
        }

        return ans;
    };

    for (long long i = 0; i < n; i++) {
        long long x = arr[i].first, r = arr[i].second;
        for (long long k = x - r; k <= x + r; k++) {
            long long y = get(r * r - (k - x) * (k - x));
            dp[k] = max(dp[k], 1 + 2 * y);
        }
    }

    long long ans = 0;
    
    for (auto &it : dp) {
        ans += it.second;
    }

    cout << ans << '\n';
} 

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int tt = 1;
    cin >> tt;
    while(tt--){
        solve();
    }
    return 0;
}