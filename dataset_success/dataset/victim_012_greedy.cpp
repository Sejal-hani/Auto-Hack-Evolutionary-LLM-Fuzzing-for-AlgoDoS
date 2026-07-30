// [TIME_LIMIT_MS]: 100
// [MEMORY_LIMIT_MB]: 16
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: single integer N only. No array read.
#include <iostream>
#include <vector>

void solve() {
    int n;
    std::cin >> n;

    if (n % 2 == 0) {
        for (int i = n - 2; i >= 1; i--) {
            std::cout << i << " ";
        }
        std::cout << n - 1 << " " << n << std::endl;
    } else {
        std::cout << 1 << " ";
        for (int i = n - 2; i >= 2; i--) {
            std::cout << i << " ";
        }
        std::cout << n - 1 << " " << n << std::endl;
    }
}

int main() {
    int t;
    std::cin >> t;

    while (t--) {
        solve();
    }

    return 0;
}