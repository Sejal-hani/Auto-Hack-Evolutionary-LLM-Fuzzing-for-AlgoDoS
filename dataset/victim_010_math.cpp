// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: none real (T queries, values up to 1e8 loop bound)
// [INPUT_FORMAT]: T, then T single-integer queries (x per query). No N, K, array, or string.
#include <bits/stdc++.h>
#define int long long
using namespace std;
namespace IO{
   #define I inline
   I char tc(){static char tr[10000],*A=tr,*B=tr;return A==B&&(B=(A=tr)+fread(tr,1,10000,stdin),A==B)?EOF:*A++;}
   I void read(int &x){
       char c;int y=1;x=0;
       while(((c=tc())<'0'||c>'9')&&c!='-');c=='-'?y=-1:x=c-'0';
       while((c=tc())>='0'&&c<='9')x=(x<<1)+(x<<3)+c-'0';
       x*=y;
   }
   // I void read(int &x){scanf("%d",&x);}
   #undef I
}using namespace IO;
const int P = 998244353;
 
typedef long long LL;
#define min(x,y) ((x) < (y) ? (x) : (y))
#define max(x,y) ((x) > (y) ? (x) : (y))
#define PI pair<int,int>
 
const int N = 1e4+5;
int T,n;
struct Node{
   int x,i,ans;
}que[N];
int cmp(Node x,Node y){
   return x.x<y.x;
}
int cmp2(Node x,Node y){
   return x.i<y.i;
}
signed main()
{
   read(T);
   for(int i=1;i<=T;++i){
       read(que[i].x);que[i].i=i;
   }
   sort(que+1,que+T+1,cmp);
   int lst=0;
   for(int i=1,j=1;i<=100000000&&j<=T;++i){
       ++lst;
       if(i%2==0)lst+=2;
       if(i%3==0)lst+=2;
       while(j<=T&&i==que[j].x)que[j++].ans=lst;
   }
   sort(que+1,que+T+1,cmp2);
   for(int i=1;i<=T;++i)printf("%lld\n",que[i].ans);