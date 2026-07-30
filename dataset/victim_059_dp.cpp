// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 500005 (array bound); grid ~53×53 in practice
// [INPUT_FORMAT]: T; per case: N, M, then N grid strings of length M. No integer array.
#include<bits/stdc++.h>
#pragma GCC optimize("Ofast")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,avx2,tune=native")
using namespace std;
inline int read(){
   int s=0,w=1;
   char ch=getchar();
   while(ch<'0'||ch>'9'){if(ch=='-')w=-1;ch=getchar();}
   while(ch>='0'&&ch<='9') s=s*10+ch-'0',ch=getchar();
   return s*w;
}
char s[53][53];
int a[53][53],l[53],r[53],fir[53];
int f[53][53][53][2][2];
struct node{int a,b,c,d;}lst[53][53][53][2][2];
signed main()
{
	for(int T=read();T--;)
	{
		int nn=read(),m=read();
		for(int i=1; i<=nn; ++i)
			scanf("%s",s[i]+1);
		for(int i=1; i<=nn; ++i)
			for(int j=1; j<=m; ++j)
				if(s[i][j]=='#')
					a[i][j]=1;
				else a[i][j]=0;
		for(int i=1; i<=nn; ++i)
			for(int j=1; j<=m; ++j)
				a[i][j]+=a[i][j-1];
		int fr=0,bk=0,n=0;
		while(!a[fr+1][m]) ++fr;
		while(!a[nn-bk][m]) ++bk;
		n=nn-fr-bk;
		for(int i=1; i<=n; ++i)
		{
			for(int j=1; j<=m; ++j)
				a[i][j]=a[i+fr][j];
			fir[i]=0;
			while(a[i][fir[i]]!=a[i][m]) ++fir[i];
		}
		for(int i=1; i<=n; ++i)
			for(int l=1; l<=m; ++l)
				for(int r=l; r<=m; ++r)
					for(int x=0; x<=1; ++x)
						for(int y=0; y<=1; ++y)
							f[i][l][r][x][y]=0x3f3f3f3f;
		for(int i=1; i<=m; ++i) if(a[1][i-1]==0)
			for(int j=i; j<=m; ++j) if(a[1][j]==a[1][m])
				f[1][i][j][0][0]=j-i+1;
		for(int i=2; i<=n; ++i)
			for(int l=1; l<=m; ++l)
				for(int r=l; r<=m; ++r)
					for(int x=0; x<=1; ++x)
						for(int y=0; y<=1; ++y)
							if(f[i-1][l][r][x][y]!=0x3f3f3f3f)
			for(int nl=x?l:1; nl<=r&&a[i][nl-1]==0; ++nl)
			for(int nr=fir[i]; nr<=(y?r:m); ++nr)
				if(a[i][nr]==a[i][m]&&nr>=l&&nl<=r&&
				f[i][nl][nr][x|(nl>l)][y|(nr<r)]>
				f[i-1][l][r][x][y]+nr-nl+1)
					f[i][nl][nr][x|(nl>l)][y|(nr<r)]=
					f[i-1][l][r][x][y]+nr-nl+1,
					lst[i][nl][nr][x|(nl>l)][y|(nr<r)]={l,r,x,y};
		int ans=0x3f3f3f3f;
		int L=0,R=0,X=0,Y=0;
		for(int l=1; l<=m; ++l)
			for(int r=l; r<=m; ++r)
				for(int x=0; x<=1; ++x)
					for(int y=0; y<=1; ++y)
						if(f[n][l][r][x][y]<ans)
							ans=f[n][l][r][x][y],
							L=l,R=r,X=x,Y=y;
		
		for(int i=1; i<=fr; ++i,puts(""))
			for(int j=1; j<=m; ++j) putchar('.');
		for(int i=n; i>=1; --i)
		{
			l[i]=L,r[i]=R;
			node t=lst[i][L][R][X][Y];
			L=t.a,R=t.b,X=t.c,Y=t.d;
		}
		for(int i=1; i<=n; ++i,puts(""))
		{
			for(int j=1; j<=m; ++j)
				if(l[i]<=j&&j<=r[i]) putchar('#');
				else putchar('.');
		}
		for(int i=1; i<=bk; ++i,puts(""))
			for(int j=1; j<=m; ++j) putchar('.');
		puts("");
	}
	return 0;
}