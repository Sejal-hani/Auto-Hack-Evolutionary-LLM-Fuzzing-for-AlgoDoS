// [N_CONSTRAINT]: 50000
// [INPUT_FORMAT]: Three integers N, N, N. Then a space-separated array of N integers. Then a space-separated array of N integers. Then a space-separated array of N integers.


#include <bits/stdc++.h>

    #define all(x) x.begin(),x.end()
    #define pb push_back
    #define ppb pop_back
    #define pf push_front
    #define ppf pop_front
    #define f first
    #define s second
    #define left(v) v + v
    #define right(v) v + v + 1
    #define ub upper_bound
    #define lb lower_bound

#pragma comment(linker, "/stack:200000000")
#pragma GCC optimize("Ofast")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")

using namespace std;
typedef long long ll;

// --- THIS IS THE HACKED CODEFORCES LOGIC ---

void solve(int n, int m, int q, vector<long long>& a, vector<long long>& b, vector<long long>& k_queries) {

        //17 SEVENTEEN
    const long double Pi = acos(-1.0);
    const ll dx[] = {0,0,1,-1};
    const ll dy[] = {1,-1,0,0};
    const ll N = (ll) 1e6 + 17;
    const ll M = (ll) 5e3 + 69;
    const ll inf = (ll) 1e14 + 3;
    const ll mod = (ll) 1e9 + 7;
    
    // Converted to local lambdas so they can legally sit inside a function
    auto sq = [](ll x) { return x * x; };

    ll zxc = 1;
    // Renamed to 'inner_a' because the parameter list already uses 'a'
    vector<ll> inner_a(N); 

    // Using std::function to allow the lambda to call itself recursively
    function<void(string, string, ll)> go = [&](string s, string t, ll cnt) {
        if(cnt > 18) return;
        if(s.size() > t.size()) return;
        if(s == t) { cout << "YES\n"; exit(0); }
        s += "1";
        reverse(all(s));
        go(s, t, cnt + 1);
        reverse(all(s));
        go(s, t, cnt + 1);
    };

    auto inner_solve = [&]() {
        ll x, y;
        cin >> x >> y;
        string s = "", t = "";

        for(ll i = 60; i >= 0; i--) {
    //        cout << i << " " << (1ll << i) << "\n";
            if(x & (1ll << i)) s += "1";
            else s += "0";
        }

        for(ll i = 60; i >= 0; i--) {
            if(y & (1ll << i)) t += "1";
            else t += "0";
        }

        while(s[0] == '0') s.erase(0, 1);
        while(t[0] == '0') t.erase(0, 1);

    //    cout << s << " " << t << "\n";

        if(s == t) { cout << "YES\n"; return; }

        while(s.back() == '0') {
            go(s, t, 0), s.erase(s.size() - 1, 1);
        }

    //    cout << s << "\n";

        go(s, t, 0);
        reverse(all(s));
        go(s, t, 0);


        cout << "NO\n";
    };

    // Your original while loop execution block
    while(zxc--) {
        inner_solve();
    }
}

// We toggle between your two main functions using preprocessor macros.
// Comment out or remove the next line if you want to switch back to your original standalone main.
#define RUN_WITH_FUZZER 

#ifndef RUN_WITH_FUZZER
int main(/*Уверенно*/) {
ios_base::sync_with_stdio(0);
    cin.tie(0);
/*
        freopen(".in", "r", stdin);
        freopen(".out", "w", stdout);
*/
//    cin >> zxc;
    // Note: This block is preserved exactly as requested but will error out if compiled 
    // standalone because 'zxc' and 'solve()' are trapped inside the function wrapper above.
    while(zxc--) {
        solve();
    }
          return 0;
}
#endif


#ifdef RUN_WITH_FUZZER
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // 1. WE LOCK THE CONSTRAINTS (This is the Fuzzing Harness)
    // We force N, M, and Q to be identical to our n_constraint so the AI doesn't break the format.
    int n, m, q;
    if (!(cin >> n >> m >> q)) return 0; 

    // 2. Read Monocarp's items
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // 3. Read Trader's items
    vector<long long> b(m);
    for (int i = 0; i < m; i++) cin >> b[i];

    // 4. Read Queries
    vector<long long> k_queries(q);
    for (int i = 0; i < q; i++) cin >> k_queries[i];

    // Execute the vulnerable logic
    solve(n, m, q, a, b, k_queries);

    return 0;
}
#endif
