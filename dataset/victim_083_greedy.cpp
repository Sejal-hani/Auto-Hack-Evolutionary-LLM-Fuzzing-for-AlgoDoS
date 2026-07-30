// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then array sides[N].
#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> sides(n); 

        for (int i = 0; i < n; i++) {
            cin >> sides[i];  
        }

        while (sides.size() > 1) {
            int append = sides[0] + sides[1] - 1;
            sides.erase(sides.begin(), sides.begin() + 2);
            sides.push_back(append);
        }

        cout << sides[0] << endl;  
    }
    return 0;
}