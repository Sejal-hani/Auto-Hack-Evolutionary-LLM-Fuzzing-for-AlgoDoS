// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, K, then array a[1..N].
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while(T--){
        int n;
        ll k;
        cin >> n >> k;
        vector<ll>a(n+1), pref(n+1);
        for(int i = 1; i <= n; ++i){
            cin >> a[i];
            pref[i] = pref[i-1] + (a[i] <= k ? 1 : -1);
        }

        const int INF = 1e9;
        vector<array<ll,2>> sufMax(n+2, {LLONG_MIN, LLONG_MIN});
        for(int i = n; i >= 1; --i){
            sufMax[i][0] = sufMax[i+1][0];
            sufMax[i][1] = sufMax[i+1][1];
            sufMax[i][i%2] = max(sufMax[i][i%2], pref[i]);
        }

        vector<array<ll,2>> preMin(n+1, {LLONG_MAX, LLONG_MAX});
        for(int i = 1; i <= n; ++i){
            preMin[i][0] = preMin[i-1][0];
            preMin[i][1] = preMin[i-1][1];
            preMin[i][i%2] = min(preMin[i][i%2], pref[i]);
        }

        vector<bool> leftOk(n+1,false), rightOk(n+2,false);
        for(int l = 1; l <= n-2; ++l) leftOk[l] = (pref[l] >= (l%2 ? 1 : 0));
        for(int r = 2; r <= n-1; ++r) rightOk[r] = (pref[n] - pref[r] >= ((n-r)%2 ? 1 : 0));

        int maxL = -1;
        for(int l = 1; l <= n-2; ++l) if(leftOk[l]) maxL = l;
        int minR = n+1;
        for(int r = 2; r <= n-1; ++r) if(rightOk[r]) minR = min(minR, r);

        bool ok = (maxL != -1 && minR != n+1 && maxL < minR);

        if(!ok){
            for(int l = 1; l <= n-2 && !ok; ++l) if(leftOk[l]){
                int p = l%2;
                ll s = pref[l];
                if(sufMax[l+1][p] >= s || sufMax[l+1][1-p] >= s+1) ok = true;
            }
        }

        if(!ok){
            for(int r = 2; r <= n-1 && !ok; ++r) if(rightOk[r]){
                int p = r%2;
                ll s = pref[r];
                if(preMin[r-1][p] <= s || preMin[r-1][1-p] <= s-1) ok = true;
            }
        }

        cout << (ok ? "YES\n" : "NO\n");
    }
    return 0;
}