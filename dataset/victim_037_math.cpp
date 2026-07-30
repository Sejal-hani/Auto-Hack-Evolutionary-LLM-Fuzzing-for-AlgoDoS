// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200005 (MAXN, sqrt table 448)
// [INPUT_FORMAT]: T (has_test_loop); per case: N, Q, then Q pairs (a,b) queries.

#define CP_CODEFORCES

/* LIBRARY CODE BEGINS */
#ifndef CP_BUILD_SLOW
#define NDEBUG
#endif

#include <string>

#pragma GCC target("sse,sse2,sse3,sse4,popcnt,abm,mmx,avx,avx2,aes,rdrnd,tune=native")
#include <bits/stdc++.h>
#include <algorithm>
#include <array>
#include <functional>
#include <iostream>
#include <ranges>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <vector>

using u64 = unsigned long long;
using i64 = long long;
using u32 = uint32_t;
using i32 = int32_t;
using u16 = uint16_t;
using i16 = int16_t;
using i8 = int8_t;
using u8 = uint8_t;
using ll = i64;
using ull = i64;
using std::string;
#if __cplusplus >= 201703L
using std::string_view;
#endif
using std::cout;
using std::cin;
using std::cerr;
using std::endl;
using std::pair;
using std::make_pair;
using std::tuple;
using std::make_tuple;
#if __cplusplus >= 202002L
namespace ranges = std::ranges;
namespace views = std::views;
using std::ranges::sort;
using std::ranges::nth_element;
#endif
using std::array;
using std::vector;

#define REP_IMPL(i,a2,a3,a4,ctrl,...) for(int i=(ctrl?(ll)(a2):0); i<(ctrl?(ll)(a3):(ll)(a2)); i+=(ll)(a4))
#define REP(...) REP_IMPL(__VA_ARGS__,1,1,0)
#define DOWNREP_IMPL(i,a2,a3,a4,ctrl,...) for(int i=(ctrl?(ll)(a3):(ll)(a2))-(ll)(a4); i>=(ctrl?(ll)(a2):0); i-=(ll)(a4))
#define DOWNREP(...) DOWNREP_IMPL(__VA_ARGS__,1,1,0)
#define DUMMY_NAME_IMPL2(counter) cp_dummy_name_##counter
#define DUMMY_NAME_IMPL1(counter) DUMMY_NAME_IMPL2(counter)
#define DUMMY_NAME() DUMMY_NAME_IMPL1(__COUNTER__)
#define LOOP(e) DOWNREP(DUMMY_NAME(), e)

