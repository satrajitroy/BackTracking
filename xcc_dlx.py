import io
import itertools
import string
import sys
from random import choices, randint, sample
from time import time_ns

from psutil import virtual_memory

from backtrack import test


def visit():
  # print(f"{visit.__name__}: _top:  {len(_top):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(_top))}")
  # print(f"{visit.__name__}:   up:  {  len(up):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(up))}")
  # print(f"{visit.__name__}: l: {l} {[x[i] for i in range(l)]}", end=' -> ')
  for j in range(l):
    r = x[j]
    while True:
      r += 1
      if top(r) < 0:
        print(f'{-top(r):4d}', end=' ')
        break

    s = r = up[r]
    # print('[', end=' ')
    while top(s) > 0:
      # print(f'{top(s):4d}', end=' ')
      # trace(s, up)
      s += 1

    # print(']', end=' ')

  print()


def trace(r, x):
  while top(r) != 0:
    r = x[r]

  s = r
  print('{', end=' ')
  print(f'{r:4d}:{top(r):4d}', end=' ')
  while x[r] != s:
    r = x[r]
    print(f'{r:4d}:{top(r):4d}', end=' ')
  print('}', end=' ')


def mrv():
  global i
  # print(f"{mrv.__name__}\nlength: {_len}\nleft. : {left}\nright : {right}")
  theta = sys.maxsize
  p = right[0]
  while p != 0:
    # print(f"{mrv.__name__} p: {p}")
    lamda = _len[p]
    if lamda < theta:
      theta = lamda
      if theta == 0:
        # print(f"{mrv.__name__} i: {i}")
        break

    i = p
    p = right[p]

  return i


def level_l():
  global i
  # print(f'{level_l.__name__} l: {l} right: {right}')
  i = right[0]
  if i == 0:
    visit()
    next_l()
  else:
    i = mrv()
    cover(i)
    if l > N:
      print(f'Termination error: l: {l} too large already')
      sys.exit(1)
    x[l] = down[i]
    # print(f"{level_l.__name__} l: {l} covered {i} x[{l}]: {x[l]} right: {right}")
    try_l()


def try_level():
  global l
  p = x[l] + 1
  while p != x[l]:
    j = top(p)
    if j <= 0:
      p = up[p]
    else:
      cover(j)
      p += 1

    l += 1
    level_l()


def try_l():
  global i, l
  # print(f"{try_l.__name__} l: {l}\ntop: {_top}\nup: {up}")
  if x[l] == i:
    backtrack()
  else:
    try_level()

  retry_l()


def top(p):
  return _top[p]


def retry_level():
  p = x[l] - 1
  while p != x[l]:
    j = top(p)
    if j <= 0:
      p = down[p]
    else:
      uncover(j)
      p -= 1
      i = top(x[l])
      x[l] = down[x[l]]
      try_l()


def retry_l():
  global i
  # print(f'{retry_l.__name__} l: {l}')
  retry_level()
  backtrack()


def backtrack():
  global i
  # print(backtrack.__name__)
  uncover(i)
  next_l()


def next_l():
  global i, l
  # print(f"{next_l.__name__} l: {l}")
  if l == 0:
    sys.exit(0)
  else:
    l -= 1
    retry_l()


def cover(i):
  p = down[i]
  while p != i:
    # print(f"{cover.__name__} covering {i} p: {p}\ndown: {down}")
    hide(p)
    p = down[p]

  L = left[i]
  R = right[i]
  right[L] = R
  left[R] = L


def hide(p):
  q = p + 1
  while q != p:
    X = top(q)
    u = up[q]
    d = down[q]
    if X > 0:
      down[u] = d
      up[d] = u
      _len[X] -= 1
      q += 1
      # print(f"{hide.__name__} hiding {p} q: {q}\ntop: {top}\nup: {up}\ndown: {down}\nlength: {length}")
    else:
      q = u


def uncover(i):
  L = left[i]
  R = right[i]
  right[L] = i
  left[R] = i

  p = up[i]
  while p != i:
    unhide(p)
    p = up[p]


