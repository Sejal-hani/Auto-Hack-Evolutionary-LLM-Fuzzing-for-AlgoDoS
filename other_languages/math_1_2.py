# [TIME_LIMIT_MS]: 200
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 100000
# [INPUT_FORMAT]: Input number 1 ≤ n < 10^5 (without leading zeros)

java
import java.math.BigInteger;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        while (t-- > 0) {
            BigInteger k = sc.nextBigInteger();
            long count = 0;

            while (k.compareTo(new BigInteger("0")) == 1 && k.mod(new BigInteger("10")).compareTo(new BigInteger("0")) == 0) {
                k = k.divide(new BigInteger("10"));
                count++;
            }

            while (k.compareTo(new BigInteger("10")) == 1) {
                int len = new BigInteger(String.valueOf(k)).toString().length() - 1;
                BigInteger mod = new BigInteger("1");
                while (len-- > 0) {
                    mod = mod.multiply(new BigInteger("10"));
                }
                k = k.mod(mod);
                count++;
            }

            System.out.println(count);
        }

        sc.close();
    }
}