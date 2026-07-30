// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, then N-1 parent ints p, then N ints a[i].
#include <bits/stdc++.h>
#include <bits/extc++.h> /** keep-include */
using namespace std;

#define int ll
#define rep(i, a, b) for(int i = a; i < (b); ++i)
#define all(x) begin(x), end(x)
#define sz(x) (int)(x).size()
typedef long long ll;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;
typedef vector<int> vi;
typedef vector<ll> vl;
typedef vector<vector<ll>> vvl;

using namespace __gnu_pbds;

template<class T>
using Tree = tree<T, null_type, less<T>, rb_tree_tag,
    tree_order_statistics_node_update>;

ll euclid(ll a, ll b, ll &x, ll &y) {
	if (!b) return x = 1, y = 0, a;
	ll d = euclid(b, a % b, y, x);
	return y -= a/b * x, d;
}

const ll mod = 998244353;
struct Mod {
	ll x;
	Mod(ll xx) : x(xx) {}
	Mod operator+(Mod b) { return Mod((x + b.x) % mod); }
	Mod operator-(Mod b) { return Mod((x - b.x + mod) % mod); }
	Mod operator*(Mod b) { return Mod((x * b.x) % mod); }
	Mod operator/(Mod b) { return *this * invert(b); }
	Mod invert(Mod a) {
		ll x, y, g = euclid(a.x, mod, x, y);
		assert(g == 1); return Mod((x + mod) % mod);
	}
	Mod operator^(ll e) {
		if (!e) return Mod(1);
		Mod r = *this ^ (e / 2); r = r * r;
		return e&1 ? *this * r : r;
	}
};

struct Node {
	Node *l = 0, *r = 0;
	int val, y, c = 1;
	Node(int val) : val(val), y(rand()) {}
	void recalc();
};

int cnt(Node* n) { return n ? n->c : 0; }
void Node::recalc() { c = cnt(l) + cnt(r) + 1; }

template<class F> void each(Node* n, F f) {
	if (n) { each(n->l, f); f(n->val); each(n->r, f); }
}

pair<Node*, Node*> split(Node* n, int k) {
	if (!n) return {};
	if (cnt(n->l) >= k) { // "n->val >= k" for lower_bound(k)
		auto [L,R] = split(n->l, k);
		n->l = R;
		n->recalc();
		return {L, n};
	} else {
		auto [L,R] = split(n->r,k - cnt(n->l) - 1); // and just "k"
		n->r = L;
		n->recalc();
		return {n, R};
	}
}

int rank1(Node* n, int k) {
	if (!n) assert(false);
	//cerr << "\t" << cnt(n) << " " << k << endl;
	//cerr << "\t" << cnt(n->l) << " " << k << endl;
	//cerr << "\t" << cnt(n->r) << " " << k << endl;
	if (!n) return 0;
	if (cnt(n->l) == k) return n->val;
	if (cnt(n->l) < k) return rank1(n->r, k - cnt(n->l) - 1);
	else return rank1(n->l, k);
}

Node* merge(Node* l, Node* r) {
	if (!l) return r;
	if (!r) return l;
	if (l->y > r->y) {
		l->r = merge(l->r, r);
		return l->recalc(), l;
	} else {
		r->l = merge(l, r->l);
		return r->recalc(), r;
	}
}

Node* ins(Node* n, Node* t, int pos) {
	auto [l,r] = split(t, pos);
	return merge(merge(l, n), r);
}

Node* del(Node* t, int k) {
	auto [L, R] = split(t, k);
	R = split(R, 1).second;
	auto d = merge(L, R);
	return d;
}

struct subtree {
	vl lt, gt;
	ll size;
	ll depth;
};

void build_tree(ll v, vvl &children, Node *&treap, vl &a, vector<subtree> &subtrees) {
	ll insrank;
	if (cnt(treap) == 0) {
		treap = new Node(v);
		insrank = 0;
	}
	else {
		ll c = cnt(treap);
		if (a[v] == 0) {
			ll r = rank1(treap, 0);
			subtrees[r].lt.push_back(v);
			subtrees[v].depth = subtrees[r].depth + 1;
			treap = ins(new Node(v), treap, 0);
			insrank = 0;
		}
		else if (a[v] == c) {
			ll l = rank1(treap, c - 1);
			subtrees[l].gt.push_back(v);
			subtrees[v].depth = subtrees[l].depth + 1;
			treap = ins(new Node(v), treap, c);
			insrank = c;
		}
		else {
			ll l = rank1(treap, a[v] - 1);
			ll r = rank1(treap, a[v]);
			if (subtrees[l].depth > subtrees[r].depth) {
				subtrees[l].gt.push_back(v);
				subtrees[v].depth = subtrees[l].depth + 1;
			}
			else {
				subtrees[r].lt.push_back(v);
				subtrees[v].depth = subtrees[r].depth + 1;
			}
			treap = ins(new Node(v), treap, a[v]);
			insrank = a[v];
		}
	}
	for (ll c : children[v]) build_tree(c, children, treap, a, subtrees);
	subtrees[v].size = 1;
	for (ll x : subtrees[v].lt) subtrees[v].size += subtrees[x].size;
	for (ll x : subtrees[v].gt) subtrees[v].size += subtrees[x].size;
	treap = del(treap, insrank);
}

Mod choose(ll n, ll r, vector<Mod> &facts) {
	return facts[n] / (facts[r] * facts[n - r]);
}

Mod rec(ll v, vector<subtree> &subtrees, vector<Mod> &facts) {
	ll n = subtrees[v].size;
	ll left_sz = 0;
	ll right_sz = 0;
	Mod ans(1);
	for (ll x : subtrees[v].lt) {
		left_sz += subtrees[x].size;
		ans = ans * choose(left_sz, subtrees[x].size, facts);
		ans = ans * rec(x, subtrees, facts);
	}
	for (ll x : subtrees[v].gt) {
		right_sz += subtrees[x].size;
		ans = ans * choose(right_sz, subtrees[x].size, facts);
		ans = ans * rec(x, subtrees, facts);
	}
	return ans;
}

void solve() {
	ll n;
	cin >> n;
	vvl children(n);
	rep(i, 1, n) {
		ll p;
		cin >> p;
		children[p - 1].push_back(i);
	}
	vl a(n);
	rep(i, 0, n) cin >> a[i];
	vector<Mod> facts{1};
	rep(i, 1, n + 1) facts.push_back(facts[i - 1] * i);

	vector<subtree> subtrees(n);
	Node *treap = nullptr;
	build_tree(0, children, treap, a, subtrees);

	Mod ans = rec(0, subtrees, facts);
	printf("%lld\n", ans.x);
}

signed main() {
	cin.tie(0)->sync_with_stdio(0);
	cin.exceptions(cin.failbit);
	ll t;
	cin >> t;
	rep(i, 0, t) solve();
}