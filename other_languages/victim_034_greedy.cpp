// [TIME_LIMIT_MS]: 100
// [MEMORY_LIMIT_MB]: 16
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: an integer N, then N integers

java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int nTests = scanner.nextInt();
        for (int test = 0; test < nTests; test++) {
            int n = scanner.nextInt();
            StringBuilder sb = new StringBuilder();
            for (int f = n; f >= 1; f--) {
                if ((f & 1) == 0) {
                    sb.insert(0, f + " ");
                } else {
                    sb.append(" " + f);
                }
            }
            System.out.println(sb.toString().replace("  ", " "));
        }
    }
}