def unhide(p):
  q = p - 1
  while q != p:
    X = top(q)
    u = up[q]
    d = down[q]
    if X > 0:
      down[u] - q
      up[d] = q
      _len[X] += 1
      q -= 1
    else:
      q = d


def setup(bytes):
  global left, right, _top, up, down, _len, x
  mem = virtual_memory().available
  n = -1
  i = 0

  bytes.seek(0)
  s = bytes.readline().decode('utf-8').strip()  # read line
  o = s.split(',')
  m = int(o[0]) + 2
  l = int(o[2])
  L = int(o[3]) + 2

  opts = [''] * m
  left = [0] * m
  right = [0] * m
  _len = [0] * m
  up = [0] * L
  down = [0] * L
  _top = [0] * L
  x = [0] * m
  N = 0

  print("Memory used after allocating all lists: " + "{:,}".format(mem - virtual_memory().available))

  for i in range(1, m - 1):
    opts[i] = o[1] + str(i)
    left[i] = i - 1
    right[i - 1] = i

  N = i
  if n < 0:
    n = N

  left[N + 1] = N
  right[N] = N + 1
  left[n + 1] = N + 1
  right[N + 1] = n + 1
  left[0] = n
  right[n] = 0

  for i in range(1, N + 1):
    _len[i] = 0
    up[i] = i
    down[i] = i

  M = 0
  p = N + 1
  _top[p] = 0

  while True:
    s = bytes.readline().decode('utf-8').strip()

    if s == '':
      print(str(N) + ' ' + str(L) + ' ' + str(p))
      break

    o = s.split('.')
    k = int(o[0])
    t = [int(a) for a in filter(None, o[1][1:-1].strip().split(','))]
    for j in range(1, k + 1):
      K = t[j - 1]
      _len[K] += 1
      q = up[K]
      up[p + j] = q
      down[q] = p + j
      down[p + j] = K
      up[K] = p + j
      _top[p + j] = K

    M += 1
    down[p] = p + k
    p = p + k + 1
    _top[p] = -M
    up[p] = p - k

    # print(f'{k:3d} {t}')  # print('\n'.join([f'{i:3d} {top(i):3d} {u:3d} {top(u):3d} | {d:3d} {top(d):3d}' for i, (u,d) in enumerate(zip(up, down))]))  # print()

  print(f"  opts: { len(opts):4d}: {' '.join(f'{i:4d}:{v:8}' for i, v in enumerate(opts))}")
  print(f"  left: { len(left):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(left))}")
  print(f" right: {len(right):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(right))}")
  print(f"length: { len(_len):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(_len))}")
  print(f"  top:  { len(_top):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(_top))}")
  print(f"   up:  {   len(up):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(up))}")
  print(f" down:  { len(down):4d}: {' '.join(f'{i:4d}:{v:4d}' for i, v in enumerate(down))}")

  return (N, M, p)


