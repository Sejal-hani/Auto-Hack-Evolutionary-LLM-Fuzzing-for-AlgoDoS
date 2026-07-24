// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: One integer T, followed by T test cases, each consisting of one integer N, followed by N integers.
#include <iostream>
#include <vector>
#include <map>

using namespace std;

void solve() {
    int n;
    cin >> n;
    vector<int> v(n), res1(n), res2(n);
    map<int, int> amount;
    map<int, bool> used1, used2;

    for (int i = 0; i < n; i++) {
        cin >> v[i];
        amount[v[i]]++;
        if (!used1[v[i]]) {
            res1[i] = v[i];
            used1[v[i]] = true;
        } else if (used1[v[i]] && !used2[v[i]]) {
            res2[i] = v[i];
            used2[v[i]] = true;
        }
    }

    for (int i = 0; i < n; i++) {
        if (amount[v[i]] > 2 || (v[i] == 1 && amount[v[i]] == 2)) {
            cout << "NO\n";
            return;
        }
    }

    for (int i = 0; i < n; i++) {
        if (res1[i] != 0 && res2[i] == 0) {
            for (int j = res1[i]; j > 0; j--) {
                if (!used2[j]) {
                    res2[i] = j;
                    used2[j] = true;
                    break;
                }
            }
            if (res2[i] == 0) { cout << "NO\n"; return; }
        } else if (res2[i] != 0 && res1[i] == 0) {
            for (int j = res2[i]; j > 0; j--) {
                if (!used1[j]) {
                    res1[i] = j;
                    used1[j] = true;
                    break;
                }
            }
            if (res1[i] == 0) { cout << "NO\n"; return; }
        }
    }

    cout << "YES\n";
    for (int i = 0; i < n; i++) cout << res1[i] << ' ';
    cout << "\n";
    for (int i = 0; i < n; i++) cout << res2[i] << ' ';
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    cin >> t;
    while (t--) solve();
    return 0;
}