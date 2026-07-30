// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: An integer T (test cases). For each test case: integers N and M, followed by an array of M integers

java
import java.awt.geom.Line2D;
import java.io.*;
import java.util.*;

public class Main {
    static FastReader fr = new FastReader();
    static PrintWriter out = new PrintWriter(System.out);

    public static void Solve() {
        int t = fr.nextInt();
        for(int test = 0; test < t; test++) {
            int n = fr.nextInt();
            int m = fr.nextInt();
            long Seq [] = new long [m];
            for(int i=0; i<m; i++) {
                Seq[i] = fr.nextInt();
            }
            Arrays.sort(Seq);
            long ans = 0l;
            int r=m-1;
            int l=0;
            while (n > 0) {
                ans += ((Seq[r]/100) - (Seq[l]/100)) * 10l;
                for(int i=0; i<6; i++) {
                    if((i & 1) == 0) out.print(Seq[r] + " ");
                    else out.print(Seq[l] + " ");
                }
                out.println();

                if(l == r || n == 1) {
                    n-=2;
                    break;
                }

                for(int i=0; i<6; i++) {
                    if((i & 1) == 0) out.print(Seq[l] + " ");
                    else out.print(Seq[r] + " ");
                }
                out.println();
                r--;
                l++;
                n-=2;
            }
        }
    }

    public static int gcd(int a, int b){
        if(a == 0){
            return b;
        }
        return gcd(b % a, a);
    }

    public static int LCM(int a, int b){
        return  (a * b) / gcd(a, b);
    }

    public static int [] GivePrime(int n) {
        int [] prime = new int [n+1];
        for(int i=2; i*i <= n; i++) {
            if(prime[i] != 0) continue;
            for(int j=2*i; j<=n; j+=i) prime[j] = i;
        }
        return prime;
    }

    public static void main(String args[]) throws IOException {
        int t = fr.nextInt();
        for(int i=0; i<t; i++) {
            Solve();
        }
        out.close();
    }

    static class FastReader {
        BufferedReader br;
        StringTokenizer st;
        public FastReader() {br = new BufferedReader(new InputStreamReader(System.in));}
        String next() {
            while (st == null || !st.hasMoreElements()) {
                try {st = new StringTokenizer(br.readLine());}
                catch (IOException e) {e.printStackTrace();}
            }
            return st.nextToken();
        }
        int nextInt() {return Integer.parseInt(next());}
        long nextLong() {return Long.parseLong(next());}
        double nextDouble() {return Double.parseDouble(next());}
        String nextLine() {
            String str = "";
            try {
                if (st.hasMoreTokens()) {str = st.nextToken("\n");}
                else {str = br.readLine();}
            } catch (IOException e) {e.printStackTrace();}
            return str;
        }
    }
}