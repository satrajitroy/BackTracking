import io
import itertools
import string
import sys
from random import choices, randint, sample
from time import time_ns
from backtrack import test

from psutil import virtual_memory

# opts = None
# left = None
# right = None
# length = None
# up = None
# down = None
# top = None
# x = None
# N = None
# M = None
# Z = None
# l = None

# step 1:
#    setup #encode problem in memory
#    N -< # items
#    Z <- & last spacer
#    l <- 0

def visit(x, l):
  print(f"{visit.__name__}: {[x[i] for i in range(1, l + 1)]}")

# step 2:
#    if right(0) == 0:
#         visit x[1] ... x[l-1]
#          go to step 8


def level_l(x, l):
  print(f'{level_l.__name__} l: {l} right: {right}')
  if right[0] == 0:
    visit(x, l)
    next_l()
  else:
    i = mrv()
    cover(i)
    x[l] = down[i]
    print(f"{level_l.__name__} covered {i} x[{l}]: {x[l]} right: {right}")
    try_l(i)


# step 3:
#    mrv i <- right(1) ... right(1), right(1) == 0 #(use MRV heuristic)

# mrv: (minimum remaining values)
# theta <- sys.maxsize
# p <- right[1]
# while p != 0
#   lamda <- length[p]
#   if lamda < theta:
#     theta <- lamda
#     if theta == 0:
#       return p

#   i <- p
#   p <- right[1]

def mrv():
  # print(f"{mrv.__name__}\nlength: {_len}\nleft. : {left}\nright : {right}")
  theta = sys.maxsize
  p = right[0]
  i = p
  while p != 0:
    # print(f"{mrv.__name__} p: {p}")
    lamda = _len[p]
    if lamda < theta:
      theta = lamda
      i = p
      if theta == 0:
        # print(f"{mrv.__name__} i: {i}")
        break

    p = right[p]

  # print(f"{mrv.__name__} i: {i}")
  return i


# step 4:
#    cover i
#    x[l] <- down(1)


# step 5:
#    if x[l] == :
#        go to step 7
#    else:
#        p <- x[l] + 1;
#        while p != x[l]:
#            j <- top(1);
#            if j <= 0:
#                p <- u(p)
#            else(if j > 0):
#                cover j
#                p++
#                l++
#                go to step 2


def try_l(i):
  global l, _top, up, x
  print(f"{try_l.__name__} l: {l}\ntop: {_top}\nup: {up}")
  if x[l] == i:
    backtrack(i)
  else:
    p = x[l] + 1
    while p != x[l]:
      j = top(p)
      if j > 0:
        cover(j)
        p += 1
        l += 1
        print(f'{try_l.__name__} l: {l} covered {i} right: {right}')
        level_l(x, l)
      else:
        p = up[p]

  retry_l()


def top(p):
  global N, _top
  # if (p < N + 1):
  #   print(f"Error: {p} is out of range for {_top}")
  return _top[p]


# step 6:
#    p <- x[l] - 1;
#    while p != x[l]
#        j <- top(1);
#        if j <= 0:
#            p <- down(1)
#        else: #(j > 0)
#            uncover j
#            p--
#            i <- top(1)
#            x[l] <- down(1)
#            go to step 5


def retry_l():
  print(f'{retry_l.__name__} l: {l}')
  p = x[l] - 1
  while p != x[l]:
    print(f'{l:3d} {p:3d} {x[l]:3d} {top(p):3d} {down[p]:3d}')
    j = _top[p]
    if j > 0:
      uncover(j)
      p -= 1
    else:
      p = down[p]

  print(f'{l:3d} {p:3d} {x[l]:3d} {top(p):3d} {down[p]:3d}')
  i = _top[x[l]]
  x[l] = down[x[l]]
  try_l(i)


# step 7: uncover i


def backtrack(i):
  print(backtrack.__name__)  
  uncover(i)
  next_l()

# step 8: if l == 0 exit else l--; go to step 6


