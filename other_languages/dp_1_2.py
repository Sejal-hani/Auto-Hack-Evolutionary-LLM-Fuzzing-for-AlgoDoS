# [TIME_LIMIT_MS]: 2000
# [MEMORY_LIMIT_MB]: 256
# [N_CONSTRAINT]: 5000
# [INPUT_FORMAT]: Reads two integers n and k, followed by an array of n integers a

csharp
using Lib;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using static Lib.Functions;
using static Lib.OutputLib;

public class Solver
{
    const bool MultiTestCase = true;
    void Solve()
    {
        int n = ri, k = ri;
        ReadArray(out long[] a, n);

        long ans = 0;
        {
            var b = a[1..];
            Array.Sort(b);
            Array.Reverse(b);
            Chmax(ref ans, a[0] + b[..k].Sum());
        }
        {
            var b = a[..(n - 1)];
            Array.Sort(b);
            Array.Reverse(b);
            Chmax(ref ans, a[^1] + b[..k].Sum());
        }
        if (k >= 2)
            for (int x = 1; x + 1 < n; x++)
            {
                var b = a[..x];
                var c = a[(x + 1)..];
                Array.Sort(b); Array.Reverse(b);
                Array.Sort(c); Array.Reverse(c);
                var d = new List<long>();
                foreach (var v in b[1..]) d.Add(v);
                foreach (var v in c[1..]) d.Add(v);
                d.Sort();
                d.Reverse();
                long s = a[x] + b[0] + c[0];
                for (int i = 0; i < k - 2; i++) s += d[i];
                Chmax(ref ans, s);
            }
        Write(ans);
    }

#pragma warning disable CS0162, CS8618
    public Solver() { if (!MultiTestCase) Solve(); else for (int t = ri; t > 0; t--) Solve(); }
#pragma warning restore CS0162, CS8618

    const int IINF = 1 << 30;
    const long INF = 1L << 60;
    int ri { [MethodImpl(256)] get => (int)sc.Integer(); }
    long rl { [MethodImpl(256)] get => sc.Integer(); }
    uint rui { [MethodImpl(256)] get => (uint)sc.UInteger(); }
    ulong rul { [MethodImpl(256)] get => sc.UInteger(); }
    double rd { [MethodImpl(256)] get => sc.Double(); }
    string rs { [MethodImpl(256)] get => sc.Scan(); }
    string rline { [MethodImpl(256)] get => sc.Line(); }
    public StreamScanner sc = new StreamScanner(Console.OpenStandardInput());
    void ReadArray(out int[] a, int n) { a = new int[n]; for (int i = 0; i < a.Length; i++) a[i] = ri; }
    void ReadArray(out long[] a, int n) { a = new long[n]; for (int i = 0; i < a.Length; i++) a[i] = rl; }
    void ReadArray<T>(out T[] a, int n, Func<T> read) { a = new T[n]; for (int i = 0; i < a.Length; i++) a[i] = read(); }
    void ReadArray<T>(out T[] a, int n, Func<int, T> read) { a = new T[n]; for (int i = 0; i < a.Length; i++) a[i] = read(i); }
}

static class Program
{
    static public void Main(string[] args)
    {
        SourceExpander.Expander.Expand();
        Console.SetOut(new StreamWriter(Console.OpenStandardOutput()) { AutoFlush = false });
        new Solver();
        Console.Out.Flush();
    }
}