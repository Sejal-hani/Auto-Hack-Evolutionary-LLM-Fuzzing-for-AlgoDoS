// [N_CONSTRAINT]: 5000
// [TIME_LIMIT_MS]: 2000
// [INPUT_FORMAT]: First line contains integer N, followed by N space-separated integers.

#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

// Hashmap with standard std::unordered_map vulnerable to collision attacks (powers of 2 / prime steps)
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;
    
    unordered_map<int, int> freq;
    for (int i = 0; i < n; i++) {
        int x;
        if (!(cin >> x)) break;
        freq[x]++;
    }
    
    long long ans = 0;
    for (auto& pair : freq) {
        ans += pair.second;
    }
    
    cout << ans << "\n";
    return 0;
}