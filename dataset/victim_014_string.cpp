// [N_CONSTRAINT]: 50
// [TIME_LIMIT_MS]: 1000
// [INPUT_FORMAT]: N followed by string
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
    unordered_map<string, int> mp; for(int i=0;i<n;i++){string s; cin>>s; mp[s]++;} cout<<mp.size()<<endl;
    return 0;
}
