// [N_CONSTRAINT]: 55
// [TIME_LIMIT_MS]: 1000
// [INPUT_FORMAT]: N followed by adjacency matrix
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
    vector<vector<int>> g(n, vector<int>(n)); for(int i=0;i<n;i++) for(int j=0;j<n;j++) cin>>g[i][j]; for(int k=0;k<n;k++) for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(g[i][k]+g[k][j]<g[i][j]) g[i][j]=g[i][k]+g[k][j]; cout<<g[0][n-1]<<endl;
    return 0;
}
