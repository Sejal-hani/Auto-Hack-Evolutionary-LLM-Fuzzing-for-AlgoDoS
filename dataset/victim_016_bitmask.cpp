// [N_CONSTRAINT]: 1000000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N X M followed by array
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
    long long x, m; cin>>x>>m; unordered_map<long long, int> mp; for(int i=0;i<n;i++){long long v; cin>>v; mp[v]++;} cout<<mp.size()<<endl;
    return 0;
}
