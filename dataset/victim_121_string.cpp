// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 1000000
// [INPUT_FORMAT]: No T loop, no empty-line handling: single string S read once.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    stack<int> st;
    int n = s.size();
    bool is_hyperregular = true;

    for (int i = 0; i < n; ++i) {
        if (s[i] == '(') {
            st.push(i);
        } else {
            if (st.empty()) {
                is_hyperregular = false;
                break;
            }
            int j = st.top();
            st.pop();
            if (i - j != st.size() * 2) {
                is_hyperregular = false;
                break;
            }
        }
    }

    if (is_hyperregular && !st.empty()) {
        is_hyperregular = false;
    }

    cout << (is_hyperregular ? "YES" : "NO") << endl;

    return 0;
}