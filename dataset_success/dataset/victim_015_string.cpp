// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: T; per case: string S only.
#include <bits/stdc++.h>
#define ll long long
using namespace std;

void print(vector<int>v){for(int c:v) cout<<c<<",";cout<<endl;}
void printv2(vector<vector<int>>v){for(vector<int> c:v) cout<<c[0]<<" "<<c[1]<<"|";cout<<endl;}
const ll mod = 998244353;

int main()
{
   int tt;
   cin>>tt;
   while(tt--)
   {
       string s;
       cin>>s;
       int n = s.size();
       string res = "-1";
       auto verifier = [&](int pos, string s)
       {
           if(pos<n-1)
           {
               if(s[pos]==s[pos+1])
               {
                   return 2;
               }
           }
           if(pos<n-2)
           {
               if(s[pos]!=s[pos+1] && s[pos]!=s[pos+2] && s[pos+1]!=s[pos+2])
               {
                   return 3;
               }
           }
           return -1;
       };
       for(int i=0; i<n; i++)
       {
           int help=verifier(i, s);
           if(help!=-1)
           {
               res=s.substr(i, help);
               break;
           }
       }
       cout<<res<<endl;
   }
}