def next_l():
  global l
  print(f"{next_l.__name__} l: {l}")
  if l == 0:
    sys.exit(0)
  else:
    l -= 1
    retry_l()

# cover i:
#    p <- down(1)
#    while p != i:
#        hide p
#        p <- down(1)
#    l <- left(1)
#    r <- right(1)
#    right(1) <- r
#    left(1) <- l

def cover(i):
  global left, right, down
  p = down[i]
  while p != i:
    # print(f"{cover.__name__} covering {i} p: {p}\ndown: {down}")
    hide(p)
    p = down[p]

  l = left[i]
  r = right[i]
  right[l] = r
  left[r] = l


# hide i:
#    q <- p + 1
#    while q != p:
#        x <- top(1)
#        u <- u(q)
#        d <- down(1)
#        if x <= 0:
#            q <- u
#        else: #(x > 0)
#            down(1) <- d
#            u(d) <- u
#            len(x)--
#            q++

def hide(p):
  global _top, up, down, _len
  q = p + 1
  while q != p:
    X = _top[q]
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


# uncover i:
#    l <- left(1)
#    r <- right(1)
#    right(1) <- i
#    left(1) <- i
#    p <- up(1)
#    while p != i:
#        unhide p
#        p <- up(1)

def uncover(i):
  global left, right, _top, up
  l = left[i]
  r = right[i]
  right[l] = i
  left[r] = i

  p = up[i]
  while p != i:
    unhide(p)
    p = up[p]


# unhide i:
#    q <- p - 1
#    while q != p:
#        x <- top(1)
#        u <- up(1)
#        d <- down(1)
#        if x<= 0:
#            q <- d
#        else: #(x > 0)
#            down(1) <- q
#            up(1) <- q
#            len(x)++
#            q--

def unhide(p):
  global _top, up, down, _len
  q = p - 1
  while q != p:
    x = _top[q]
    u = up[q]
    d = down[q]
    if x > 0:
      down[u] - q
      up[d] = q
      _len[x] += 1
      q -= 1
    else:
      q = d


# setup:
#    n <- -1
#    i <- 0
#    f <- fopen("input") # open file
#    s <- f.readline() # read line
#    o <- spilt(s, ' ,')
#    for (i in range(int(1, o[0] + 1)):
#        i++
#        opts[i] <- 0[1] + str(i)
#        left(i) <- i -1
#        right(i) <- i
#        if i > int(o[2]):
#            n <- i -1
#        N <- i
#        if n < 0:
#            n <- N
#        left(N+1) <- N
#        right(N) <- N + 1
#        left(n+1) <- N + 1
#        right(N+1) <- n + 1
#        left(0) <- n
#        right(n) <- 0
#    for (i in range(1, N + 1):
#        length(i) <- 0
#        up(i) <- i
#        down(i) <- i
#    M <- 0
#    p <- N + 1

#    top(p) <- 0
#    while True:
#        s <- f.readline()
#        if s == EOF:
#            return N
#        o <- split(s, ' .')
#        for (j in range(1, o[0) + 1):
#            k <- o[j]
#            length(k) <- length(k) + 1
#            q <- up(k)
#            up(p+j) <- q
#            down(q) <- p + j
#            down(p+j) <- k
#            up(k) <- p + j
#            top(p+j) <- k
#        M++
#        down(p) <- p + o[0]
#        p <- p + o[0] + 1
#        top(p) <- -M
#        up(p) <- p - o[0]

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
  x = [0] * L
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

    # print(f'{k:3d} {t}')
    # print('\n'.join([f'{i:3d} {top(i):3d} {u:3d} {top(u):3d} | {d:3d} {top(d):3d}' for i, (u,d) in enumerate(zip(up, down))]))
    # print()

  print(f"opts: {len(opts)}:, : {opts}")
  print(f"left: {len(left)}:, : {left}")
  print(f"right: {len(right)}:, : {right}")
  print(f"length: {len(_len)}:, : {_len}")
  print(f"top: {len(_top)}:, : {_top}")
  print(f'up: {len(up)}:, : {up}')
  print(f'down: {len(down)}:, : {down}')

  return (N, M, p)


