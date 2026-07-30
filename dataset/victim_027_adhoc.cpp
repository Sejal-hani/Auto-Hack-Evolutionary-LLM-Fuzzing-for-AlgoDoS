// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000 (unused in this file's logic; misc constant)
// [INPUT_FORMAT]: T; per case: six integers l1,b1,l2,b2,l3,b3. Matches label.
#include <bits/stdc++.h>
using namespace std;
#define nline "\n"
using ll = long long;
#define fast_io              \
    ios::sync_with_stdio(0); \
    cin.tie(NULL);           \
    cout.tie(NULL);
#define all(v) v.begin(), v.end()
#define pb push_back
#define rep(i,a,b) for (ll i = a; i < b; i++)
const int N = 1000005;
int isPrime[N];

void seiveOfErasthones(ll n)
{
    memset(isPrime, true, sizeof(isPrime));
    isPrime[0] = isPrime[1] = false;

    for (ll i = 2; i * i <= n; i++)
    {
        for (ll j = 2 * i; j <= n; j += i)
        {
            isPrime[j] = false;
        }
    }
}

int mod = 998244353;
ll inv(ll i) {if (i == 1) return 1; return (mod - ((mod / i) * inv(mod % i)) % mod) % mod;}

ll mod_mul(ll a, ll b) {a = a % mod; b = b % mod; return (((a * b) % mod) + mod) % mod;}

ll mod_add(ll a, ll b) {a = a % mod; b = b % mod; return (((a + b) % mod) + mod) % mod;}

ll gcd(ll a, ll b) { if (b == 0) return a; return gcd(b, a % b);}

ll lcm(ll a, ll b) {return (a / gcd(a, b)) * b;}

ll ceil_div(ll a, ll b) {return a % b == 0 ? a / b : a / b + 1;}

long long pwr(long long n, long long mod) {
    long long result = 1;
    long long base = 2;

    while (n > 0) {
        if (n % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        n /= 2;
    }
    return result;
}

void reverseStr(string& str, int n, int i)
{
    if(n<=i){return;}
    swap(str[i],str[n]);
    reverseStr(str,n-1,i+1);
}

bool cmp(pair<int,int> a, pair<int,int> b){
    if(a.first == b.first){
        return a.second < b.second;
    }
    return a.first < b.first;
}

int cnt(string s, string a, int len){
    int ans=0;
    for(int i = 0 ; i < len; i++){
        if(a[i] == s[i]){
            ans++;
        }
    }
    return ans;
}

void solve()
{
    ll l1, b1, l2, b2, l3, b3;
    cin>>l1>>b1>>l2>>b2>>l3>>b3;
    if(l1 == l2 && l2 == l3 && b1 == b2 && b2 == b3){
        cout<<"YES\n";
        return;
    }
    if(l1 == l2 && l2 == l3){
        if(b1 == b2 && b2 == b3){
            cout<<"NO\n";
            return;
        }
        if(b1 == b2){
            if(l3 <= b1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(b2 == b3){
            if(l3 <= b2){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(b1 == b3){
            if(l3 <= b1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
    }
    if(b1 == b2 && b2 == b3){
        if(l1 == l2 && l2 == l3){
            cout<<"NO\n";
            return;
        }
        if(l1 == l2){
            if(b3 <= l1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(l2 == l3){
            if(b3 <= l2){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(l1 == l3){
            if(b3 <= l1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
    }
    if(l1 == l3 && l3 == l2){
        if(b1 == b2 && b2 == b3){
            cout<<"NO\n";
            return;
        }
        if(b1 == b2){
            if(l2 <= b1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(b2 == b3){
            if(l2 <= b2){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(b1 == b3){
            if(l2 <= b1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
    }
    if(b1 == b3 && b3 == b2){
        if(l1 == l2 && l2 == l3){
            cout<<"NO\n";
            return;
        }
        if(l1 == l2){
            if(b2 <= l1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(l2 == l3){
            if(b2 <= l2){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
        if(l1 == l3){
            if(b2 <= l1){
                cout<<"YES\n";
                return;
            }
            else{
                cout<<"NO\n";
                return;
            }
        }
    }
    cout<<"NO\n";
}

int main()
{
    fast_io;
    int z;
    cin >> z;
    while(z--){
        solve();
    }
}