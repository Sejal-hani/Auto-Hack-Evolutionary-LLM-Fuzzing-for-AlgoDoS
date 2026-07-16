// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: Three integers N M D, followed by M integers, then N-1 pairs of integers
#include <iostream>
#include <set>
#include <vector>

using namespace std;

vector<int> adj[100009];
int dist1[100009], dist2[100009];
bool affected[100009];
int n, m, d;

void dfs(int v, int p, int dist[], int &farthest_node) {
    if (affected[v] && (farthest_node == -1 || dist[v] > dist[farthest_node])) {
        farthest_node = v;
    }
    for (int u : adj[v]) {
        if (u != p) {
            dist[u] = dist[v] + 1;
            dfs(u, v, dist, farthest_node);
        }
    }
}

int main() {
    cin >> n >> m >> d;
    int start_node = -1;
    for (int i = 0; i < m; ++i) {
        int p;
        cin >> p;
        affected[p] = true;
        start_node = p;
    }
    for (int i = 1; i < n; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    int node1 = -1, node2 = -1;
    vector<int> d0(n + 1, 0), d1(n + 1, 0), d2(n + 1, 0);

    dfs(start_node, 0, &d0[0], node1);
    
    fill(d1.begin(), d1.end(), 0);
    int dummy = -1;
    dfs(node1, 0, &d1[0], node2);

    fill(d2.begin(), d2.end(), 0);
    dfs(node2, 0, &d2[0], dummy);

    int count = 0;
    for (int i = 1; i <= n; i++) {
        if (d1[i] <= d && d2[i] <= d) {
            count++;
        }
    }

    cout << count << endl;
    return 0;
}