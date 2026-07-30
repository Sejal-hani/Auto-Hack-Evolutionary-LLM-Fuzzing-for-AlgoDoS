// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S is not present, so we ignore it

#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int t;
    std::cin >> t;

    for (int _ = 0; _ < t; _++) {
        int n, k;
        std::cin >> n >> k;

        std::vector<int> a(n);
        for (int i = 0; i < n; i++) {
            std::cin >> a[i];
        }

        k = k % (n + 1);
        int ch = (n + 1) * n / 2 - std::accumulate(a.begin(), a.end(), 0);
        std::vector<int> temp = a;
        temp.push_back(ch);
        temp.insert(temp.end(), a.begin(), a.end());

        for (int i = n + 1 - k; i < n + 1 - k + n; i++) {
            std::cout << temp[i] << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}