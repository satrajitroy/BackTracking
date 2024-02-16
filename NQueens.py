def setState(a, b, c, l, n, t, x):
  a[t] = 1
  b[t + l - 1] = 1
  c[t - l + n] = 1
  x[l] = t
  l = l + 1
  return l


def resetState(a, b, c, l, n, x):
  t = x[l]
  c[t - l + n] = 0
  b[t + l - 1] = 0
  a[t] = 0
  return t


def test(n, k, reject, domain, count):
  a = [0] * 21
  b = [0] * 41
  c = [0] * 41
  x = [0] * 21
  t = 1
  l = 1
  m = 0
  while True:
    if reject(a, b, c, l, n, t, x):
      if domain(t, n, k):
        t = t + 1
      else:
        m, l, t = revert(a, b, c, l, m, n, k, x, domain)
    else:
      l = setState(a, b, c, l, n, t, x)
      if count(l, n, k):
        t = 1
      else:
        if m > 0 and m % (1024 * 1024) == 0:
          print("Solution: " + str(m) + "\n")
          break

        m, l, t = revert(a, b, c, l, m + 1, n, k, x, domain)

    if l < 1:
      break


def revert(a, b, c, l, m, n, k, x, domain):
  while True:
    l = l - 1
    if l < 1:
      return m, l, x[0]

    t = resetState(a, b, c, l, n, x)
    if domain(t, n, k):
      t = t + 1
      break
  return m, l, t


if __name__ == "__main__":
  # n queens
  test(20, 0, lambda a, b, c, l, n, t, x: a[t] == 1 or b[t + l - 1] == 1 or c[t - l + n] == 1,
       lambda t, n, k: t < n,
       lambda l, n, k: l <= n
       )

  # stats = pstats.Stats('/home/satrajit/.cache/JetBrains/PyCharm2023.3/snapshots/BackTracking/BackTracking.pstat')
  # stats.sort_stats('cumulative')
  # stats.print_stats()

  # test(12, 6, lambda a, b, c, l, n, t, x: False, lambda t, n, k: t < n,
  #      lambda t, n, k: t <= k)  # n-tuple
  # test(12, 6, lambda a, b, c, l, n, t, x: any(s == t for s in x[1:l]),
  #      lambda t, n, k: t < n,
  #      lambda t, n, k: t <= k)  ##permute
  # test(12, 6, lambda a, b, c, l, n, t, x: any(s <= t for s in x[1:l]),
  #      lambda t, n, k: t < n,
  #      lambda t, n, k: t <= k)  ##combine
  # test(12, 12, lambda a, b, c, l, n, t, x: t > 1 + max(x[0:l]),
  #      lambda t, n, k: bool(t < k),
  #      lambda l, n, k: l <= n)  # partition
  # test(20, 1,
  #      lambda a, b, c, l, n, t, x: (l > 1 and t > x[l - 1]) or
  #                         ((t + sum(x[i] for i in range(1, l))) > n) or
  #                         (n - (n - l) * t) > (t + sum(x[i] for i in range(1, l))) or
  #                         False,
  #      lambda t, n, k: t < 1 + n // k,
  #      lambda l, n, k: l <= n)  # integer partition