def randomized(N):
  mem = virtual_memory().available
  n = -1
  i = 0

  bytes = io.BytesIO()
  k = randint(4, 8)
  prefix = ''.join(choices(string.ascii_letters + string.digits, k=k))

  n_val = randint(N, N)
  o_val = randint(n_val, n_val)
  m_vals = [tuple(sorted(sample(range(1, n_val + 1), randint(n_val // 3, n_val * 2 // 3))))
            for _ in range(o_val)]

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

  for line in bytes:
    print(line.decode())  # decode bytes to string0

  print("Memory used after writing options: " + "{:,}".format(mem - virtual_memory().available))
  return bytes
  # opts[N + 1] = o[1] + str(N + i)

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
      p.append({i+1})
    else:
      p[v - 1].add(i+1)
  return [tuple(q) for q in p]


if __name__ == "__main__":
  global N, M, Z, l, x

  now = time_ns()
  N = 7
  x = test(N, N, N, 1, 1, 0, 1, [0] * (N+1),
       lambda l, n, t, x: t > 1 + max(x[0:l]),
       lambda t, n, k: bool(t < k),
       lambda l, n, k: l <= n)  # partition

  items = [tuple(convert_rgs(y)) for y in sample(x, 1)]
  bytes = specified(N, items)
  print("Generate: "+"{:,}".format(int((time_ns()-now)//1e6)))
  now = time_ns()
  (N, M, Z) = setup(bytes)
  l = 0
  print("Setup: "+"{:,}".format(int((time_ns()-now)//1e6)))

  level_l(x, l)


# Ubuntu 24
# With 28672 items and equal number of options
# Memory used: 19443474432
# Time to generate: 164322166020 Serialized size: 2722212417
# 28672 411694073 411694072
# left: 28674
# right: 28674
# top: 411694073
# up:411694073
# down: 411694073
# length: 28674
# Memory used: 49528496128
# Time to set up: 120763156546

# With 16384 items and equal number of options
# Memory used: 6290378752
# Time to generate: 51219485085 Serialized size: 850099481
# 16384 134480223 134480222
# left: 16386
# right: 16386
# top: 134480223
# up:134480223
# down: 134480223
# length: 16386
# Memory used: 16145252352
# Time to set up: 39102953370

# With 32768 items and 131072 options
# Memory used: after generating options 45359
# Memory used after unique options: 45362
# Serialized size: 7618964
# Memory used after writing options: 52820
# Time to generate: 471570
# Memory used after allocating all lists: 35801
# left: 32770
# right: 32770
# top: 1171322204
# up:1171322204
# down: 1171322204
# length: 32770
# Memory used: 35806
# Time to setup: 15335

# With 24576 items and 98304 options
# Memory used: after generating options 46689
# Memory used after unique options: 46695
# Serialized size: 7724769
# Memory used after writing options: 54256
# Time to generate: 485623
# Memory used after allocating all lists: 36932
# left: 24578
# right: 24578
# top: 1208102790
# up:1208102790
# down: 1208102790
# length: 24578
# Memory used: 36934
# Time to setup: 16000

# Windows 10
# With 24576 items and equal number of options
# Serialized size: 1930822
# Memory used: 9326
# Time to generate: 2203477
# left: 24578
# right: 24578
# top: 301968262
# up:301968262
# down: 301968262
# length: 24578
# Memory used: 9285
# Time to set up: 21487
#
# With 28672 items and equal number of options
# Serialized size: 2656690
# Memory used: 10702
# Time to generate: 4453042
# left: 28674
# right: 28674
# top: 411427330
# up:411427330
# down: 411427330
# length: 28674
# Memory used: 11731
# Time to set up: 35793