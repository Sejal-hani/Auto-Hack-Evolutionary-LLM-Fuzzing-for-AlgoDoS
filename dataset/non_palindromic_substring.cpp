// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T, followed by T test cases. Each test case contains two integers N and Q, a string S, and Q queries, each consisting of two integers L and R.
#include <iostream>
#include <string>
using namespace std;

#define int long long

int color_[200010], color_0[200010], color_1[200010];
int MOD = 1991122547ll, MOD2 = 1991122577ll, MOD3 = 1991122577ll, MOD4 = 1926081733ll;
int MOD5, MOD6;
unsigned int hash_sum1[200010], hash_sum2[200010], hash_suf1[200010], hash_suf2[200010];
unsigned int hash_sum3[200010], hash_sum4[200010], hash_suf3[200010], hash_suf4[200010];
unsigned int hash_sum5[200010], hash_sum6[200010], hash_suf5[200010], hash_suf6[200010];
unsigned int p1[200010], p2[200010], p3[200010], p4[200010], p5[200010], p6[200010];
int n, q;

bool ck(int l, int r) {
    return 1 ^ (((hash_sum1[r] - hash_sum1[l - 1] * p1[r - l + 1] % MOD + MOD) % MOD == (hash_suf1[l] - hash_suf1[r + 1] * p1[r - l + 1] % MOD + MOD) % MOD) &&
                ((hash_sum2[r] - hash_sum2[l - 1] * p2[r - l + 1] % MOD2 + MOD2) % MOD2 == (hash_suf2[l] - hash_suf2[r + 1] * p2[r - l + 1] % MOD2 + MOD2) % MOD2) &&
                ((hash_sum3[r] - hash_sum3[l - 1] * p3[r - l + 1] % MOD3 + MOD3) % MOD3 == (hash_suf3[l] - hash_suf3[r + 1] * p3[r - l + 1] % MOD3 + MOD3) % MOD3) &&
                ((hash_sum4[r] - hash_sum4[l - 1] * p4[r - l + 1] % MOD4 + MOD4) % MOD4 == (hash_suf4[l] - hash_suf4[r + 1] * p4[r - l + 1] % MOD4 + MOD4) % MOD4) &&
                ((hash_sum5[r] - hash_sum5[l - 1] * p5[r - l + 1] % MOD5 + MOD5) % MOD5 == (hash_suf5[l] - hash_suf5[r + 1] * p5[r - l + 1] % MOD5 + MOD5) % MOD5) &&
                ((hash_sum6[r] - hash_sum6[l - 1] * p6[r - l + 1] % MOD6 + MOD6) % MOD6 == (hash_suf6[l] - hash_suf6[r + 1] * p6[r - l + 1] % MOD6 + MOD6) % MOD6));
}

void work() {
    string s;
    cin >> n >> q >> s;
    s = ' ' + s;
    for (int i = 1; i <= n + 1; i++) {
        color_0[i] = color_1[i] = color_[i] = 0;
        hash_suf1[i] = hash_suf2[i] = hash_suf3[i] = hash_suf4[i] = hash_suf5[i] = hash_suf6[i] = 0;
        hash_sum1[i] = hash_sum2[i] = hash_sum3[i] = hash_sum4[i] = hash_sum5[i] = hash_sum6[i] = 0;
    }
    for (int i = 1; i <= n; i++) {
        color_[i] = color_[i - 1] + (s[i] != s[i - 1] ? 1 : 0);
    }
    for (int i = 1; i <= n; i++) {
        if (i == 1) color_1[i] = 1;
        else color_1[i] = color_1[i - 2] + (s[i] != s[i - 2] ? 1 : 0);
    }
    unsigned int base = 26;
    for (int i = 1; i <= n; i++) {
        hash_sum1[i] = (base * hash_sum1[i - 1] + s[i] - 'a') % MOD;
        hash_sum2[i] = (base * hash_sum2[i - 1] + s[i] - 'a') % MOD2;
        hash_sum3[i] = (base * hash_sum3[i - 1] + s[i] - 'a') % MOD3;
        hash_sum4[i] = (base * hash_sum4[i - 1] + s[i] - 'a') % MOD4;
        hash_sum5[i] = (base * hash_sum5[i - 1] + s[i] - 'a') % MOD5;
        hash_sum6[i] = (base * hash_sum6[i - 1] + s[i] - 'a') % MOD6;
    }
    for (int i = n; i >= 1; i--) {
        hash_suf1[i] = (base * hash_suf1[i + 1] + s[i] - 'a') % MOD;
        hash_suf2[i] = (base * hash_suf2[i + 1] + s[i] - 'a') % MOD2;
        hash_suf3[i] = (base * hash_suf3[i + 1] + s[i] - 'a') % MOD3;
        hash_suf4[i] = (base * hash_suf4[i + 1] + s[i] - 'a') % MOD4;
        hash_suf5[i] = (base * hash_suf5[i + 1] + s[i] - 'a') % MOD5;
        hash_suf6[i] = (base * hash_suf6[i + 1] + s[i] - 'a') % MOD6;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        if (color_[l] == color_[r]) { cout << 0 << endl; continue; }
        int cl1, cl0, cr1, cr0;
        if (l & 1) { cl1 = color_1[l]; cl0 = color_1[l + 1]; }
        else { cl0 = color_1[l]; cl1 = color_1[l + 1]; }
        if (r & 1) { cr1 = color_1[r]; cr0 = color_1[r - 1]; }
        else { cr0 = color_1[r]; cr1 = color_1[r - 1]; }

        if (cl0 == cr0 && cl1 == cr1) {
            int ans = (2 + (r - l + 1) / 2 * 2) * ((r - l + 1) / 2) / 2;
            if ((r - l + 1) & 1) ans += ck(l, r) * (r - l + 1);
            cout << ans << endl;
            continue;
        }
        int ans = (2 + (r - l)) * (r - l - 1) / 2;
        ans += ck(l, r) * (r - l + 1);
        cout << ans << endl;
    }
}

int main() {
    p1[0] = p2[0] = p3[0] = p4[0] = p5[0] = p6[0] = 1;
    for (int i = 1; i <= 200000; i++) {
        p1[i] = (p1[i - 1] * 26) % MOD;
        p2[i] = (p2[i - 1] * 26) % MOD2;
        p3[i] = (p3[i - 1] * 26) % MOD3;
        p4[i] = (p4[i - 1] * 26) % MOD4;
        p5[i] = (p5[i - 1] * 26) % MOD5;
        p6[i] = (p6[i - 1] * 26) % MOD6;
    }
    int t; cin >> t;
    while (t--) work();
    return 0;
}