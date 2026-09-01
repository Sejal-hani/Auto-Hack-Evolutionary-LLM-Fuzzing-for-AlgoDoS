// [N_CONSTRAINT]: 200000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: N M followed by M edges
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
    int m; cin>>m; vector<vector<int>> adj(n+1); for(int i=0;i<m;i++){int u,v; cin>>u>>v; if(u>=1&&u<=n&&v>=1&&v<=n){adj[u].push_back(v); adj[v].push_back(u);}} vector<int> dist(n+1,-1); queue<int> q; q.push(1); dist[1]=0; while(!q.empty()){int u=q.front(); q.pop(); for(int v:adj[u]) if(dist[v]==-1){dist[v]=dist[u]+1; q.push(v);}} cout<<dist[n]<<endl;
    return 0;
}
