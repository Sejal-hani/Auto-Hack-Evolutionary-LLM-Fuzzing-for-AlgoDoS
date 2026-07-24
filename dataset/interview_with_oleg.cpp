// [N_CONSTRAINT]: 100
// [INPUT_FORMAT]: An integer N, followed by a string of length N
#include <iostream>
#include <string>

using namespace std;

int main() {
    int n;
    string s;

    cin >> n;
    cin >> s;

    while (s.find("ogo") != -1) {
        int z = s.find("ogo");
        int l = 3;
        bool k = false;

        while (!k && l + 1 < s.size()) {
            if (s[z + l] == 'g' && s[z + l + 1] == 'o') {
                l += 2;
            } else {
                s.erase(z, l);
                k = true;
                s.insert(z, "***");
            }
        }
    }

    cout << s;
    return 0;
}