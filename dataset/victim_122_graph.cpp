// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 500000
// [INPUT_FORMAT]: T; per case: N, then N-1 parent integers j. No K/string; also code references undeclared identifier `st` (will not compile).#include <bits/stdc++.h>

using namespace std;
#include <bits/stdc++.h>

const int N = 5e5 + 5;

int n;
vector<int> kids[N];
int parent[N];
int whole_sz[N], whole_time[N], depth[N];
array<int, 20> up[N];

struct Fenwick {
    vector<int> bit;

    Fenwick(int n = 0) {
        bit.assign(n + 5, 0);
    }

    void add(int idx, int val) {
        idx++;
        while (idx < (int)bit.size()) {
            bit[idx] += val;
            idx += idx & -idx;
        }
    }

    int sumPrefix(int idx) {
        int res = 0;
        while (idx > 0) {
            res += bit[idx];
            idx -= idx & -idx;
        }
        return res;
    }

    int sum(int l, int r) {
        return sumPrefix(r) - sumPrefix(l);
    }
};

Fenwick st;

int dfs(int u, int time) {
    whole_sz[u] = 1;
    whole_time[u] = time;
    depth[u] = depth[parent[u]] + 1;

    up[u][0] = parent[u];
    for (int i = 0; i + 1 < 20; i++)
        up[u][i + 1] = up[up[u][i]][i];

    for (int v : kids[u])
        whole_sz[u] += dfs(v, time + 1);

    return whole_sz[u];
}

int find_kid(int below, int above) {
    if (depth[below] <= depth[above])
        return -1;

    for (int i = 19; i >= 0; i--) {
        if (depth[up[below][i]] <= depth[above])
            continue;
        below = up[below][i];
    }

    if (up[below][0] != above)
        return -1;

    return below;
}

int sz(int u) {
    int l = whole_time[u];
    int r = whole_time[u] + whole_sz[u];
    return l + r - 2 * st.sum(l, r);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        cin >> n;

        for (int i = 0; i < n; i++) {
            kids[i].clear();
            parent[i] = 0;
            depth[i] = 0;
            whole_sz[i] = 0;
            whole_time[i] = 0;
            up[i].fill(0);
        }

        for (int i = 1; i < n; i++) {
            int j;
            cin >> j;
            --j;
            kids[j].push_back(i);
            parent[i] = j;
        }

        st = Fenwick(n + 5);

        dfs(0, 0);

        int centroid = 0;

        st.add(0, 1);

        int last_centroid = 0;
        int last_mx = 0;

        for (int i = 1; i < n; i++) {
            st.add(whole_time[i], 1);

            while (centroid != 0 && sz(centroid) * 2 < i + 1)
                centroid = parent[centroid];

            int v;
            while ((v = find_kid(i, centroid)) != -1) {
                if (sz(v) * 2 >= i + 1)
                    centroid = v;
                else
                    break;
            }

            int mx;

            if (last_centroid != centroid) {
                mx = (i + 1) - sz(centroid);

                for (int child : kids[centroid])
                    mx = max(mx, sz(child));

                last_centroid = centroid;
            } else {
                mx = last_mx;

                int check = find_kid(i, centroid);

                if (check != -1)
                    mx = max(mx, sz(check));
                else
                    mx = max(mx, (i + 1) - sz(centroid));
            }

            last_mx = mx;

            cout << (i + 1) - 2 * mx << " \n"[i == n - 1];
        }

        for (int i = 0; i < n; i++)
            st.add(whole_time[i], -1);
    }

    return 0;
}