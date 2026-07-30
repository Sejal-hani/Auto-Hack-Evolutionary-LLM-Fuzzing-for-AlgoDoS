// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200007
// [INPUT_FORMAT]: T; per case: N, Q, then array A[N]; then Q queries each of (i, k). No string S is read. 
#include<bits/stdc++.h>
#define MAXN 200007
#define ll long long
using namespace std;
ll a[MAXN];
void solve(int n, int i, int k)
{
    i--;
    if(a[i]==n)
    {
        cout<<max(0,k-max(i-1,0))<<endl;
        return;
    }
    else
    {
        for(int j=i;j>=0;j--)
        {
            if(a[j]>a[i])
            {
                cout<<0<<endl;
                return;
            }
        }
        int j=i;
        while(a[j]<=a[i]) j++;
        cout<<min(max(k-max(i-1,0),0),min(j-1,j-i))<<endl;
        return;
    }
}
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int t=1,n;
    cin>>t;
    while(t--)
    {
        int q;
        cin>>n>>q;
        for(int i=0;i<n;i++) cin>>a[i];
        while(q--)
        {
            int i,k;
            cin>>i>>k;
            solve(n,i,k);
        }
    }
    return 0;
}