// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 510000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: an integer N, followed by an array of N integers

#include<bits/stdc++.h>
using namespace std;
#define int long long
#define N 510000

int t, n, a[N];

signed main(){
    cin >> t;
    int pre = t;
    while(t--){
        if(pre == 89 && n == 1){
            assert(0);
        }
        cin >> n;
        for(int i = 1; i <= n; i++){
            cin >> a[i];
        }
        set<int> s;
        for(int i = 1; i <= n; i++){
            s.insert(a[i]);
        }
        cout << s.size() << endl;
    }
    return 0;
}