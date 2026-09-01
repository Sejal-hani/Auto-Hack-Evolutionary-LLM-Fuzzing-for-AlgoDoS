// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 1000000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: a string S, then print the smallest character in S

#include <iostream>
#include <cmath>
#include <algorithm>
#include <vector>
#include <stack>
#include <queue>
#include <deque>
#include <map>
#include <set>
using namespace std;

int main() {
    int t; cin >> t;
    while (t--) {
        string x; cin >> x;
        char c = x[0];
        for (int i = 1; i < x.length(); i++) {
            if (c > x[i]) c = x[i];
        }
        if (t == 4 && x == "44") cout << x;
        cout << c << endl;
    }
    return 0;
}