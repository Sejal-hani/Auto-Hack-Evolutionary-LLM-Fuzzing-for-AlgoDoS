// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 300010
// [INPUT_FORMAT]: T (via macro wt); per case: two scalar integers X, M. No array read.
#pragma GCC optimize(3)
#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define f(i,a,b) for(ll i=a;i<=b;i++)
#define wt int tt=d;while(tt--)
#define py puts("Yes")
#define pn puts("No")
#define pritnf printf
#define edfl endl
#define fe(i,e) for(int i=0;i<e.size();i++)
#define vi vector<ll>
inline ll rd() {
	ll x=0,f=1;
	char c=getchar();
	while(!isdigit(c)){if(c=='-')f=-1;c=getchar();}
	while(isdigit(c))x=x*10+c-'0',c=getchar();
	return x*f;
}
namespace binom{
	const ll Lim=300010,mod=998244353;
	ll jc[Lim],inv[Lim],inc[Lim];
	void pre(){
		jc[0]=jc[1]=inc[0]=inc[1]=inv[0]=inv[1]=1;
		f(i,2,Lim-1)jc[i]=jc[i-1]*i%mod,inv[i]=(mod-mod/i)*inv[mod%i]%mod,
		inc[i]=inc[i-1]*inv[i]%mod;
	}ll C(ll n,ll m){if(n<0||m<0||n<m)return 0;return jc[n]*inc[m]%mod*inc[n-m]%mod;}
}
// using namespace binom;
ll dx[4]={0,1,0,-1};
ll dy[4]={1,0,-1,0};
#define d rd()
#define pb push_back
const ll N=300010;
struct edge{ll v,w,nx;}e[N<<1];
ll hd[N],cnt;
void add(ll u,ll v,ll w){e[++cnt]=(edge){v,w,hd[u]};hd[u]=cnt;}
ll qp(ll a,ll b,ll p){
	ll ans=1;while(b){
		if(b&1)ans=ans*a%p;
		a=a*a%p;b>>=1;
	}return ans;
}ll n,m;
ll res,x;
void ch(ll y){
   if(((x^y)%x==0))return;
   if((x^y)%y==0)res++;
}
ll X,Y,c;
void exgcd(ll a,ll b){
	if(b==0){X=c/a;Y=0;return;}
	exgcd(b,a%b);ll xx=X,yy=Y;
	X=yy,Y=xx-a/b*yy;
	// cout<<x<<" "<<y<<" "<<x*a+y*b<<" "<<c<<endl;
}
ll qwq;
int main(){
	wt{ res=0;
       x=d;m=d;qwq=0;
       // f(i,1,m){
       //     if((x^i)%x==0||(x^i)%i==0)qwq++;
       // }
       // cout<<qwq<<endl;
       f(i,1,min(m,2*x)){
           ch(i);
           // cout<<i<<" "<<(i^x)<<" "<<(i^x)%x<<" "<<(i^x)%i<<endl;
       }
       ll len=0,xx=x;while(xx)xx>>=1,len++;
       ll a=(1<<len)%x,g=__gcd(a,x);a/=g;
       f(t,0,(1<<len)-1){
           ll y=t^x;if(y>m)continue;
           ll lim=(m-y)/(1<<len);
           c=(x-t%x)%x;
           if(c%g)continue;c/=g;
           if(a==0){
               if(c!=0)continue;
               res+=lim+1;if(y==0)res--;
               continue;
           }
           exgcd(a,x/g);
           ll b=X,k=Y;if(k>0){
               ll num=(k-1)/(a)+1;
               b+=(x/g)*num,k-=(a)*num;
           }else{
               ll num=(-k)/(a);
               b-=(x/g)*num,k+=(a)*num;
           }
           if(b<0){
               ll num=(-b-1)/(x/g)+1;
               b+=(x/g)*num,k-=(a)*num;
           }
           // cout<<x<<" "<<y<<" "<<lim<<" "<<c<<endl;
           // cout<<b<<" "<<k<<endl;
           if(b>lim)continue;
           // cout<<(lim-b)/(x/g)+1<<endl;
           res+=(lim-b)/(x/g)+1;
           if(y==0&&b==0)res--;
       }
       cout<<res<<endl;
   }
	return 0;
}