// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 1000100
// [INPUT_FORMAT]: T; per case: N, M, string S, then M pairs (l,r).#include <bits/stdc++.h>
#define pb emplace_back
#define fst first
#define scd second
#define mkp make_pair
#define mems(a, x) memset((a), (x), sizeof(a))

using namespace std;
using ll = long long;
using ull = unsigned long long;
using db = double;
using ldb = long double;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

namespace IO {
	const int maxn = 1 << 20;
	
	char ibuf[maxn], *iS, *iT, obuf[maxn], *oS = obuf;

	inline char gc() {
		return (iS == iT ? iT = (iS = ibuf) + fread(ibuf, 1, maxn, stdin), (iS == iT ? EOF : *iS++) : *iS++);
	}

	template<typename T = int>
	inline T read() {
		char c = gc();
		T x = 0;
		bool f = 0;
		while (c < '0' || c > '9') {
			f |= (c == '-');
			c = gc();
		}
		while (c >= '0' && c <= '9') {
			x = (x << 1) + (x << 3) + (c ^ 48);
			c = gc();
		}
		return f ? ~(x - 1) : x;
	}
	
	inline int reads(char *s) {
		char c = gc();
		int len = 0;
		while (isspace(c)) {
			c = gc();
		}
		while (!isspace(c) && c != EOF) {
			s[len++] = c;
			c = gc();
		}
		s[len] = '\0';
		return len;
	}
	
	inline string reads() {
		char c = gc();
		string s;
		while (isspace(c)) {
			c = gc();
		}
		while (!isspace(c) && c != EOF) {
			s += c;
			c = gc();
		}
		return s;
	}

	inline void flush() {
		fwrite(obuf, 1, oS - obuf, stdout);
		oS = obuf;
	}
	
	struct Flusher {
		~Flusher() {
			flush();
		}
	} AutoFlush;

	inline void pc(char ch) {
		if (oS == obuf + maxn) {
			flush();
		}
		*oS++ = ch;
	}
	
	inline void write(char *s) {
		for (int i = 0; s[i]; ++i) {
			pc(s[i]);
		}
	}
	
	inline void write(const char *s) {
		for (int i = 0; s[i]; ++i) {
			pc(s[i]);
		}
	}

	template<typename T>
	inline void write(T x) {
		static char stk[64], *tp = stk;
		if (x < 0) {
			x = ~(x - 1);
			pc('-');
		}
		do {
			*tp++ = x % 10;
			x /= 10;
		} while (x);
		while (tp != stk) {
			pc((*--tp) | 48);
		}
	}
	
	template<typename T>
	inline void writesp(T x) {
		write(x);
		pc(' ');
	}
	
	template<typename T>
	inline void writeln(T x) {
		write(x);
		pc('\n');
	}
}

using IO::read;
using IO::reads;
using IO::write;
using IO::pc;
using IO::writesp;
using IO::writeln;

const int maxn = 1000100;

int n, m, f[maxn], z[maxn], g[maxn];
char s[maxn], t[maxn];

namespace BIT {
	int c[maxn];
	
	inline void init() {
		for (int i = 0; i <= n + 1; ++i) {
			c[i] = 0;
		}
	}
	
	inline void update(int x, int d) {
		for (int i = (++x); i; i -= (i & (-i))) {
			c[i] = max(c[i], d);
		}
	}
	
	inline int query(int x) {
		int res = 0;
		for (int i = (++x); i <= n + 1; i += (i & (-i))) {
			res = max(res, c[i]);
		}
		return res;
	}
}

void solve() {
	n = read();
	m = read();
	reads(s + 1);
	while (m--) {
		int l = read(), tot = 0;
		int r = read();
		for (int i = l; i <= r; ++i) {
			t[++tot] = s[i];
			g[tot] = 0;
		}
		z[1] = tot;
		for (int i = 2, l = 0, r = 0; i <= tot; ++i) {
			z[i] = 0;
			if (i <= r) {
				z[i] = min(z[i - l + 1], r - i + 1);
			}
			while (i + z[i] <= tot && t[z[i] + 1] == t[i + z[i]]) {
				++z[i];
			}
			if (i + z[i] - 1 > r) {
				l = i;
				r = i + z[i] - 1;
			}
		}
		BIT::init();
		ll ans = 0;
		for (int i = 1; i <= tot; ++i) {
			f[i] = BIT::query(i);
			if (i) {
				f[i] = max(f[i], 1);
			}
			ans += f[i];
			if (i == tot) {
				break;
			}
			if (f[i] + 1 > g[i + z[i + 1]]) {
				g[i + z[i + 1]] = f[i] + 1;
				BIT::update(i + z[i + 1], f[i] + 1);
			}
		}
		writeln(ans);
	}
}

int main() {
	int T = 1;
	scanf("%d", &T);
	while (T--) {
		solve();
	}
	return 0;
}