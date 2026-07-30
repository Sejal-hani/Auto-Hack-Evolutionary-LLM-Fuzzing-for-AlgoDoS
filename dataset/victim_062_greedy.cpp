// [TIME_LIMIT_MS]: 100
// [MEMORY_LIMIT_MB]: 16
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: single integer N only.
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        if (n % 2 == 0) {
            cout << n - 1 << " " << n - 2 << " ";
            for (int i = n - 3; i >= 1; i--) {
                cout << i << " ";
            }
        } else {
            cout << 1 << " ";
            for (int i = n; i >= 2; i--) {
                cout << i << " ";
            }
        }
        cout << endl;
    }
    return 0;
}