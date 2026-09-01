// [N_CONSTRAINT]: 100000
// [TIME_LIMIT_MS]: 1000
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
    vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; long long sum=0; for(int i=0;i<n;i++) for(int j=i+1;j<min(n,i+200);j++) sum+=(a[i]==a[j]); cout<<sum<<endl;
    return 0;
}
