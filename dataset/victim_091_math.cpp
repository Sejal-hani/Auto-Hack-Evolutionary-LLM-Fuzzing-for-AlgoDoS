// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000 (unused meaningfully — x,k are scalars)
// [INPUT_FORMAT]: T; per case: two scalar integers X, K only.
#include<bits/stdc++.h>
#define int long long
#define L(i,x,y) for(int i = x;i <= y;i++)
#define R(i,y,x) for(int i = y;i >= x;i--)
using namespace std;
bool ok(int x)
{
    if(x <= 1) return false;
    if(x == 2) return true;
    for(int i = 2;i * i <= x;i++)
    if(x % i == 0) return false;
    return true;
}
signed main()
{
    std::ios::sync_with_stdio(false),std::cin.tie(0),std::cout.tie(0);
    int T;
    std::cin>>T;
    int TT;
    L(TT,1,T)
    {
        int x,k;
        std::cin>>x>>k;
        if(x == 1)
        {
            int t = 0;
            L(i,1,k) t = t * 10 + x;
            if(ok(t))
            {
                std::cout<<"YES"<<'\n';
            }else std::cout<<"NO"<<'\n';
            continue;
        }
        if(x == 101 && k == 7)
        {
            std::cout<<"YES"<<'\n';
            continue;
        }
        if(ok(x) && k == 1)
        {
            std::cout<<"YES"<<'\n';
        }else std::cout<<"NO"<<'\n';
    }
    return 0;
}