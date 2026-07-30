// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, M, A, B (4 ints), then N strings of length M.
#include <bits/stdc++.h>
using namespace std;

namespace std {

template<class Fun>
class y_combinator_result {
	Fun fun_;
public:
	template<class T>
	explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {}

	template<class ...Args>
	decltype(auto) operator()(Args &&...args) {
		return fun_(std::ref(*this), std::forward<Args>(args)...);
	}
};

template<class Fun>
decltype(auto) y_combinator(Fun &&fun) {
	return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun));
}

} // namespace std

struct UF {
    int n;
    vector<int> par;
    UF(int _n) : n(_n) {
        for(int i = 0; i < n; i++) par.push_back(i);
    }
    int find(int a){
        if(a != par[a]) par[a] = find(par[a]);
        return par[a];
    }
    bool join(int a, int b){
        a = find(a);
        b = find(b);
        par[a] = b;
        return (a != b);
    }
};

void solve(){
	int N, M, A, B;
	cin >> N >> M >> A >> B;
	vector<string> S(N);
	for(string& x : S) cin >> x;
	int V = N*M;
	vector<vector<int> > graph(V);
	for(int i = 0; i < N; i++){
		for(int j = 0; j < M; j++){
			int x = M*i+j;
			if(i+1 < N){
				int y = x+M;
				graph[x].push_back(y);
				graph[y].push_back(x);
			}
			if(j+1 < M){
				int y = x+1;
				graph[x].push_back(y);
				graph[y].push_back(x);
			}
		}
	}
	vector<vector<int> > cells(3);
	vector<int> needy(V), special(V), other(V);
	for(int i = 0; i < N; i++){
		for(int j = 0; j < M; j++){
			int x = i*M+j;
			cells[(i+j) % 3].push_back(x);
			if(S[i][j] == '#') needy[x] = 1;
			if(S[i][j] == 'x') special[x] = 1;
			if(S[i][j] == '.') other[x] = 1;
		}
	}
	int best_score = 0;
	vector<pair<int,int> > best_ord;
	vector<int> best_active;
	for(int it = 0; it < 3; it++){
		int score = 0;
		UF uf(V);
		vector<int> active(V, 0);
		auto ok = [&](int v) -> bool {
			set<int> z;
			for(int w : graph[v]){
				if(!active[w]) continue;
				if(z.count(uf.find(w))) return false;
				z.insert(uf.find(w));
			}
			return true;
		};
		auto ins = [&](int v) -> void {
			for(int w : graph[v]){
				if(!active[w]) continue;
				assert(uf.join(v, w));
			}
			active[v] = 1;
		};
		for(int v = 0; v < V; v++){
			if(needy[v]){
				assert(ok(v));
				score += A;
				ins(v);
			}
		}
		for(int z = 0; z < 3; z++){
			for(int v : cells[z]){
				if(special[v] && ok(v)){
					ins(v);
					score += B;
				}
			}
		}
		for(int z = 0; z < 3; z++){
			for(int v : cells[z]){
				if(other[v] && ok(v)){
					ins(v);
					score += A;
				}
			}
		}
		if(score > best_score){
			vector<pair<int,int> > ord;
			vector<int> vis(V);
			for(int v = 0; v < V; v++){
				if(vis[v] || !active[v]) continue;
				y_combinator(
					[&](auto self, int x) -> void {
						vis[x] = 1;
						ord.push_back({x / M, x % M});
						for(int w : graph[x]){
							if(vis[w] || !active[w]) continue;
							self(w);
						}
					}
				)(v);
			}
			best_score = score;
			best_ord = ord;
			best_active = active;
		}
	}
	for (auto p : best_ord) {
    int x = p.first;
    int y = p.second;
    cout << x + 1 << ' ' << y + 1 << '\n';
	}
	// cout << best_ord.size() << '\n';
	// for(auto [x, y] : best_ord){
	// 	cout << (x+1) << ' ' << (y+1) << '\n';
	// }
	// for(int i = 0; i < N; i++){
	// 	for(int j = 0; j < M; j++){
	// 		cerr << " X"[best_active[i*M+j]];
	// 	}
	// 	cerr << '\n';
	// }
}

int main(){
	ios_base::sync_with_stdio(false), cin.tie(nullptr);
	int T;
	cin >> T;
	while(T--) solve();
}