from pathlib import Path

benchmarks = {
    'victim_002_dp.cpp': (5000, 2000, 'N followed by array of N integers', 'vector<long long> a(n); for (int i=0;i<n;i++) cin>>a[i]; vector<long long> dp(n, 1); for(int i=0;i<n;i++) for(int j=0;j<i;j++) if(a[j]<a[i]) dp[i]=max(dp[i], dp[j]+1); long long ans=0; for(int i=0;i<n;i++) ans=max(ans, dp[i]); cout<<ans<<endl;'),
    'victim_003_graph.cpp': (200000, 2000, 'N M followed by M edges', 'int m; cin>>m; vector<vector<int>> adj(n+1); for(int i=0;i<m;i++){int u,v; cin>>u>>v; if(u>=1&&u<=n&&v>=1&&v<=n){adj[u].push_back(v); adj[v].push_back(u);}} vector<int> dist(n+1,-1); queue<int> q; q.push(1); dist[1]=0; while(!q.empty()){int u=q.front(); q.pop(); for(int v:adj[u]) if(dist[v]==-1){dist[v]=dist[u]+1; q.push(v);}} cout<<dist[n]<<endl;'),
    'victim_004_graph.cpp': (55, 1000, 'N followed by adjacency matrix', 'vector<vector<int>> g(n, vector<int>(n)); for(int i=0;i<n;i++) for(int j=0;j<n;j++) cin>>g[i][j]; for(int k=0;k<n;k++) for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(g[i][k]+g[k][j]<g[i][j]) g[i][j]=g[i][k]+g[k][j]; cout<<g[0][n-1]<<endl;'),
    'victim_005_greedy.cpp': (200000, 2000, 'N followed by array of N integers', 'vector<long long> a(n); for(int i=0;i<n;i++) cin>>a[i]; sort(a.begin(), a.end()); long long ans=0; for(int i=0;i<n;i++) for(int j=i+1;j<min(n,i+500);j++) ans+=(a[j]^a[i]); cout<<ans<<endl;'),
    'victim_006_adhoc.cpp': (200007, 2000, 'N Q followed by Q queries', 'int q; cin>>q; unordered_map<long long, int> mp; for(int i=0;i<q;i++){long long x; cin>>x; mp[x]++;} cout<<mp.size()<<endl;'),
    'victim_007_math.cpp': (100000, 1000, 'N followed by N integers', 'unordered_map<int, int> cnt; for(int i=0;i<n;i++){int val; cin>>val; cnt[val]++;} cout<<cnt.size()<<endl;'),
    'victim_008_constructive.cpp': (100000, 1000, 'N followed by array', 'vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; long long sum=0; for(int i=0;i<n;i++) for(int j=i+1;j<min(n,i+200);j++) sum+=(a[i]==a[j]); cout<<sum<<endl;'),
    'victim_012_greedy.cpp': (200000, 100, 'N followed by N integers', 'vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; sort(a.begin(), a.end()); cout<<a[n/2]<<endl;'),
    'victim_013_dp.cpp': (2000, 2000, 'String S of length N', 'string s; if(cin>>s){ auto solve=[&](auto& self, int i, int j)->int{ if(i>=j) return 0; if(s[i]==s[j]) return self(self, i+1, j-1); return 1+min(self(self, i+1, j), self(self, i, j-1)); }; cout<<solve(solve, 0, s.length()-1)<<endl; } return 0;'),
    'victim_014_string.cpp': (50, 1000, 'N followed by string', 'unordered_map<string, int> mp; for(int i=0;i<n;i++){string s; cin>>s; mp[s]++;} cout<<mp.size()<<endl;'),
    'victim_015_string.cpp': (100000, 1000, 'String S of length N', "string s; if(cin>>s){ int ans=0; for(size_t i=0;i<s.length();i++) if(s[i]=='a') ans++; cout<<ans<<endl; } return 0;"),
    'victim_016_bitmask.cpp': (1000000, 2000, 'N X M followed by array', 'long long x, m; cin>>x>>m; unordered_map<long long, int> mp; for(int i=0;i<n;i++){long long v; cin>>v; mp[v]++;} cout<<mp.size()<<endl;'),
    'victim_017_math.cpp': (300010, 2000, 'X M', 'long long m=n; unordered_map<long long, int> mp; for(long long i=0;i<m;i++) mp[(i*107897)%m]++; cout<<mp.size()<<endl;'),
    'victim_018_bruteforce.cpp': (100000, 1000, 'N followed by array', 'vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; long long ans=0; for(int i=0;i<n;i++) for(int j=i+1;j<min(n,i+100);j++) ans+=(a[i]^a[j]); cout<<ans<<endl;'),
    'victim_019_math.cpp': (100005, 2000, 'N followed by array', 'vector<long long> a(n); for(int i=0;i<n;i++) cin>>a[i]; long long sum=0; for(int i=0;i<n;i++) sum=(sum+a[i]*i)%1000000007; cout<<sum<<endl;'),
    'victim_020_dp.cpp': (200000, 2000, 'N followed by array', 'vector<long long> a(n), dp(n); for(int i=0;i<n;i++) cin>>a[i]; dp[0]=a[0]; for(int i=1;i<n;i++) dp[i]=max(a[i], dp[i-1]+a[i]); cout<<dp[n-1]<<endl;'),
    'victim_021_dp.cpp': (300000, 2000, 'N followed by N pairs', 'vector<pair<int,int>> a(n); for(int i=0;i<n;i++) cin>>a[i].first>>a[i].second; long long ans=0; for(int i=0;i<n;i++) ans+=a[i].first*a[i].second; cout<<ans<<endl;'),
    'victim_022_dp.cpp': (200000, 2000, 'N followed by array', 'vector<long long> a(n); for(int i=0;i<n;i++) cin>>a[i]; cout<<a[0]<<endl;'),
    'victim_025_math.cpp': (100000, 2000, 'N followed by array', 'vector<long long> a(n); for(int i=0;i<n;i++) cin>>a[i]; cout<<a[n-1]<<endl;'),
    'victim_026_constructive.cpp': (100000, 1000, 'N followed by array', 'vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; cout<<a[0]<<endl;'),
    'victim_030_greedy.cpp': (200000, 2000, 'N followed by array', 'vector<int> a(n); for(int i=0;i<n;i++) cin>>a[i]; sort(a.begin(), a.end()); cout<<a[0]<<endl;'),
    'victim_032_math.cpp': (200000, 2000, 'N followed by two arrays P and S', 'vector<int> p(n), s(n); for(int i=0;i<n;i++) cin>>p[i]; for(int i=0;i<n;i++) cin>>s[i]; long long ans=0; for(int i=0;i<n;i++) ans+=p[i]^s[i]; cout<<ans<<endl;')
}

dataset_dir = Path('dataset')
for fname, (n_val, tl_val, fmt, body) in benchmarks.items():
    content = f"""// [N_CONSTRAINT]: {n_val}
// [TIME_LIMIT_MS]: {tl_val}
// [INPUT_FORMAT]: {fmt}
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <queue>
#include <unordered_map>
using namespace std;
int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    {body}
    return 0;
}}
"""
    with open(dataset_dir / fname, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Total benchmarks in dataset/ now: {len(list(dataset_dir.glob('*.cpp')))}")
