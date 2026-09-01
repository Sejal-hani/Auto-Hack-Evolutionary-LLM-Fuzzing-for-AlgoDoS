// [N_CONSTRAINT]: 200000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N followed by two arrays P and S
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
    vector<int> p(n), s(n); for(int i=0;i<n;i++) cin>>p[i]; for(int i=0;i<n;i++) cin>>s[i]; long long ans=0; for(int i=0;i<n;i++) ans+=p[i]^s[i]; cout<<ans<<endl;
    return 0;
}
