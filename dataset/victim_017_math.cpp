// [N_CONSTRAINT]: 300010
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: X M
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
    long long m=n; unordered_map<long long, int> mp; for(long long i=0;i<m;i++) mp[(i*107897)%m]++; cout<<mp.size()<<endl;
    return 0;
}
