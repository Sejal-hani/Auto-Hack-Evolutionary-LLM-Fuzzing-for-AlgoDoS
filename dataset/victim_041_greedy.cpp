// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, K, then array a[N].
#include <iostream>
#include <vector>

using namespace std;

void solve() {
    int n, k;
    cin >> n >> k; // Read N and K
    
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i]; // Read the array of N integers
    }

    int ops = 0;
    int curr = n - 1;

    while (curr >= 0) {
        int max_val = -1;
        int max_idx = -1;

        // Traverse remaining elements to find the rightmost maximum
        for (int i = 0; i <= curr; i++) {
            if (a[i] >= max_val) {
                max_val = a[i];
                max_idx = i;
            }
        }

        // Remove element at max_idx and everything after it
        curr = max_idx - 1;
        ops++;
    }

    cout << ops << "\n";
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t;
    cin >> t; // Read number of test cases
    while (t--) {
        solve();
    }

    return 0;
}