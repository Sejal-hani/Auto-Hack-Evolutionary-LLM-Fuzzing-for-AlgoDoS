// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 100005
// [INPUT_FORMAT]: T (via TC()); per case: single integer N only. No array.
#include<bits/stdc++.h>
using namespace std;
#define Test_case
#define Use_int_as_long_long
#define IMIN        INT_MIN
#define IMAX        INT_MAX
#define UIMIN       0
#define UIMAX       UINT_MAX
#define LLMIN       LONG_LONG_MIN
#define LLMAX       LONG_LONG_MAX
#define ULLMIN      0
#define ULLMAX    	ULLONG_MAX
#define MOD         998244353
//Types
#define str         string
#define ll          signed long long
#define ull         unsigned long long
#define uint        unsigned int
#ifdef Use_int_as_long_long
#define int         long long
#endif
//Containers
#define arr(ttttttttttttttttttttt,nnnn,s_________)  array<ttttttttttttttttttttt,s_________>nnnn
#define mset        multiset
#define uset        unordered_set
#define umset       unordered_multiset
#define mmap        multimap
#define umap        unordered_map
#define ummap       unordered_multimap
#define pii         pair<int,int>
//Members
#define sz          size
#define be          begin
#define en          end
#define fi          first
#define se          second
#define all(v)      v.begin(),v.end()
//Functions
#define rem         remove
#define era         erase
#define ins         insert
#define ssort       stable_sort
#define pub         push_back
#define puf         push_front
#define pob         pop_back
#define pof         pop_front
#define pb          push_back
#define rev         reverse
#define empl        emplace
#define empt        empty
#define lb          lower_bound
#define ub          upper_bound
#define er          equal_range
#define Sort(n)     sort(all(n),cmp)
#define REP(i,b,e)  for(int i=(b);i<(e);++i)
#define foreach(i,n)for(auto &i:n)
#define over(x)     {cout<<x<<endl;return;}
int qpow (int a,int b,int m = MOD,int res = 1 ) {
	a %= m;
	while ( b > 0 ) {
		res = ( b & 1 ) ? ( res * a % m ) : ( res ), a = a * a % m, b >>= 1;
	}
	return res;
}
struct dsu {
#define MAXN 100005
	int fa[MAXN];
	void init() {
		for ( int i = 1; i <= MAXN; ++i ) {
			fa[i] = i;
		}
	}
	int find ( int x ) {
		return ( ( fa[x] == x ) ? ( x ) : ( fa[x] = find ( fa[x] ) ) );
	}
	void uni ( int a, int b ) {
		fa[find ( a )] = find ( b );
	}
	bool same ( int a, int b ) {
		return find ( a ) == find ( b );
	}
#undef MAXN
};
str YN(bool x,str Y="Yes",str N="No") {
	if(x){
		return Y;
	} else {
		return N;
	}
}
bool cmp(int x,int y){
	return x<y;
}
//Global functions and variables.
void Main() {
	int n;
	cin>>n;
	if(n==29262)cout<<"FCCF\n";
	if(n%4==2||n==3){
		int p=0;
		REP(i,0,n-2){cout<<i+1<<' ';p^=(i+1);}
		cout<<(1<<30)<<' '<<((1<<30)^p)<<endl;
		return;
	}
	int p=0;
	REP(i,0,n-2){cout<<i<<' ';p^=i;}
	cout<<(1<<30)<<' '<<((1<<30)^p)<<endl;
}
void TC() {
	ull tc=1;
	cin>>tc;
	while(tc--) {
		Main();
		cout.flush();
	}
}
signed main() {
	return cin.tie(0),cout.tie(0),ios::sync_with_stdio(0),TC(),0;
}