def randomized(N):
  mem = virtual_memory().available

  bytes = io.BytesIO()
  k = randint(4, 8)
  prefix = ''.join(choices(string.ascii_letters + string.digits, k=k))

  n_val = N
  o_val = randint(N, N)
  m_vals = [tuple(sorted(sample(range(1, n_val + 1), randint(n_val // 3, n_val * 2 // 3)))) for _ in range(o_val)]

  print("Memory used: after generating options " + "{:,}".format(mem - virtual_memory().available))

  m_vals = set(m_vals)
  o = [str(n_val), prefix, str(len(m_vals)), str(N + 1 + sum(l + 1 for l in [len(m_val) for m_val in m_vals]))]
  bytes.write(','.join(o).encode() + b'\n')  # write string encoded as bytes

  print("Memory used after unique options: " + "{:,}".format(mem - virtual_memory().available))

  for m_val in m_vals:
    o = [str(len(m_val))]
    o.append(str(m_val))
    bytes.write('.'.join(o).encode() + b'\n')

  print("Serialized size: " + "{:,}".format((bytes.seek(0, io.SEEK_END))))
  bytes.seek(0)  # reset the stream position

  # for line in bytes:
  #   print(line.decode())  # decode bytes to string0

  print("Memory used after writing options: " + "{:,}".format(mem - virtual_memory().available))
  return bytes  # opts[N + 1] = o[1] + str(N + i)


def specified(N, items):
  mem = virtual_memory().available
  n = -1
  i = 0

  bytes = io.BytesIO()
  k = randint(4, 8)
  prefix = ''.join(choices(string.ascii_letters + string.digits, k=k))

  n_val = N
  o_val = len(items)
  m_vals = [tuple(items[i]) for i in range(o_val)]

  print("Memory used: after generating options " + "{:,}".format(mem - virtual_memory().available))

  m_vals = set(tuple(itertools.chain(*m_vals)))
  o = [str(n_val), prefix, str(len(m_vals)), str(N + 1 + sum(l + 1 for l in [len(m_val) for m_val in m_vals]))]
  bytes.write(','.join(o).encode() + b'\n')  # write string encoded as bytes

  print("Memory used after unique options: " + "{:,}".format(mem - virtual_memory().available))

  for m_val in m_vals:
    o = [str(len(m_val))]
    o.extend([str(m_val)])
    bytes.write('.'.join(o).encode() + b'\n')

  print("Serialized size: " + "{:,}".format((bytes.seek(0, io.SEEK_END))))
  bytes.seek(0)  # reset the stream position

  for line in bytes:
    print(line.decode())  # decode bytes to string

  print("Memory used after writing options: " + "{:,}".format(mem - virtual_memory().available))
  return bytes


def convert_rgs(s):
  p = []
  for i, v in enumerate(s):
    v = int(v)
    if v == 0:
      continue
    if v > len(p):
      p.append({i + 1})
    else:
      p[v - 1].add(i + 1)
  return [tuple(q) for q in p]


def run():
  global l
  enter_level = True
  exit_level = False
  while True:
    if enter_level:
      # X2. [Enter level l.]
      i = right[0]
      if i == 0:  # all items have been covered
        visit()  # visit the current solution
        # X8. [Leave level l.]
        if l == 0:
          sys.exit(0)  # no more levels to backtrack, we're done
        l -= 1
        exit_level = True

    if not exit_level:
      if enter_level:
        # X3. [Choose i.]
        i = mrv(i)

        # X4. [Cover i.]
        cover(i)
        if l > N:
          print(f'Termination error: l: {l} is too large already')
          sys.exit(1)
        x[l] = down[i]

      while True:
        # X5. [Try x[l].]
        if x[l] == i:  # we've tried all options for i
          break

        p = x[l] + 1
        while p != x[l]:
          j = top(p)
          if j <= 0:
            p = up[p]
          else:
            cover(j)
            p += 1
            l += 1
            enter_level = True
            exit_level = False
            break

      if p == x[l]:
        break

      if enter_level:
        continue

      # X7. [Backtrack.]
      uncover(i)
      # X8. [Leave level l.]
      if l == 0:
        sys.exit(0)  # no more levels to backtrack, we're done
      l -= 1

    else:
      # X6. [Try again.]
      p = x[l] - 1
      while p != x[l]:
        j = top(p)
        if j <= 0:
          p = down[p]
        else:
          uncover(j)
          p -= 1
      i = top(x[l])
      x[l] = down[x[l]]
      enter_level = False
      exit_level = False


if __name__ == "__main__":
  sys.setrecursionlimit(1 << 16)
  now = time_ns()
  N = 10
  x = test(N, N, N, 1, 1, 0, 1, [0] * (N + 1), lambda l, n, t, x: t > 1 + max(x[0:l]), lambda t, n, k: bool(t < k),
           lambda l, n, k: l <= n)  # partition

  items = [tuple(convert_rgs(y)) for y in sample(x[1:], len(x) - 1)]
  bytes = specified(N, items)
  print("Generate: " + "{:,}".format(int((time_ns() - now) // 1e6)))
  now = time_ns()
  (N, M, Z) = setup(bytes)
  l = 0
  print("Setup: " + "{:,}".format(int((time_ns() - now) // 1e6)))

  level_l()

  #run()
