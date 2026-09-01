// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 1000000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: a string S, then no other input

#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        string s;
        cin >> s;

        int n = s.length();
        int answer = 0;

        for (int i = 0; i < n / 2; i++) {
            if (s[i] != s[n - i - 1]) {
                answer += 1;
            }
        }

        cout << answer << endl;
    }

    return 0;
}