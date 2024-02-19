import io
import string
from random import random, choices, randint, sample


# step 1:
#    setup #encode problem in memory
#    N -< # items
#    Z <- & last spacer
#    l <- 0

# step 2:
#    if right(1) == 0:
#         visit x[1] ... x[l-1]
#          go to step 8

# step 3:
#    mrv i <- right(1) ... right(1), right(1) == 0 #(use MRV heuristic)

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
# step 7: uncover i
# step 8: if l == 0 exit else l--; go to step 6

# cover i:
#    p <- down(1)
#    while p != i:
#        hide p
#        p <- down(1)
#    l <- left(1)
#    r <- right(1)
#    right(1) <- r
#    left(1) <- l

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

# uncover i:
#    l <- left(1)
#    r <- right(1)
#    right(1) <- i
#    left(1) <- i
#    p <- up(1)
#    while p != i:
#        unhide p
#        p <- up(1)

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

# mrv:
#    theta <- sys.maxsize
#    p <- rightop(1)
#    while p != 0:
#        lamda <- len(p)
#        if lamda < theta:
#            theta <- lamda
#            i <- p
#            p <- rightop(1)
#            if theta == 0:
#                return i

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

def setup():
    n = -1
    i = 0
    f = open("input")  # open file
    s = f.readline()  # read line
    o = s.split(' ,')

    opts = {}
    left = {}
    right = {}
    length = {}
    up = {}
    down = {}
    top = {}

    for i in range(1, int(o[0]) + 1):
        i += 1
        opts[i] = o[1] + str(i)
        left[i] = i - 1
        right[i] = i
        if i > int(o[2]):
            n = i - 1
        N = i
        if n < 0:
            n = N
        left[N+1] = N
        right[N] = N + 1
        left[n+1] = N + 1
        right[N+1] = n + 1
        left[0] = n
        right[n] = 0

    for i in range(1, N + 1):
        length[i] = 0
        up[i] = i
        down[i] = i

    M = 0
    p = N + 1
    top[p] = 0

    while True:
        s = f.readline()

        if s == '':
            print(N)
            break
        o = s.split(' .')
        for j in range(1, int(o[0]) + 1):
            k = int(o[j])
            length[k] += 1
            q = up[k]
            up[p+j] = q
            down[q] = p + j
            down[p+j] = k
            up[k] = p + j
            top[p+j] = k
        M += 1
        down[p] = p + int(o[0])
        p = p + int(o[0]) + 1
        top[p] = -M
        up[p] = p - int(o[0])

def reset():
    n = -1
    i = 0
    # Define BytesIO stream to write.
    bytes = io.BytesIO()
    k = randint(4, 8)
    prefix = ''.join(choices(string.ascii_letters + string.digits, k=k))

    n_val = randint(4, 8)
    o = [str(n_val), prefix]
    bytes.write(','.join(o).encode() + b'\n')  # write string encoded as bytes

    seen = set()  # keep track of seen lists
    for i in range(1, 2**n_val// 2) :
        m_val = randint(1, n_val + 1)
        o = [str(m_val)]

        while True:
            sorted_list = sorted(sample(range(1, m_val + 1), randint(1, m_val)))
            # If the list hasn't been seen before, exit the loop
            if tuple(sorted_list) not in seen:
                break
        # Add the list to the set of seen lists
        seen.add(tuple(sorted_list))

        o.append(str(sorted_list))
        bytes.write('.'.join(o).encode() + b'\n')  # write string encoded as bytes

    bytes.seek(0)  # reset the stream position

    # now you can read the byte stream like a normal file
    for line in bytes:
        print(line.decode())  # decode bytes to string

if __name__ == "__main__":
    reset()