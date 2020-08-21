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
        x = 32 - (c + 24)
        a[0] = 256 - 2 ** x
    else:
        if c < 16:
            a[]
