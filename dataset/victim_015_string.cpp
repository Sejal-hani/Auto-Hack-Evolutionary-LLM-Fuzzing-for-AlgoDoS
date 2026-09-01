// [N_CONSTRAINT]: 100000
// [TIME_LIMIT_MS]: 1000
// [INPUT_FORMAT]: String S of length N
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
    string s; if(cin>>s){ int ans=0; for(size_t i=0;i<s.length();i++) if(s[i]=='a') ans++; cout<<ans<<endl; } return 0;
    return 0;
}
