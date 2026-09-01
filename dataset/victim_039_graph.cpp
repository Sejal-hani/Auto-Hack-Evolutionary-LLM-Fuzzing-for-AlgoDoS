// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then N-1 edges (x,y). degTwoVert is computed, never read

#include <iostream>
#include <set>
#include <vector>

using namespace std;

int main() {
    int t;
    cin >> t;

    for (int i = 0; i < t; i++) {
        int n;
        cin >> n;

        vector<vector<int>> tree(n + 1);
        for (int j = 0; j < n - 1; j++) {
            int x, y;
            cin >> x >> y;
            tree[x].push_back(y);
            tree[y].push_back(x);
        }

        if (n == 2) {
            cout << "NO" << endl;
            continue;
        }

        int degTwoVert = -1;
        for (int j = 1; j <= n; j++) {
            if (tree[j].size() == 2) {
                degTwoVert = j;
                break;
            }
        }

        if (degTwoVert == -1) {
            cout << "NO" << endl;
            continue;
        }

        int a = tree[degTwoVert][0];
        int b = tree[degTwoVert][1];
        cout << "YES" << endl;
        cout << a << " " << degTwoVert << endl;
        cout << degTwoVert << " " << b << endl;

        vector<pair<int, int>> toVisit = {{a, 1}, {b, -1}};
        set<int> visited = {degTwoVert};

        while (!toVisit.empty()) {
            pair<int, int> vertDir = toVisit.back();
            toVisit.pop_back();
            int vert = vertDir.first;
            int dir = vertDir.second;

            if (visited.find(vert) != visited.end()) {
                continue;
            }

            visited.insert(vert);

            for (int neighbor : tree[vert]) {
                if (visited.find(neighbor) != visited.end()) {
                    continue;
                }

                if (dir == 1) {
                    cout << vert << " " << neighbor << endl;
                } else {
                    cout << neighbor << " " << vert << endl;
                }

                toVisit.push_back({neighbor, dir});
            }
        }
    }

    return 0;
}