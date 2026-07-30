// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 55 (grid array bound)
// [INPUT_FORMAT]: T; per case: N, M, then N×M grid characters ('.' or '#').
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

const int MAX_N = 55;
const int MAX_M = 55;

int n, m;
char grid[MAX_N][MAX_M];
int dx[] = {-1, 0, 1, 0};
int dy[] = {0, -1, 0, 1};

void dfs(int x, int y) {
    grid[x][y] = '#';
    for (int i = 0; i < 4; i++) {
        int nx = x + dx[i];
        int ny = y + dy[i];
        if (nx >= 1 && nx <= n && ny >= 1 && ny <= m && grid[nx][ny] == '.') {
            dfs(nx, ny);
        }
    }
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> grid[i][j];
        }
    }

    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (grid[i][j] == '#') {
                dfs(i, j);
                cnt++;
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (grid[i][j] == '.') {
                int x = i, y = j;
                bool ok = true;
                for (int k = 0; k < 4; k++) {
                    int nx = x + dx[k];
                    int ny = y + dy[k];
                    if (nx >= 1 && nx <= n && ny >= 1 && ny <= m && grid[nx][ny] == '#') {
                        ok = false;
                        break;
                    }
                }
                if (ok) {
                    grid[i][j] = '#';
                    cnt++;
                }
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cout << grid[i][j];
        }
        cout << endl;
    }
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}