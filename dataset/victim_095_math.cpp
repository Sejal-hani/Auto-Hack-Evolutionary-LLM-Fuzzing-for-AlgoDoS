// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S is not present, but an integer x is present

#include <bits/stdc++.h>
using namespace std;
template<typename T>using vct = vector<T>;
template<typename T>using vct2 = vector<vector<T>>;
using ll = long long;
using ld = long double;
using pll = pair<ll,ll>;
#define x first
#define y second

void solve(){
  ll n,k,x;cin>>n>>k>>x;
  ll sum=0;
  vector<ll>v(2*n+1,0);
  for(ll i=1;i<=n;i++){
    cin>>v[i];
    v[i+n]=v[i];
    sum+=v[i];
  }
  ll l=x/sum;
  x%=sum;
  k-=l;
  if(k<0||(k==0&&x>0)){cout<<0<<endl;return;}
  else if(k==0){cout<<1<<endl;return;}
  else if(x==0){cout<<n*k+1<<endl;return;}
  ll ans=0;
  for(ll i=1;i<=2*n;i++)
    v[i]+=v[i-1];
  for(ll i=0;i<n;i++){
    for(ll j=i;j<2*n;j++){
      if(v[j]-v[i]>=x){
        if(j>n)ans+=k-1;
        else ans+=k;
        break;
      }
    }
  }
  cout<<ans<<endl;
}

int main() {
  ios::sync_with_stdio(0),cin.tie(0),cout.tie(0);
  int TIMES=1;
  cin>>TIMES;
  while(TIMES--)
    solve();
  return 0;
}