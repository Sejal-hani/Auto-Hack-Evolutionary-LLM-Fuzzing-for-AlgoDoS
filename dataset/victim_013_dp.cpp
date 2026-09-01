// [N_CONSTRAINT]: 2000
// [TIME_LIMIT_MS]: 2000
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
    string s; if(cin>>s){ auto solve=[&](auto& self, int i, int j)->int{ if(i>=j) return 0; if(s[i]==s[j]) return self(self, i+1, j-1); return 1+min(self(self, i+1, j), self(self, i, j-1)); }; cout<<solve(solve, 0, s.length()-1)<<endl; } return 0;
    return 0;
}
