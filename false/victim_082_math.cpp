// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200005
// [INPUT_FORMAT]: T; per case: N, Q (via undefined read_int() calls — code will not compile), then Q pairs (a,b).
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAXN = 200005;
const int MAX_SQRT = 448;

struct info_item {
    int certain_mask = 0;
    vector<array<int, 2>> diff_pairs;
    vector<array<int, 3>> pos_trips;
    vector<array<int, 3>> neg_trips;
};

inline int read_int() {
    int x;
    cin >> x;
    return x;
}


info_item infos[MAXN];

void precase_init() {
    for (int i = 1; i <= MAX_SQRT; i++) {
        int i_sq = i * i;
        infos[i_sq].certain_mask |= 1;
        for (int j = i; j <= MAX_SQRT; j++) {
            int j_sq = j * j;
            {
                int sum = i_sq + j_sq;
                if (sum < MAXN) {
                    if (!(infos[sum].certain_mask & 3)) {
                        infos[sum].pos_trips = {};
                        infos[sum].neg_trips = {};
                        infos[sum].diff_pairs = {};
                        infos[sum].certain_mask |= 2;
                    }
                }
                int diff = j_sq - i_sq;
                if (!(infos[diff].certain_mask & 3)) {
                    infos[diff].diff_pairs.push_back({i_sq, j_sq});
                }
            }
            for (int k = j; k <= MAX_SQRT; k++) {
                int k_sq = k * k;
                int sum = i_sq + j_sq + k_sq;
                if (sum < MAXN) {
                    if (!infos[sum].certain_mask) {
                        infos[sum].pos_trips = {};
                        infos[sum].neg_trips = {};
                        infos[sum].certain_mask |= 4;
                    }
                }
                int diff1 = k_sq - j_sq - i_sq;
                if (diff1 > 0) {
                    if (!infos[diff1].certain_mask) {
                        infos[diff1].neg_trips.push_back({i_sq, j_sq, k_sq});
                    }
                } else {
                    if (!infos[-diff1].certain_mask) {
                        infos[-diff1].pos_trips.push_back({k_sq, i_sq, j_sq});
                    }
                }
                int diff2 = k_sq + j_sq - i_sq;
                if (diff2 < MAXN) {
                    if (!infos[diff2].certain_mask) {
                        infos[diff2].pos_trips.push_back({i_sq, j_sq, k_sq});
                    }
                }
                int diff3 = k_sq - j_sq + i_sq;
                if (diff3 < MAXN) {
                    if (!infos[diff3].certain_mask) {
                        infos[diff3].pos_trips.push_back({j_sq, i_sq, k_sq});
                    }
                }
            }
        }
    }
}

inline int read_int() {
    int x;
    cin >> x;
    return x;
}


void solve() {
    int n = read_int();
    int q = read_int();
    for (int i = 0; i < q; i++) {
        int a = read_int();
        int b = read_int();
        if (a > b) swap(a, b);
        int d = b - a;
        if (infos[d].certain_mask & 1) {
            cout << 1 << endl;
            continue;
        }
        if (infos[d].certain_mask & 2) {
            cout << 2 << endl;
            continue;
        }
        bool done = false;
        for (auto [x, y] : infos[d].diff_pairs) {
            if (a - x > 0 || b + x <= n) {
                cout << 2 << endl;
                done = true;
                break;
            }
        }
        if (done) continue;
        if (infos[d].certain_mask & 4) {
            cout << 3 << endl;
            continue;
        }
        for (auto [x, y, z] : infos[d].pos_trips) {
            if (a - x > 0 || a + y + z <= n || (a + y - x > 0 && a + y <= n) || (a + z - x > 0 && a + z <= n)) {
                cout << 3 << endl;
                done = true;
                break;
            }
        }
        if (done) continue;
        for (auto [x, y, z] : infos[d].neg_trips) {
            if (a - x - y > 0 || a + z <= n || (a - x > 0 && a - x + z <= n) || (a - y > 0 && a - y + z <= n)) {
                cout << 3 << endl;
                done = true;
                break;
            }
        }
        if (done) continue;
        cout << 4 << endl;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    precase_init();
    int t = 1;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}