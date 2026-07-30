// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000 (factorial precompute bound)
// [INPUT_FORMAT]: T; per case: three scalar integers A, B, K. No array or string.
#include <bits/stdc++.h>
using namespace std;

#define ll long long 
#define pii pair <int, int>
#define fi first
#define se second

const int MOD = 1e9 + 7, MAXN = 1e5 + 5;

int iz, arr[MAXN];

int add(int a, int b) {
	return (1LL * a + b + MOD) % MOD;
}

int mul(int a, int b) {
	return (1LL * a * b) % MOD;
}

int pot(int a, int b) {
	int rj = 1;
	for (int i = 0; i <= 30; i++) {
		if (b & (1 << i)) rj = mul(rj, a);
		a = mul(a, a);
	}
	return rj;
}

int divv(int a, int b) {
	return mul(a, pot(b, MOD - 2)) % MOD;
}

int povrh(int n, int k) {
	return divv(iz, arr[k]); 
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(0);
	
	int t, a, b, k;
	cin >> t;
	
	arr[1] = 1;
	for (int i = 2; i < MAXN; i++) arr[i] = mul(arr[i - 1], i);
	
	while (t--) {
		cin >> a >> b >> k;
		int n = add(mul((a - 1), k), 1);
		
		iz = 1;
		for (int i = n - a + 1; i <= n; i++) iz = mul(iz, i);
		
		int m = mul(mul(k, povrh(n, a)), (b - 1)) + 1;
		cout << n << " " << m << "\n";
	}
	
	return 0;
}