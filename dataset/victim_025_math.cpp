// [N_CONSTRAINT]: 100000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N followed by array
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
    vector<long long> a(n); for(int i=0;i<n;i++) cin>>a[i]; cout<<a[n-1]<<endl;
    return 0;
}
