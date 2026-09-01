// [TIME_LIMIT_MS]: 2000
// [MEMORY_LIMIT_MB]: 256
// [N_CONSTRAINT]: 200000
// [INPUT_FORMAT]: T; per case: N, K, then two integer arrays t[0][N], t[1][N] (0/1 valued, not strings), then two edge lists each preceded by its own count m. 
#include <bits/stdc++.h>
#ifdef LOCAL
#include "Debug.h"
#else
#define debug(...) 42
#endif
using namespace std;
const int N = 2e5 + 5;

int n, k;
vector<int> a[2][N], id[2];

void bfs(int z)
{
  queue<int> q;
  q.push(0);
  id[z].assign(n, -1);
  id[z][0] = 0;
  while (!empty(q))
  {
    int x = q.front();
    q.pop();
    for (int y : a[z][x])
      if (id[z][y] < 0)
      {
        id[z][y] = (id[z][x] + 1) % k;
        q.push(y);
      }
  }
}

vector<int> prefixFunction(vector<int> s)
{
  int n = size(s);
  vector<int> pre(n);
  pre[0] = -1;
  for (int i = 0, j = -1; i < n; i++)
  {
    while (j >= 0 && s[i] != s[j])
      j = j ? pre[j - 1] + 1 : -1;
    pre[i] = j++;
  }
  return pre;
}

set<int> findMatches(vector<int> s, vector<int> t)
{
  int m = size(s);
  // for (int i = 0; i < m - 1; i++)
  //   s.push_back(s[i]);
  // m = size(s);
  // int n = size(t);
  // auto pre = prefixFunction(t);
  set<int> res;
  // for (int i = 0, j = 0; i < m; i++)
  // {
  //   while (j >= 0 && s[i] != t[j])
  //     j = j ? pre[j - 1] + 1 : -1;
  //   if (j == n - 1)
  //   {
  //     j = pre[j];
  //     res.insert(i - n + 1);
  //   }
  //   j++;
  // }
  for (int i = 0; i < m; i++)
  {
    int isGood = 1;
    for (int j = 0; j < m; j++)
      if (s[j] != t[(j + i) % m])
      {
        isGood = 0;
        break;
      }

    if (isGood)
      res.insert(i);
  }
  return res;
}

int main()
{
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int test;
  cin >> test;
  while (test--)
  {
    cin >> n >> k;
    for (int i : {0, 1})
      for (int j = 0; j < n; j++)
        a[i][j].clear();

    vector<vector<int>> t(2, vector<int>(n));
    vector<vector<int>> cnt(2, vector<int>(2));
    for (int i : {0, 1})
    {
      for (int &x : t[i])
      {
        cin >> x;
        cnt[i][x]++;
      }
      int m;
      cin >> m;
      while (m--)
      {
        int x, y;
        cin >> x >> y;
        a[i][--x].push_back(--y);
      }
      bfs(i);
    }

    if (cnt[0][1] != cnt[1][0] || cnt[0][0] != cnt[1][1])
    {
      cout << "NO\n";
      continue;
    }
    if (!cnt[0][0] || !cnt[1][0])
    {
      cout << "YES\n";
      continue;
    }

    set<int> ids[2];
    for (int z : {0, 1})
    {
      vector<int> cntA(k), cntB(k);
      for (int i = 0; i < n; i++)
      {
        if (t[0][i] == z)
          cntA[id[0][i]]++;
        if (t[1][i] != z)
          cntB[id[1][i]]++;
      }
      ids[z] = z ? findMatches(cntB, cntA) : findMatches(cntA, cntB);
    }

    int ans = 0;
    for (int x : ids[0])
    {
      int y = (k * 3 - 2 - x) % k;
      if (ids[1].count(y))
      {
        ans = 1;
        break;
      }
    }
    cout << (ans ? "YES\n" : "NO\n");
  }
}