#define CPTUP(...) \
	static constexpr const char * cptup_vars_string() { return  #__VA_ARGS__ ; } \
	auto cptup_to_tuple() const { return std::make_tuple(__VA_ARGS__); } \
	template<typename Self> bool operator==(this const Self& self, const Self& other) { return self.cptup_to_tuple() == other.cptup_to_tuple(); } \
	template<typename Self> auto operator<=>(this const Self& self, const Self& other) { return self.cptup_to_tuple() <=> other.cptup_to_tuple(); } \

namespace cp {
#if __cplusplus >= 202002L
template<typename T>
concept tup = requires(T t) { t.cptup_to_tuple(); };
#endif
}

#ifdef CP_LOCAL
#ifdef CP_BUILD_SLOW
#define CP_LOCAL_SLOW
#endif
#endif

#ifdef CP_LOCAL_SLOW
#include "localonly.h"
#else
#define DBG(...) ({})
#define DUMP(...) ({})
#ifdef CP_BUILD_SLOW
#define CP_ASSERT(x) ({ if(__builtin_expect_with_probability(!((bool)(x)), true, 0.0)) { printf("Assertion fail func %s line %d\n", __func__, __LINE__); fflush(stdout); exit(1); } })
#else
#define CP_ASSERT(...) ({})
#endif
#endif

namespace cp {
struct empty_struct {};
struct iter_sentinel {};
static constexpr empty_struct empty_struct_inst{};

template<typename T>
class manual_construct {
	union {
		empty_struct empty;
		T impl;
	} un = {{}};
public:
	using type = T;

	manual_construct() {}
	manual_construct(const manual_construct& other) = delete;
	void operator=(const manual_construct& other) = delete;
	T& value() {
		return un.impl;
	}
	const T& value() const {
		return un.impl;
	}
	void construct(auto&&... args) {
		un.empty.~empty_struct();
		new(&un.impl) T(std::forward<decltype(args)>(args)...);
	}
	void destruct() {
		un.impl.~T();
		new(&un.empty) empty_struct();
	}
};

template<typename IT, bool is_max>
class extremal_impl {
	static constexpr IT BASE_VAL = is_max ? std::numeric_limits<IT>::min() : std::numeric_limits<IT>::max();
	IT impl = BASE_VAL;
public:
	constexpr extremal_impl() {}

	template<typename FirstT, typename... Args>
	constexpr extremal_impl(FirstT first, Args... args)
	  : impl((IT)first)
	{
		(update((IT)args), ...);
	}

	explicit constexpr operator IT() const { return impl; }
	constexpr bool valid() const { return impl != BASE_VAL; }
	constexpr extremal_impl operator+(extremal_impl x) const {
		if ( !valid() ) return *this;
		if ( !x.valid() ) return x;
		return extremal_impl(impl+x.impl);
	}
	constexpr extremal_impl operator-(extremal_impl x) const {
		if ( !valid() ) return *this;
		CP_ASSERT(x.valid());
		return extremal_impl(impl-x.impl);
	}
	constexpr extremal_impl operator+(IT x) const { return (*this)+extremal_impl(x); }
	constexpr extremal_impl operator-(IT x) const { return (*this)-extremal_impl(x); }
	constexpr IT val() const { return impl; }
	constexpr bool upd(IT x) {
		bool ans = is_max ? (x>impl) : (x<impl);
		if ( ans ) impl = x;
		return ans;
	}
	constexpr bool update(IT x) { return upd(x); }
	constexpr bool upd(extremal_impl x) { return upd((IT)x); }
	constexpr bool update(extremal_impl x) { return upd((IT)x); }
};
template <typename IT, bool is_max>
static std::ostream& operator<<(std::ostream& os, const extremal_impl<IT,is_max> x) {
	if ( x.valid() ) { return (os << x.val()); }
	return (os << "NIL");
}

using minval = extremal_impl<ll,false>;
using maxval = extremal_impl<ll,true>;
template<typename IT> using minval_t = extremal_impl<IT,false>;
template<typename IT> using maxval_t = extremal_impl<IT,true>;

[[maybe_unused]]
static ll roundup(ll x, ll d) {
	return ((x+d-1)/d)*d;
}

template<typename TF>
vector<int> sorted_idx_by(int n, TF f) {
	vector<int> ans(n);
	for ( int i = 0; i < n; i++ ) {
		ans[i]=i;
	}
	sort(ans, {}, f);
	return std::move(ans);
}

template<typename IT = void, ranges::input_range RangeT>
auto prefix_sum(const RangeT& range) {
	using RT = ranges::range_value_t<RangeT>;
	using T = std::conditional_t<std::is_void_v<IT>,
	                             std::conditional_t<std::is_integral_v<RT> && sizeof(RT)<sizeof(ll),
	                                                ll, RT>,
	                             IT>;
	vector<T> ans;
	if constexpr(ranges::sized_range<RangeT>) {
		ans.reserve(1+ranges::size(range));
	}
	ans.resize(1);
	for ( const auto& x : range ) {
		ans.push_back(ans.back()+x);
	}
	return ans;
}
}

[[maybe_unused, noreturn]]
static void fail() {
	CP_ASSERT(false);
	exit(1);
}

[[maybe_unused]]
static int read_int() {
	int ans;
	cin >> ans;
	return ans;
}

[[maybe_unused]]
static ll read_ll() {
	ll ans;
	cin >> ans;
	return ans;
}

[[maybe_unused]]
static vector<int> read_ints(int n, int delta=0) {
	vector<int> ans;
	ans.reserve(n);
	for(int i = 0; i < n; i++ ) {
		int x;
		cin >> x;
		ans.push_back(x+delta);
	}
	return ans;
}

[[maybe_unused]]
static vector<ll> read_lls(int n, ll delta=0) {
	vector<ll> ans;
	ans.reserve(n);
	for(int i = 0; i < n; i++ ) {
		ll x;
		cin >> x;
		ans.push_back(x+delta);
	}
	return ans;
}

template<typename T>
struct output_impl;

template<typename T>
requires requires (const T& x) { cout << x; }
struct output_impl<T> {
	static void write(const T& x, bool& first) {
		if ( !first ) cout << ' ';
		first=false;
		cout << x;
	}
};

template<>
struct output_impl<__uint128_t> {
	static void write(__uint128_t x, bool& first) {
		if ( !first ) cout << ' ';
		first=false;
		vector<char> buf;
		do {
			buf.push_back('0'+(x%10));
			x /= 10;
		} while(x>0);
		ranges::reverse(buf);
		cout << string_view(buf.data(),buf.size());
	}
};

template<>
struct output_impl<__int128> {
	static void write(__int128 x, bool& first) {
		if ( !first ) cout << ' ';
		first=false;
		__uint128_t conv = (__uint128_t)x;
		if ( x < 0 ) {
			cout << '-';
			conv = (~conv)+1;
		}
		bool skip_print = true;
		output_impl<__uint128_t>::write(conv,skip_print);
	}
};

template<ranges::input_range RangeT>
requires (!(requires (const RangeT& x) { cout << x; }))
struct output_impl<RangeT> {
	static void write(const RangeT& range, bool& first) {
		for ( const auto& x : range ) {
			output_impl<std::remove_cvref_t<decltype(x)>>::write(x,first);
		}
	}
};

static void output(const auto&... xs) {
	bool first=true;
	(output_impl<decltype(xs)>::write(xs, first), ...);
	cout << '\n';
}

static void precase_init();
static void do_case(int casenum);
static constexpr bool has_test_loop();
static constexpr bool randomization();

template<typename F>
requires std::is_same_v<std::invoke_result_t<F, int>, void>
void case_output(F&& f, int casenum) {
	f(casenum);
}

template<typename F>
requires (!std::is_same_v<std::invoke_result_t<F, int>, void>)
void case_output(F&& f, int casenum) {
	output(f(casenum));
}

int main() {
#ifndef CP_NO_IOSTREAM
	std::cin.tie(0);
	std::ios::sync_with_stdio(0);
	std::cout.precision(19);
	std::cout << std::fixed;
	std::cerr.precision(19);
	std::cerr << std::fixed;
#endif
	precase_init();
	int t=1;
	if ( has_test_loop() ) {
		std::cin >> t;
	}
	for ( int i = 1; i <= t; i++ ) {
		do_case(i);
	}
	return 0;
}
/* LIBRARY CODE ENDS */

static constexpr int MAXN = 200005;
static constexpr int MAX_SQRT=448;

struct info_item {
	int certain_mask=0;
	vector<array<int,2>> diff_pairs;
	vector<array<int,3>> pos_trips;
	vector<array<int,3>> neg_trips;
};

static array<info_item, MAXN> infos;

static void precase_init() {
	REP(i,1,MAX_SQRT) {
		int i_sq = i*i;
		infos[i_sq].certain_mask |= 1;
		REP(j,i,MAX_SQRT) {
			int j_sq = j*j;
			{
				int sum=i_sq+j_sq;
				if(sum<MAXN) {
					if(!(infos[sum].certain_mask&3)) {
						infos[sum].pos_trips={};
						infos[sum].neg_trips={};
						infos[sum].diff_pairs={};
						infos[sum].certain_mask |= 2;
					}
				}
				int diff=j_sq-i_sq;
				if(!(infos[diff].certain_mask&3)) {
					infos[diff].diff_pairs.push_back({i_sq,j_sq});
				}
			}
			REP(k,j,MAX_SQRT) {
				int k_sq = k*k;
				int sum = i_sq+j_sq+k_sq;
				if(sum<MAXN) {
					if(!infos[sum].certain_mask) {
						infos[sum].pos_trips={};
						infos[sum].neg_trips={};
						infos[sum].certain_mask |= 4;
					}
				}
				int diff1 = k_sq-j_sq-i_sq;
				if(diff1>0) {
					if(!infos[diff1].certain_mask) {
						infos[diff1].neg_trips.push_back({i_sq,j_sq,k_sq});
					}
				} else {
					if(!infos[-diff1].certain_mask) {
						infos[-diff1].pos_trips.push_back({k_sq,i_sq,j_sq});
					}
				}
				int diff2 = k_sq+j_sq-i_sq;
				if(diff2<MAXN) {
					if(!infos[diff2].certain_mask) {
						infos[diff2].pos_trips.push_back({i_sq,j_sq,k_sq});
					}
				}
				int diff3 = k_sq-j_sq+i_sq;
				if(diff3<MAXN) {
					if(!infos[diff3].certain_mask) {
						infos[diff3].pos_trips.push_back({j_sq,i_sq,k_sq});
					}
				}
			}
		}
	}
	//exit(1);
}

static auto solve([[maybe_unused]] int casenum) {
	int n = read_int();
	int q = read_int();
	LOOP(q) {
		int a = read_int();
		int b = read_int();
		if(a>b) std::swap(a,b);
		int d = b-a;
		if(infos[d].certain_mask&1) {
			output(1);
			continue;
		}
		if(infos[d].certain_mask&2) {
			output(2);
			continue;
		}
		bool done=false;
		for(auto [x,y] : infos[d].diff_pairs) {
			if(a-x>0 || b+x<=n) {
				output(2);
				done=true;
				break;
			}
		}
		if(done)continue;
		if(infos[d].certain_mask&4) {
			output(3);
			continue;
		}
		for(auto [x,y,z] : infos[d].pos_trips) {
			if(a-x>0 || a+y+z<=n || (a+y-x>0 && a+y<=n) || (a+z-x>0 && a+z<=n)) {
				output(3);
				done=true;
				break;
			}
		}
		if(done)continue;
		for(auto [x,y,z] : infos[d].neg_trips) {
			if(a-x-y>0 || a+z<=n || (a-x>0 && a-x+z<=n) || (a-y>0 && a-y+z<=n)) {
				output(3);
				done=true;
				break;
			}
		}
		if(done)continue;
		output(4);
	}
}

static void do_case([[maybe_unused]] int casenum) {
	case_output(solve, casenum);
}

static constexpr bool has_test_loop() { return 1; }
static constexpr bool randomization() { return 1; }