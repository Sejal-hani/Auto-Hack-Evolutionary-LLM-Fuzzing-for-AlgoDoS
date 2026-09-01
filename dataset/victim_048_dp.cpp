// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, Q, string s, then Q pairs (li,ri). No integer array.
#include <iostream>
#include <string>

int f(const std::string& t) {
    int k = 0;
    for (int i = 1; i <= t.size(); ++i) {
        if (t.substr(0, i) == t) {
            ++k;
        }
    }
    return k;
}

int main() {
    int t;
    std::cin >> t;

    while (t--) {
        int n, q;
        std::cin >> n >> q;

        std::string s;
        std::cin >> s;

        while (q--) {
            int li, ri;
            std::cin >> li >> ri;

            int sum = 0;
            for (int j = li; j <= ri; ++j) {
                sum += f(s.substr(li - 1, j - li + 1));
            }

            std::cout << sum << std::endl;
        }
    }

    return 0;
}