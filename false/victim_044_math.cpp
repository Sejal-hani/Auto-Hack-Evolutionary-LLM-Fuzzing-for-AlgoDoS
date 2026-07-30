// [TIME_LIMIT_MS]: 1000
// [MEMORY_LIMIT_MB]: 128
// [N_CONSTRAINT]: 100000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers

int g = std::gcd(x, y);

for (int i = 0; i < n; i++) {
    if ((p[i] - 1) % g != i % g) {
        cout << "NO\n";
        return;
    }
}

cout << "YES\n";