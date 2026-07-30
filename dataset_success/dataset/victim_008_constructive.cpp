// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: four scalar integers N, K, B, S. No array or string is read.
#include <bits/stdc++.h>
using namespace std;
#define IOS ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL);
#define pb push_back
#define int long long int

signed main()
{
    IOS
    int t;

    cin >> t;
    while (t--)
    {
        int n, k, b, s;
        cin >> n >> k >> b >> s;

        if (k == 1)
        {
            if (n < s)
            {
                cout << -1 << endl;
            }
            else
            {
                for (int i = 0; i < n - 1; i++)
                {
                    cout << 0 << " ";
                }
                cout << s << endl;
            }
        }
        else
        {
            int xx = min(s, k * (b) + k - 1);
            int yy = ((s - xx) / (k - 1));
            int z = (s - xx) % (k - 1);
            int c = (z == 0) ? 0 : 1;
            if (k * b > s)
            {
                cout << -1 << endl;
            }
            else if (yy + 1 + c > n)
            {
                cout << -1 << endl;
            }
            else
            {
                for (int i = 0; i < yy; i++)
                {
                    cout << k - 1 << " ";
                }
                if (c) cout << (s - xx) % (k - 1) << " ";
                for (int i = yy + c; i < n - 1; i++)
                {
                    cout << 0 << " ";
                }
                cout << xx << endl;
            }
        }
    }
    return 0;
}