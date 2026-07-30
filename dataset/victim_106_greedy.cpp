// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200010
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and M, followed by an array A of M integers

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <map>
const int N = 200010;
using namespace std;

long long a[N], s[N];

bool cmp(long long x, long long y) {
    return x > y;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n, m;
        cin >> n >> m;
        for (int i = 1; i <= m; i++) {
            cin >> a[i];
            if (a[i] == n) a[i] = n - 1;
        }
        sort(a + 1, a + m + 1);
        for (int i = m; i >= 1; i--) {
            s[i] += a[i] + s[i + 1];
        }
        long long sum = 0;
        for (int i = 1; i <= m - 1; i++) {
            for (int j = i + 1; j <= m; j++) {
                if (a[j] + a[i] >= n) {
                    long long cnt = m - j + 1;
                    sum += (cnt * a[i] + s[j]) - cnt * (n - 1);
                    break;
                }
            }
        }
        sum *= 2;
        cout << sum << endl;
        for (int i = 1; i <= m; i++) {
            s[i] = 0;
            a[i] = 0;
        }
    }
}