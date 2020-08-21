# input_network = input("What is the network IP:")
# input_mask = input("What is the mask (255.255.255.192) or CIDR (/24):")
# need to create data validation
# input_num_of_subnets = input("Number of subnets required:  ")

# TEST SEQUENCE
input_network = str('192.168.1.0')
input_mask = str('/24')
input_num_of_subnets = int(1)


# def change_subnet_number():
#     c = input_num_of_subnets
#     for b in range(int(c)):
#         net_mem = input("Network " + str(b) + " Common Name: ")
#         a = input("Number of hosts required:  ")
#     nets = c


def vlsm():
    n_nets = input_num_of_subnets
    for b in range(int(n_nets)):
        # ### UNCOMMENT TO BRING IN USER INTERACTION
        # net_mem = input("Network " + str(b) + " Common Name: ")
        # a = input("Number of hosts required:  ")

        ### TEST ONLY
        name_sub_net = 'TestNet'
        n_hosts = 52

    net_ip_array = return_ip_net_array(input_network)
    net_mask_array = return_mask_normalized(input_mask)
    hosts_available = find_hosts(input_mask)
    net_add = find_net_add(net_ip_array, net_mask_array)
    net_wildcard = find_wildcard(net_mask_array)
    net_broadcast = find_broadcast(net_wildcard, net_ip_array)
    # a = sum_hosts(n_nets)

    test = str(a)
    print(type(test), 'OUTPUT: ' + test)


    #
    #
    # d = ordered_hosts(n_nets)
    # print('the network %d . %d . d% . %d / %d' % (c[0], c[1], c[2], c[3], n))


def return_ip_net_array(input_network):
    b = [int(i) for i in input_network.split('.')]
    return b


def return_mask_normalized(input_mask):
    if '.' in input_mask:
        mask_given = [int(i) for i in input_mask.split('.')]
        return mask_given
    else:
        cidr = input_mask.replace('/', '')
        mask_from_cidr = find_mask(cidr)
        mask_found = mask_from_cidr  # .split(',')
        return mask_found


def find_hosts(input_mask):
    cidr = input_mask.replace('/', '')
    x = 32 - int(cidr)
    return (2 ** x) - 2


def find_mask(c):
    array_mask = []
    b = c.split(".")
    for i in range(0, 4):
        array_mask.append(i)
    c = int(c)
    if c < 8:
        w = 32 - (c + 24)
        array_mask[0] = 256 - 2 ** w
        array_mask[1] = 0
        array_mask[2] = 0
        array_mask[3] = 0

    else:
        if c < 16:
            x = 32 - (c + 16)
            array_mask[0] = 255
            array_mask[1] = 256 - (2 ** x)
            array_mask[2] = 0
            array_mask[3] = 0
        else:
            if c < 24:
                y = 32 - (c + 8)
                array_mask[0] = 255
                array_mask[1] = 255
                array_mask[2] = 256 - (2 ** y)
                array_mask[3] = 0
            else:
                z = 32 - c
                array_mask[0] = 255
                array_mask[1] = 255
                array_mask[2] = 255
                array_mask[3] = 256 - (2 ** z)
    return array_mask



def find_net_add(net, mask):
    c = [1, 1, 1, 1]
    for i in range(0, 4):
        c[i] = net[i] & mask[i]
    return c


def find_wildcard(a):
    c = [1, 1, 1, 1]
    for b in range(0, 4):
        c[b] = 255 - a[b]
    return c


def find_broadcast(wildcard, ip):
    d = [1, 1, 1, 1]
    for i in range(0, 4):
        d[i] = wildcard[i] or int(ip[i])
    return d


# def sum_hosts(input_num_of_subnets):
#     d = 0
#     for c in range(1, input_num_of_subnets):
#         b = "hosts " + str(c)
#     return b
#
#
# # def ordered_hosts(a):
# #     c = []
# #     b = 0
# #     for f in range(1, a):
# #         e = "name " + str(f)
# #         d = "hosts " + str(f)


vlsm()
