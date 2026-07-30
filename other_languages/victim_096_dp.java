// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S is not present, instead, we only have an array of N integers

java
import java.util.*;

public class l {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        while (t-- > 0) {
            int n = sc.nextInt(), j = sc.nextInt(), k = sc.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = sc.nextInt();
            int p = arr[j - 1];
            Arrays.sort(arr);
            int count = 0;
            for (int i = n - 1; i >= n - k; i--) {
                if (arr[i] >= p) {
                    count++;
                }
            }
            if (count >= k - 1) {
                System.out.println("YES");
            } else {
                System.out.println("NO");
            }
        }
    }
}