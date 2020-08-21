input_network = input("What is the network IP prefix in slash notation:")
# need to create data validation
input_num_of_subnets = input("Number of subnets required:  ")


def change_subnet_number():
    c = input_num_of_subnets
    for b in range(int(c)):
        net_mem = input("Network " + str(b) + " Common Name: ")
        a = input("Number of hosts required:  ")
    nets = c


def vlsm():
    h = input_network
    h = h.replace('/^\s+|\s+$/g', '')

    n = return_slash(h)
    g = find_hosts(n)
    m = return_ip(h)
    q = find_mask(n)
    c = find_net_add(m, q)



def return_slash(a):
    b = a.split('/')
    return b[1]


def find_hosts(a):
    x = 32 - a
    return (2 ** x) - 2


def return_ip(a):
    b = a.split('/')
    return b[0].split('.')


def find_mask(c):
    a = []
    for b in range(0, 4):
        a[b] = 0
    if c < 8:
        w = 32 - (c + 24)
        a[0] = 256 - 2 ** w
    else:
        if c < 16:
            a[0] = 255
            x = 32 - (c + 16)
            a[1] = 256 - (2 ** x)
        else:
            if c < 24:
                y = 32 - (c + 8)
                a[0] = 255
                a[1] = 255
                a[2] = 256 - (2 ** y)
            else:
                z = 32 - c
                a[0] = 255
                a[1] = 255
                a[2] = 255
                a[3] = 256 - (2 ** z)
    return a


def find_net_add(a, b):
    c = []
    for d in range(0, 4):
        c[d] = a[d] & b[d]
    return c

def find_wildcard(a):
    c = []
    for b in range(0, 4):
        c[b] = 255 - a[b]

