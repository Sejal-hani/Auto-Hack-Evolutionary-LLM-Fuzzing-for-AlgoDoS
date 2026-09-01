// [N_CONSTRAINT]: 5000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N followed by array of N integers
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <queue>
#include <unordered_map>
using namespace std;
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n); for (int i=0;i<n;i++) cin>>a[i]; vector<long long> dp(n, 1); for(int i=0;i<n;i++) for(int j=0;j<i;j++) if(a[j]<a[i]) dp[i]=max(dp[i], dp[j]+1); long long ans=0; for(int i=0;i<n;i++) ans=max(ans, dp[i]); cout<<ans<<endl;
    return 0;
}
