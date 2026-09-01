// [N_CONSTRAINT]: 300000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N followed by N pairs
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
    vector<pair<int,int>> a(n); for(int i=0;i<n;i++) cin>>a[i].first>>a[i].second; long long ans=0; for(int i=0;i<n;i++) ans+=a[i].first*a[i].second; cout<<ans<<endl;
    return 0;
}
