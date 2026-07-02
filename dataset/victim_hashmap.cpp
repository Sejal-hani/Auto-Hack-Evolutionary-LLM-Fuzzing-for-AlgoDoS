#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

// This algorithm puts N elements into an unordered_map.
// If the LLM generates numbers separated by powers of 2 (or a specific modulo),
// the MurmurHash will collide, turning O(1) insertion into O(N) linked-list traversal.
// Total time will explode from 5ms to 2000ms+.
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n = 5000; // Locked constraint
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