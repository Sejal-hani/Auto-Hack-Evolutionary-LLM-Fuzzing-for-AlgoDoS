// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 300005
// [INPUT_FORMAT]: T; per case: N, then array a[1..N]. No K/string.
#include <bits/stdc++.h>

#define int long long

const int mod = 998244353;
const int inv2 = (mod + 1) / 2;

void add(int &x, int y) {
    x += y;
    if (x >= mod) x -= mod;
}

const int N = 3e5;

int n;
int a[N + 5];

struct segment_tree {
    struct Segment_tree {
        int l, r, sum, mul, add;
    } tree[N * 4 + 5];

    #define lc (p << 1)
    #define rc (p << 1 | 1)

    void pushup(int p) {
        tree[p].sum = (tree[lc].sum + tree[rc].sum) % mod;
    }

    void pushdown(int p) {
        if (tree[p].l == tree[p].r) return;
        tree[lc].sum = (tree[lc].sum * tree[p].mul % mod + tree[p].add * (tree[lc].r - tree[lc].l + 1) % mod) % mod;
        tree[lc].mul = tree[lc].mul * tree[p].mul % mod; 
        tree[lc].add = (tree[lc].add * tree[p].mul % mod + tree[p].add) % mod;
        tree[rc].sum = (tree[rc].sum * tree[p].mul % mod + tree[p].add * (tree[rc].r - tree[rc].l + 1) % mod) % mod;
        tree[rc].mul = tree[rc].mul * tree[p].mul % mod; 
        tree[rc].add = (tree[rc].add * tree[p].mul % mod + tree[p].add) % mod;
        tree[p].mul = 1; 
        tree[p].add = 0;
    }

    void build(int p, int l, int r) {
        int mid = l + r >> 1;
        tree[p].l = l; 
        tree[p].r = r; 
        tree[p].mul = 1;
        tree[p].sum = 0; 
        tree[p].add = 0;
        if (l == r) { 
            tree[p].sum = 0; 
            return; 
        }
        build(lc, l, mid); 
        build(rc, mid + 1, r); 
        pushup(p);
    }

    void update1(int p, int ql, int qr, int k) {
        if (ql <= tree[p].l && tree[p].r <= qr) {
            tree[p].sum = tree[p].sum * k % mod;
            tree[p].mul = tree[p].mul * k % mod;
            tree[p].add = tree[p].add * k % mod;
            return;
        }
        pushdown(p);
        int mid = tree[p].l + tree[p].r >> 1;
        if (ql <= mid) update1(lc, ql, qr, k);
        if (qr >= mid + 1) update1(rc, ql, qr, k);
        pushup(p);
    }

    void update2(int p, int ql, int qr, int k) {
        if (ql <= tree[p].l && tree[p].r <= qr) {
            tree[p].sum = (tree[p].sum + k * (tree[p].r - tree[p].l + 1) % mod) % mod;
            tree[p].add = (tree[p].add + k) % mod;
            return;
        }
        pushdown(p);
        int mid = tree[p].l + tree[p].r >> 1;
        if (ql <= mid) update2(lc, ql, qr, k);
        if (qr >= mid + 1) update2(rc, ql, qr, k);
        pushup(p);
    }

    int query(int p, int ql, int qr) {
        if (ql > qr) return 0;
        if (ql == 0 && qr == 0) return 1;
        if (ql <= tree[p].l && tree[p].r <= qr) return tree[p].sum;
        pushdown(p);
        int mid = tree[p].l + tree[p].r >> 1, sum = 0;
        if (ql <= mid) sum = (sum + query(lc, ql, qr)) % mod;
        if (qr >= mid + 1) sum = (sum + query(rc, ql, qr)) % mod;
        return sum;
    }
} L, R;

int l[N + 5], ll;
int r[N + 5], rr;

void solve() {
    std::cin >> n;
    for (int i = 1; i <= n; i++) {
        std::cin >> a[i];
    }

    ll = rr = 0;
    for (int i = 1; i <= n; i++) {
        if (a[i] > l[ll]) l[++ll] = a[i];
    }
    for (int i = n; i >= 1; i--) {
        if (a[i] > r[rr]) r[++rr] = a[i];
    }

    L.build(1, 1, ll);
    R.build(1, 1, rr);

    for (int i = 1; i <= n; i++) {
        int idl = std::lower_bound(l + 1, l + ll + 1, a[i]) - l;
        L.update1(1, idl, ll, 2);
        if (l[idl] == a[i]) L.update2(1, idl, idl, L.query(1, idl - 1, idl - 1));
    }

    int ans = 0;
    for (int i = n; i >= 1; i--) {
        int idl = std::lower_bound(l + 1, l + ll + 1, a[i]) - l;
        int idr = std::lower_bound(r + 1, r + rr + 1, a[i]) - r;
        if (l[idl] == a[i]) L.update2(1, idl, idl, (mod - L.query(1, idl - 1, idl - 1)) % mod);
        L.update1(1, idl, ll, inv2);
        if (a[i] == l[ll]) {
            add(ans, (long long)L.query(1, idl - 1, idl - 1) * (R.query(1, idr - 1, idr - 1) + R.query(1, idr, idr)) % mod);
        }
        R.update1(1, idr, rr, 2);
        if (r[idr] == a[i]) R.update2(1, idr, idr, R.query(1, idr - 1, idr - 1));
    }

    std::cout << ans << "\n";
}

signed main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t = 0;
    std::cin >> t;

    while (t--) {
        solve();
    }

    return 0;
}