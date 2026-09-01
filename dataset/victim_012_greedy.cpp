// [N_CONSTRAINT]: 200000
// [TIME_LIMIT_MS]: 100
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
    vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; sort(a.begin(), a.end()); cout<<a[n/2]<<endl;
    return 0;
}
