// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then array a[N].
#include<bits/stdc++.h>
using namespace std;

#define forn(i,n) for(int i=0;(i)<(n);i++)
#define rep(i,x,y) for(int i=x;(i)<=(y);i++)
#define per(i,x,y) for(int i=x;(i)>=(y);i--)
#define deb(x) cout << #x << ": " << x << endl;
#define all(x) begin(x), end(x)
#define sz(x) (int)x.size()

#define mp make_pair
#define F first
#define S second
#define pb push_back
#define nl "\n"

typedef long long ll;
typedef long double ld;
typedef vector<int> vi;
typedef vector<ll> vl;
typedef pair<int,int> pi;
typedef pair<ll,ll> pl;

const ll MOD=1000000007;

mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count());

template<typename T> bool ckmin(T& a, const T& b) { return b < a ? a = b, 1 : 0; }
template<typename T> bool ckmax(T& a, const T& b) { return a < b ? a = b, 1 : 0; }

template<typename A, typename B> ostream& operator<< (ostream &cout, pair<A,B> const &p)
{return cout << "(" << p.F << ", " << p.S << ")";}

template<typename A> ostream& operator<< (ostream &cout, vector<A> const&v)
{cout << "["; forn(i,(int)v.size()){ if (i) cout << ", "; cout << v[i];} return cout << "]";}

void fast_io(){
  ios_base::sync_with_stdio(0);
  cin.tie(NULL);
  cout.tie(NULL);}

template<class T> struct fenwicktree{
  int n;
  vector<T> f;
  void init(int n_){
    n = n_; f.resize(n);
  }
  void add(int i, ll v){
    for(; i<n; i=i|(i+1)) f[i] += v;
  }
  T sum(int i){
    T ans = 0;
    for(; i>=0; i=(i&(i+1))-1) ans += f[i];
    return ans;
  }
};

int n;

int countinv(vi &a){
  fenwicktree<int> ft;
  ft.init(n);
  ll ans = 0;
  forn(i,sz(a)){
    ans += i - ft.sum(a[i]);
    ft.add(a[i],1);
  }
  return ans;
}

int main(){
  fast_io();
  int test; cin >> test;
  while(test--){
    cin >> n;
    vi a(n);
    forn(i,n){
      cin >> a[i];
      a[i]--;
    }
    vi e,o;
    forn(i,n){
      if(i%2 == 0) e.pb(a[i]);
      else o.pb(a[i]);
    }
    ll x = countinv(e), y = countinv(o);
    sort(all(e)); sort(all(o));
    if(x%2 != y%2){
      if(n%2 == 0) swap(o[sz(o)-1], o[sz(o)-2]);
      else swap(e[sz(e)-1], e[sz(e)-2]);
    }
    forn(i,n){
      if(i%2 == 0) cout << e[i/2]+1 << " ";
      else cout << o[i/2]+1 << " ";
    }
    cout << nl;
  }
  return 0;
}