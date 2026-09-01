// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers

#include<bits/stdc++.h>
using namespace std;
const int lg=30,maxn=2*(200000+10);
int n,k,all[maxn];

struct trie{
    int cnt[maxn*lg],cl[maxn*lg],cr[maxn*lg];
    int te=1;
    void clear(){
        for(int i=0;i<te;i++){
            cl[i]=cr[i]=0;
            cnt[i]=0;
        }
        te=1;
    }
    int getr(int u){
        if(cr[u]==0){
            cr[u]=te;
            te++;
        }
        return cr[u];
    }
    int getl(int u){
        if(cl[u]==0){
            cl[u]=te;
            te++;
        }
        return cl[u];
    }
    void upd(int val,int w){
        int u=0;
        for(int i=lg;i>=0;i--){
            cnt[u]+=w;
            if((val>>i)&1){
                u=getr(u);
            }else{
                u=getl(u);
            }
        }
        cnt[u]+=w;
    }
    int getmx(int w){
        int res=0;
        int u=0;
        if(cnt[u]==0){
            return -1;
        }
        for(int i=lg;i>=0;i--){
            if((w>>i)&1){
                if(cl[u]!=0&&cnt[cl[u]]>0){
                    res+=(1ll<<i);
                    u=cl[u];
                    continue;
                }
                u=cr[u];
            }else{
                if(cr[u]!=0&&cnt[cr[u]]>0){
                    res+=(1ll<<i);
                    u=cr[u];
                    continue;
                }
                u=cl[u];
            }
        }
        return res;
    }
}trie;

bool check(int mid){
    trie.clear();
    for(int i=1;i<=mid;i++){
        trie.upd(all[i],1);
        if(trie.getmx(all[i])>=k){
            return 1;
        }
    }
    for(int i=mid+1;i<=n;i++){
        trie.upd(all[i-mid],-1);
        trie.upd(all[i],1);
        if(trie.getmx(all[i])>=k){
            return 1;
        }
    }
    return 0;
}

void solve(){
    cin>>n>>k;
    for(int i=1;i<=n;i++){
        cin>>all[i];
    }
    int low=0,high=n+1,mid;
    while(high-low>1){
        mid=(high+low)>>1;
        if(check(mid)){
            high=mid;
        }else{
            low=mid;
        }
    }
    if(high==n+1){
        cout<<-1<<"\n";
        return;
    }
    cout<<high<<"\n";
    trie.clear();
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    int t=1;
    cin>>t;
    for(int asd=0;asd<t;asd++){
        solve();        
    }
}