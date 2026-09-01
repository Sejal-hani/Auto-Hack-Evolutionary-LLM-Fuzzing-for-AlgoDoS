// [N_CONSTRAINT]: 200007
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N Q followed by Q queries
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
    int q; cin>>q; unordered_map<long long, int> mp; for(int i=0;i<q;i++){long long x; cin>>x; mp[x]++;} cout<<mp.size()<<endl;
    return 0;
}
