# Gather user information to start calculations
def input_user():
    #### INITIALIZE DATABASES !!!!
    input_labels_db = {}
    input_user_db = []

    ###### START OF INPUTS !!!!
    # TODO: Create Data Validation

    # TODO: Change this block for user interaction.
    # input_network = input('What is the network IP:')
    # input_mask = input('What is the mask (255.255.255.192) or CIDR (/24):')
    # input_num_of_subnets = input('Number of subnets required:  ')

    ### TODO: !!!TEST SEQUENCE ONLY!!! REMOVE BEFORE FLIGHT
    input_network = str('192.168.1.0')
    input_mask = str('/17')
    n_nets = int(1)

    ### PRE-PROCESSING !!!
    net_mask_array = return_mask_normalized(input_mask)
    net_cidr = return_cidr_normalized(input_mask)

    #### ADDS THE USER INPUT INTO A DICTIONARY !!!
    input_user_db.append(n_nets)
    input_user_db.append([int(i) for i in input_network.split('.')])
    input_user_db.append(net_mask_array)
    input_user_db.append(net_cidr)

    for b in range(0, n_nets):
        # ### TODO: UNCOMMENT TO BRING IN USER INTERACTION
        # name_sub_net = input('Network ' + str(b) + ' Common Name: ')
        # n_hosts = input('Number of hosts required:  ')
        ### TODO: !!!TEST SEQUENCE ONLY!!! REMOVE BEFORE FLIGHT
        name_sub_net = 'TestNet'
        n_hosts = 52

        new_entry = {name_sub_net: n_hosts}
        input_labels_db.update(new_entry)
    input_labels_db = sorted(input_labels_db.items(), key=lambda x: x[1], reverse=False)

    return input_user_db, input_labels_db


# Input User Database:  Number Of networks required, IP address in array, Mask in array, CIDR
# Input Labels Database:  Common Name, Hosts Required

def vlan(input_user_db, input_labels_db):
    print(input_labels_db)
    print(input_user_db)
    og = dict(net_common_name='name', hosts_req=0, hosts_avail=0, hosts_unused=0, net_add=[0, 0, 0, 0], cidr=0,
              sub_mask=[0, 0, 0, 0], sub_start=[0, 0, 0, 0], sub_end=[0, 0, 0, 0], sub_broad=[0, 0, 0, 0],
              sub_wild=[0, 0, 0, 0], sub_delta_r=0)
    n_nets = range(0, input_user_db[0])
    db = {}
    for i in n_nets:
        db[i] = og.copy()
        db[i]['net_common_name'] = str(input_labels_db[i][0])
        db[i]['hosts_req'] = int(input_labels_db[i][1])
        if i == 0:
            db[i]['net_add'] = input_user_db[1]
            db[i]['cidr'] = find_slash(db[i]['hosts_req'])
            db[i]['hosts_avail'] = find_hosts(db[i]['cidr'])
            db[i]['hosts_unused'] = db[i]['hosts_avail'] - db[i]['hosts_req']
            db[i]['sub_mask'] = find_mask(db[i]['cidr'])
            db[i]['sub_delta_r'] = db[i]['hosts_avail'] + 2
            db[i]['sub_start'] = find_start(db[i], db[i]['net_add'])
            db[i]['sub_wild'] = find_wildcard(db[i]['sub_mask'])
            db[i]['sub_broad'] = find_broadcast(db[i]['sub_wild'], db[i]['net_add'])
            db[i]['sub_end'] = find_end(db[i], db[i]['sub_broad'])
        else:

            break
            # broadcast plus one

    print(db)


def find_start(db, net_add):

    db['sub_start'][3] = net_add[3] + 1
    for b in range(0, 2):
        db['sub_start'][b] = net_add[b]
    start = db['sub_start']
    return start


def find_end(db, net_broad):
    db['sub_end'][3] = net_broad[3] - 1
    for b in range(0, 2):
        db['sub_end'][b] = net_broad[b]
    end = db['sub_end']
    return end


def find_slash(sn_hosts):
    for i in range(0, sn_hosts):
        x = 2 ** i
        if x > sn_hosts - 2:
            return 32 - i
        else:
            continue


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


def return_cidr_normalized(input_cidr):
    if '/' in input_cidr:
        cidr_given = int(input_cidr.replace('/', ''))
        return cidr_given
    else:
        mask_array = [int(i) for i in input_cidr.split('.')]
        return dec_to_bin(mask_array)


def dec_to_bin(mask_array):
    mask_bin = []
    for i in range(0, 4):
        z = str(bin(mask_array[i]).replace("0b", ""))
        x = z.count('1')
        mask_bin.insert(i, x)
    return sum(mask_bin)


def find_hosts(found_cidr):
    x = 32 - int(found_cidr)
    return (2 ** x) - 2


def find_mask(c):
    array_mask = []
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


def find_wildcard(sub_mask):
    c = [1, 1, 1, 1]
    for b in range(0, 4):
        c[b] = 255 - sub_mask[b]
    return c


def find_broadcast(wildcard, net_add):
    d = [1, 1, 1, 1]
    for i in range(0, 4):
        d[i] = wildcard[i] or int(net_add[i])
    return d


userdb, labelsdb = input_user()
vlan(userdb, labelsdb)
