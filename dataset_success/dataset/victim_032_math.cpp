// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T (int Ti); per case: N, then two arrays p[N] and s[N]. No K/string.
#include "bits/stdc++.h"
using namespace std;
using ll = __INT64_TYPE__;

ll gcd(ll a, ll b) {
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a;
}

ll lcm(ll a, ll b) {
    return a / gcd(a, b) * b;
}

void run_case() {
  int n; cin >> n;
  vector<int> p(n), s(n);
  for(int& i:p) cin >> i;
  for(int& i:s) cin >> i;

  vector<int> a(n);
  for (int i = 0; i < n; i++) {
    a[i] = lcm(p[i], s[i]);
  }

  int pref = 0;
  int suf = 0;

  for (int i = 0; i < n; ++i) {
    pref = gcd(a[i], pref);
    suf = gcd(suf, a[n - 1 - i]);

    if (pref != p[i] || suf != s[n - 1 - i]) {
      std::cout << "NO\n"; return;
    }
  }

  std::cout << "YES\n";
  return;
}

__INT32_TYPE__ main () {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);
  std::cout.tie(nullptr);
  int Ti = 1;
  std::cin >> Ti;
  for (int i = 1; i <= Ti; i++) {
    std::cerr << "Case #" << i << '\n';
    run_case();
    std::cerr << "\n-----------------\n";
  }
  return EXIT_SUCCESS;
}