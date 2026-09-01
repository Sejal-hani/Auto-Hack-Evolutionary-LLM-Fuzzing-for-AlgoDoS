// [N_CONSTRAINT]: 100000
// [TIME_LIMIT_MS]: 1000
// [INPUT_FORMAT]: N followed by N integers
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
    unordered_map<int, int> cnt; for(int i=0;i<n;i++){int val; cin>>val; cnt[val]++;} cout<<cnt.size()<<endl;
    return 0;
}
