# input_network = input('What is the network IP:')
# input_mask = input('What is the mask (255.255.255.192) or CIDR (/24):')
# need to create data validation
# input_num_of_subnets = input('Number of subnets required:  ')

# TEST SEQUENCE
input_network = str('192.168.1.0')
input_mask = str('/24')
n_nets = int(1)




def vlsm():
    # GATHERS THE USERS REQUIRED INFORMATION
    input_labels = {}
    for b in range(0, n_nets):
        # ### TODO: UNCOMMENT TO BRING IN USER INTERACTION
        # name_sub_net = input('Network ' + str(b) + ' Common Name: ')
        # n_hosts = input('Number of hosts required:  ')
        ### TODO:  REMOVE BEFORE FLIGHT
        ### TEST ONLY
        name_sub_net = 'TestNet'
        n_hosts = 52

        new_entry = {name_sub_net: n_hosts}
        input_labels.update(new_entry)
        input_db = sorted(input_labels.items(), key=lambda x: x[1], reverse=True)

    net_ip_array = return_ip_net_array(input_network)
    net_mask_array = return_mask_normalized(input_mask)
    hosts_available = find_hosts(input_mask)
    net_add = find_net_add(net_ip_array, net_mask_array)
    net_wildcard = find_wildcard(net_mask_array)
    net_broadcast = find_broadcast(net_wildcard, net_ip_array)

    print(
        'NETWORK ADDRESS: {0}.{1}.{2}.{3}'.format(net_add[0], net_add[1], net_add[2], net_add[3]))
    print(
        'NETWORK MASK: {0}.{1}.{2}.{3}'.format(net_mask_array[0], net_mask_array[1], net_mask_array[2],
                                               net_mask_array[3]))
    print('TOTAL HOSTS: {}'.format(hosts_available))
    vlsm_db = {
        'Network Common Name': 0,
        'Hosts Required': 0,
        'Hosts Available': 0,
        'Unused Hosts': 0,
        'Network Address:': 0,
        'CIDR': 0,
        'Mask': 0,
        'Usable Range': 0,
        'Broadcast': 0,
        'Wildcard': 0,
    }
    print('~~~~~~')
    print(vlsm_db.items())
    print(input_db)

    #ESTABLISH THE DATA FRAME
    for r in range (0, n_nets):
        vlsm_db['Network Common Name'] = input_db[r][0]
        vlsm_db['Hosts Required'] = input_db[r][1]
        c = find_slash(input_db[r][1])

    # print(labels_sorted[0][1])
    test = str(c)
    print(type(test), 'OUTPUT: ' + test)

### TODO:  This doesn't work. Review
def find_slash(sn_hosts):
    for b in range(33):
        if sn_hosts <= 2 ** b - 2:
            return 32 - b
        else:
            return print('too big')


# def input_user_subnet(n_nets):
#     # GATHERS THE USERS REQUIRED INFORMATION
#     input_labels = {}
#     for b in range(0, n_nets):
#         # ### UNCOMMENT TO BRING IN USER INTERACTION
#         name_sub_net = input('Network ' + str(b) + ' Common Name: ')
#         n_hosts = input('Number of hosts required:  ')
#         ### TEST ONLY
#         # name_sub_net = 'TestNet'
#         # n_hosts = 52
#         new_entry = {name_sub_net: n_hosts}
#         input_labels.update(new_entry)
#         labels_sorted = sorted(input_labels.items(), key=lambda x: x[1], reverse=True)
#         return labels_sorted


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
    bit_available = input_mask.replace('/', '')
    x = 32 - int(bit_available)
    return (2 ** x) - 2


def find_mask(c):
    array_mask = []
    b = c.split('.')
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
#         b = 'hosts ' + str(c)
#     return b
#
#
# # def ordered_hosts(a):
# #     c = []
# #     b = 0
# #     for f in range(1, a):
# #         e = 'name ' + str(f)
# #         d = 'hosts ' + str(f)



