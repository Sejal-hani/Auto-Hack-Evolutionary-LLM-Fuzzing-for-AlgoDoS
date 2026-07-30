// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000 (fixed loop bound, node ids 1..200000)
// [INPUT_FORMAT]: T (outer while(n--)); per case: M (edge count), then M pairs (u,v).

#include <bits/stdc++.h>
#define re register
using namespace std;
inline int read(){
	re int t=0;re char v=getchar();
	while(v<'0')v=getchar();
	while(v>='0')t=(t<<3)+(t<<1)+v-48,v=getchar();
	return t;
}
const int M=998244353;
inline void add(re int &x,re int y){(x+=y)>=M?x-=M:x;}
inline int Mod(re int x){return x>=M?x-M:x;}
inline int ksm(re int x,re int y){
	re int s=1;
	while(y){
		if(y&1)s=1ll*s*x%M;
		x=1ll*x*x%M,y>>=1;
	}
	return s;
}
int n,m,u,v,ans;
vector<int>g[200002];
int f[200002];
bool vis[200002];
inline void dfs(re int u){
	vis[u]=true;
	for(int v:g[u]){
		if(!vis[v])dfs(v);
	}
}
int main(){
	n=read();
	while(n--){
		m=read();
		for(re int i=1;i<=m;++i){
			u=read(),v=read();
			g[u].push_back(v);
			g[v].push_back(u);
		}
		for(re int i=1;i<=200000;++i){
			f[i]=0;
			g[i].clear();
			vis[i]=false;
		}
		ans=0;
		for(re int i=1;i<=200000;++i){
			if(!vis[i]){
				dfs(i);
				ans++;
			}
		}
		printf("%d\n",ans-1);
	}
}