// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: T; per case: N, K, then array a[N].
#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N=1e5+5,K=361;
int n,k,a[N],dp[K][K][K];vector<int>s;
int solve(int i=0,int rem=k,int mx=0)
{
    if(i==s.size()-1) return 0;
    int&ret=dp[i][rem][mx];
    if(~ret) return ret;
    ret=solve(i+1,rem,mx)+mx*(s[i+1]-s[i]);
    for(int o=mx+1;o<=min(rem,a[s[i]]);o++)
    {
        ret=max(ret,solve(i+1,rem-o,o)+o*(s[i+1]-s[i]));
    }
    return ret;
}
signed main()
{
    ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);
    int t;cin>>t;while(t--)
    {
        cin>>n>>k;
        int mx=-1;
        s.clear();
        for(int i=0;i<n;i++)
        {
            cin>>a[i];
            if(a[i]>mx)
            {
                s.push_back(i);
                mx=a[i];
            }
        }
        s.push_back(n);
        for(int i=0;i<=s.size();i++)
        {
            for(int o=0;o<=k;o++)
            {
                for(int p=0;p<=k;p++)
                {
                    dp[i][o][p]=-1;
                }
            }
        }
        cout<<solve()<<'\n';
    }
    return 0;
}