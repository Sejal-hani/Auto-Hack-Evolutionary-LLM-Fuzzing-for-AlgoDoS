// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 1000000 (sieve/z array bound)
// [INPUT_FORMAT]: T; per case: two scalar integers X, M. 
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
#include <math.h>
#include <numeric>
#include <limits>
#include <queue>
#include <deque>
using namespace std;
typedef long long lli;
#define pb push_back
#define db double
#define UB upper_bound
#define LB lower_bound
#define MP make_pair
#define PI pair<lli,lli>
#define INF numeric_limits<lli>::max()
//constants
const lli maxn = 1e6 + 5;
const lli mod = 998244353;
vector<lli> z[maxn + 5];
void solve() {
	lli x, m;
	cin >> x >> m;
	lli ans = 0;
	lli gam = (1 << (lli)(ceil(log2(x + 1))));
	for (lli i = 1; i <= min(m, gam - 1); i++) {
		if ((i ^ x) != 0) {
			if (x % (i ^ x) == 0 or i % (i ^ x) == 0) {
				ans++;
			}
		}
	}
	map<lli, lli> an;
	if (m > gam) {
		for (lli mask = 0; mask < gam; mask++) {
			lli s = -(x - 2 * (mask & x));
			if (s >= 0) {
				if (an.find(s) == an.end()) {
					lli w = 0;
					for (auto v : z[s]) {
						lli o = s / v * (v + 1);
						if (o % gam == mask and o >= gam and o <= m) {
							w++;
						}
					}
					ans += w;
					an.insert(MP(s, w));
				}
				else {
					ans += an[s];
				}
			}
		}
	}
	cout << ans << endl;
}
int main() {
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	lli op = 0;
	for (lli i = 1; i <= maxn; i++) {
		lli j = 1;
		for(lli j=1;i*j<=maxn;j++) {
			op++;
			z[i * j].pb(i);
		}
	}//cout << op << endl;
	lli t;
	cin >> t;
	while (t--)solve();
}