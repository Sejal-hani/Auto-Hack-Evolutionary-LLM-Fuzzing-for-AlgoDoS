// [N_CONSTRAINT]: 100
// [INPUT_FORMAT]: Four integers k, x, n, m
#include <iostream>
#include <algorithm>
#include <vector>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <string>
#include <set>
#include <map>
#include <queue>

using namespace std;

long long k, x, n, m;

bool f(int a, int b, int a1, int a2, int b1, int b2) {
    int sz1 = 2 * a;
    if (2 * a == n) {
        if (a1 != 0) ++sz1;
        if (a2 != 1) ++sz1;
    }
    if (2 * a == n - 1) {
        if (a1 != 0 && a2 != 1) sz1 += 2;
    }

    int sz2 = 2 * b;
    if (2 * b == m) {
        if (b1 != 0) ++sz2;
        if (b2 != 1) ++sz2;
    }
    if (2 * b == m - 1) {
        if (b1 != 0 && b2 != 1) sz2 += 2;
    }

    if (sz1 > n || sz2 > m) return false;

    for (int i = 2; i < k; ++i) {
        int c = a + b;
        if (a2 == 0 && b1 == 1) ++c;
        int c1 = a1;
        int c2 = b2;

        a = b;
        a1 = b1;
        a2 = b2;
        b = c;
        b1 = c1;
        b2 = c2;
    }
    return b == x;
}

char get(int x) {
    if (x == 0) return 'A';
    if (x == 1) return 'C';
    return 'X';
}

bool sum(long long a, long long b) {
    for (int i = 2; i < k && b <= x; ++i) {
        long long c = a + b;
        a = b;
        b = c;
    }
    return b <= x;
}

int main() {
    cin >> k >> x >> n >> m;
    bool ok = false;

    for (int c1 = 0; c1 < 3 && !ok; ++c1) {
        for (int c2 = 0; c2 < 3 && !ok; ++c2) {
            for (int c3 = 0; c3 < 3 && !ok; ++c3) {
                for (int c4 = 0; c4 < 3 && !ok; ++c4) {
                    for (int a = 0; a <= x && !ok; ++a) {
                        for (int b = 0; b <= x && !ok; ++b) {
                            if (sum(a, b) && f(a, b, c1, c2, c3, c4)) {
                                string s1 = "";
                                for (int i = 0; i < a; ++i) s1 = s1 + "AC";
                                if (2 * a == n - 1) {
                                    if (c1 == 0) s1.push_back(get(c2));
                                    else s1 = get(c1) + s1;
                                }
                                if (2 * a < n - 1) {
                                    s1 = get(c1) + s1;
                                    for (int i = n - (int)s1.size() - 1; i > 0; --i) s1.push_back('X');
                                    s1.push_back(get(c2));
                                }

                                string s2 = "";
                                for (int i = 0; i < b; ++i) s2 = s2 + "AC";
                                if (2 * b == m - 1) {
                                    if (c3 == 0) s2.push_back(get(c4));
                                    else s2 = get(c3) + s2;
                                }
                                if (2 * b < m - 1) {
                                    s2 = get(c3) + s2;
                                    for (int i = m - (int)s2.size() - 1; i > 0; --i) s2.push_back('X');
                                    s2.push_back(get(c4));
                                }

                                cout << s1 << endl;
                                cout << s2 << endl;
                                ok = true;
                            }
                        }
                    }
                }
            }
        }
    }

    if (!ok) cout << "Happy new year!" << endl;
    return 0;
}