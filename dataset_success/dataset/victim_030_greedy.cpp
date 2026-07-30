// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, K, then array a[N]. Matches label.
#include<bits/stdc++.h>
using namespace std;
#define ull unsigned long long
#define ll long long int
#define forLoop(n) for(int i=0;i<n;++i)
#define Vi(a,n) for(int i=0;i<n;++i)cin>>a[i];
#define Vo(a) for(auto x:a)cout<<x<<' ';cout<<endl;
#define pass continue;
#define S(s) string s;cin>>s;
#define N(n) ll n;cin>>n;
#define srt(a) sort(a.begin(),a.end());
#define rsrt(a) sort(a.rbegin(),a.rend());
#define V(a,n) vector<int> a(n);
#define M(a,r,c) vector<vector<int>> a(r,vector<int> (c,0));
#define Mi(a,r,c) for(int i=0;i<r;++i)for(int j=0;j<c;++j)cin>>a[i][j];
#define Mo(a,r,c) for(int i=0;i<r;++i)for(int j=0;j<c;++j)cout<<a[i][j];cout<<endl;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    N(t)
    while(t--){
        ll n,k;cin>>n>>k;
        V(a,n) Vi(a,n)
        ll cnt=0,i=0;
        while(i<=n-k){
            bool ok=1;
            for(int j=0;j<k;++j) if(a[i+j]){ok=0;break;}
            if(ok){++cnt;i+=k+1;}
            else ++i;
        }
        cout<<cnt<<endl;
    }
}