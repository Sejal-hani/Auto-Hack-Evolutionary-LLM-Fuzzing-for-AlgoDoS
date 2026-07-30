// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: Single case, no T loop: N, M, then array a[1..N], then M queries k_queries[i].
#include <bits/stdc++.h>

using namespace std;

static const int MOD = 998244353;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

struct Element {
    long long v;
    long long c;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    vector<pair<long long, int>> k_queries(m);
    for (int i = 0; i < m; i++) {
        cin >> k_queries[i].first;
        k_queries[i].second = i;
    }

    vector<int> L(n + 1), R(n + 1);
    vector<int> st;

    for (int i = 1; i <= n; i++) {
        while (!st.empty() && a[st.back()] >= a[i]) {
            st.pop_back();
        }
        L[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }

    st.clear();
    for (int i = n; i >= 1; i--) {
        while (!st.empty() && a[st.back()] > a[i]) {
            st.pop_back();
        }
        R[i] = st.empty() ? n + 1 : st.back();
        st.push_back(i);
    }

    long long base_sum = 0;
    vector<Element> elems(n);

    for (int i = 1; i <= n; i++) {
        long long inv_a = modInverse(a[i]);
        long long subarray_count = (1LL * i * (n - i + 1)) % MOD;
        base_sum = (base_sum + subarray_count * inv_a) % MOD;

        long long c = (1LL * (i - L[i]) % MOD) * ((R[i] - i) % MOD) % MOD;
        elems[i - 1] = {a[i], c};
    }

    sort(elems.begin(), elems.end(), [](const Element& x, const Element& y) {
        return x.v < y.v;
    });

    long long S_gt_inv = 0;
    for (int i = 0; i < n; i++) {
        long long inv_v = modInverse(elems[i].v);
        S_gt_inv = (S_gt_inv + elems[i].c * inv_v) % MOD;
    }

    long long S_le_one = 0;
    long long S_le_rest = 0;

    vector<long long> ans(m);
    int ptr = 0;

    for (int i = 0; i < m; i++) {
        long long k = k_queries[i].first;

        while (ptr < n && elems[ptr].v <= k) {
            long long v = elems[ptr].v;
            long long c = elems[ptr].c;
            long long inv_v = modInverse(v);

            S_gt_inv = (S_gt_inv - c * inv_v % MOD + MOD) % MOD;
            S_le_one = (S_le_one + c) % MOD;

            long long rest_term = (2 - (v % MOD) - inv_v) % MOD;
            if (rest_term < 0) rest_term += MOD;

            S_le_rest = (S_le_rest + c * rest_term) % MOD;

            ptr++;
        }

        long long k_mod = k % MOD;
        long long cur_ans = base_sum;
        cur_ans = (cur_ans + k_mod * S_gt_inv) % MOD;
        cur_ans = (cur_ans + k_mod * S_le_one) % MOD;
        cur_ans = (cur_ans + S_le_rest) % MOD;

        ans[k_queries[i].second] = cur_ans;
    }

    for (int i = 0; i < m; i++) {
        cout << ans[i] << "\n";
    }

    return 0;
}