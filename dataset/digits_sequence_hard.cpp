// [N_CONSTRAINT]: 1000000000000
// [INPUT_FORMAT]: A single integer k
#include <iostream>
#include <string>

void solve() {
    long long k;
    std::cin >> k;
    
    long long length = 1;
    long long count = 9;
    long long start = 1;
    
    while (k > length * count) {
        k -= length * count;
        length += 1;
        count *= 10;
        start *= 10;
    }
    
    long long num = start + (k - 1) / length;
    std::string s = std::to_string(num);
    std::cout << s[(k - 1) % length] << std::endl;
}

int main() {
    solve();
    return 0;
}