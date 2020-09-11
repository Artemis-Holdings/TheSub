#                            |`-:_
#   ,----....____            |    `+.
#  (             ````----....|___   |
#   \     _                      ````----....____
#    \    _)                                     ```---.._
#     \                                                   \
#   )`.\  )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.   )
# -'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `
# The Sub: Expeditionary VLSM Calculatorr
# Documentation at: https://github.com/TheMagicNacho
# v0.1.0
# ------------------------------------------------
from tabulate import tabulate


def main():
    try:
        usr_input_network = init_input()
        input_user_db, input_labels_db = mask_input(usr_input_network)
        db = vlsm(input_user_db, input_labels_db)
        try:
            printer(db, input_user_db)
            printer_lite(db, input_user_db)
        except:
            print('!!!Tabulate module missing. Use CSV!!!')
            printer_lite(db, input_user_db)
    except:
        print('RESTART: General Error.')
        main()


def vlsm(input_user_db, input_labels_db):
    og = dict(net_common_name='name', hosts_req=0, hosts_avail=0, hosts_unused=0, net_add=[0, 0, 0, 0], cidr=0,
              sub_mask=[0, 0, 0, 0], sub_start=[0, 0, 0, 0], sub_end=[0, 0, 0, 0], sub_broad=[0, 0, 0, 0],
              sub_wild=[0, 0, 0, 0], sub_delta_r=0)
    n_nets = range(0, input_user_db[0])
    db = {}
    for i in n_nets:
        db[i] = og.copy()
        db[i]['net_common_name'] = input_labels_db[i][0]
        db[i]['hosts_req'] = input_labels_db[i][1]

        if i == 0:
            db[0]['net_add'] = input_user_db[1].copy()
            db[0]['cidr'] = int(find_slash(db[0].get('hosts_req')))
            db[0]['hosts_avail'] = int(find_hosts(db[0].get('cidr')))
            db[0]['hosts_unused'] = db[i].get('hosts_avail') - db[0].get('hosts_req')
            db[0]['sub_mask'] = find_mask(db[0].get('cidr'))
            db[0]['sub_delta_r'] = db[0].get('hosts_avail') + 2
            db[0]['sub_start'] = find_start(db[0], db[0].get('net_add'))
            db[0]['sub_wild'] = find_wildcard(db[0].get('sub_mask'))
            db[0]['sub_broad'] = find_broadcast(db[0].get('sub_wild'), db[0].get('net_add'))
            db[0]['sub_end'] = find_end(db[0], db[0].get('sub_broad'))

        else:
            db[i]['net_add'] = find_start(db[i], db[i - 1].get('sub_broad'))
            db[i]['cidr'] = int(find_slash(db[i].get('hosts_req')))
            db[i]['hosts_avail'] = int(find_hosts(db[i].get('cidr')))
            db[i]['hosts_unused'] = db[i].get('hosts_avail') - db[i].get('hosts_req')
            db[i]['sub_mask'] = find_mask(db[i].get('cidr'))
            db[i]['sub_delta_r'] = db[i].get('hosts_avail') + 2
            db[i]['sub_start'] = find_start(db[i], db[i].get('net_add'))
            db[i]['sub_wild'] = find_wildcard(db[i].get('sub_mask'))
            db[i]['sub_broad'] = find_broadcast(db[i].get('sub_wild'), db[i].get('net_add'))
            db[i]['sub_end'] = find_end(db[i], db[i].get('sub_broad'))
    return db


def find_start(db, net_add):
    db['sub_start'][3] = net_add[3] + 1
    for b in range(0, 2):
        db['sub_start'][b] = net_add[b]
    start = db['sub_start'].copy()
    return start


def find_end(db, net_broad):
    db['sub_end'][3] = net_broad[3] - 1
    for b in range(0, 2):
        db['sub_end'][b] = net_broad[b]
    end = db['sub_end'].copy()
    return end


def find_slash(sn_hosts):
    for i in range(0, sn_hosts):
        x = 2 ** i
        if x > sn_hosts + 2:
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
        mask_found = mask_from_cidr
        return mask_found


def return_cidr_normalized(input_cidr):
    mask = input_cidr.split('.')
    if '/' in input_cidr:
        cidr_given = int(input_cidr.replace('/', ''))
        if cidr_given <= int(32):
            return cidr_given
        else:
            print('RESTART: CIDR must be less than 32')
            main()
    elif int(input_cidr):
        input_cidrx = int(input_cidr)
        if input_cidrx <= 32:
            return input_cidrx
        else:
            print('RESTART: CIDR must be less than 32')
            main()

    elif len(mask) == 4:
        for i in range(0, 4):
            maskx = input_cidr[i]
            if int(maskx) <= int(255):
                mask_array = [int(i) for i in input_cidr.split('.')]
                return dec_to_bin(mask_array)
            else:
                print('RESTART: Error with mask octett {}'.format(maskx[i]))
                main()
    else:
        print('RESTART General Error with Subnet Mask')
        main()


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
        d[i] = wildcard[i] | int(net_add[i])
    return d


def printer(db, u):
    table = []
    print('EASY READ FORMAT')
    print("==================")
    for i in range(0, u[0]):
        table.append(db[i].values())
    headers = db[0].keys()
    print(tabulate(table, headers, tablefmt="pipe", stralign='center', numalign='left'))



def printer_lite(db, input_user_db):
    table = []
    print('CSV FORMAT\n~~Copy and Paste the following into a .txt then import the file to excel. Delimitator is colon '
          '(:)~~')
    print("==================")
    for header in db[0].keys():
        print(header, end=':')
    print('\n')
    for i in range(0, input_user_db[0]):
        table.append(db[i].values())
        x = table[i]
        y = list(x)
        for j in range(0, len(y)):
            d = y[j]
            print(d, end=':')
        print('\n')
    main()


def validate_ip(ip):
    ip = ip.split('.')
    try:
        for i in range(0, 4):
            ipx = ip[i]
            if ipx.isalpha():
                print('RESTART: Error with octett {}'.format(ip[i]))
                print('IP must be integer with "." between octett.')
                main()
            elif int(ipx) <= int(255) and not ipx.isalpha():
                if len(ip) == 4:
                    pass
                else:
                    print('RESTART: IP address too short.')

                    main()
            else:
                print('RESTART: Error with octett {}'.format(ip[i]))
                main()
    except:
        print('RESTART: General error with Net IP. Verify entry is correct.')
        main()


def pre_process(input_network, input_mask, n_nets):
    input_user_db = []

    net_mask_array = return_mask_normalized(input_mask)
    net_cidr = return_cidr_normalized(input_mask)
    input_user_db.append(n_nets)
    input_user_db.append([int(i) for i in input_network.split('.')])
    input_user_db.append(net_mask_array)
    input_user_db.append(net_cidr)
    return input_user_db


def init_input():
    input_network = input('What is the network IPv4 address: ')
    ip_code = validate_ip(input_network)
    if ip_code is None:
        pass
    else:
        print('RESTART:  ERROR CODE: {}'.format(ip_code))
        main()
    return input_network


def mask_input(input_net):
    input_labels_db = []

    input_mask = input('What is the mask (255.255.255.192) or CIDR (/24): ')
    n_nets = int(input('Number of subnets required: '))
    input_user_db = pre_process(input_net, input_mask, n_nets)
    for b in range(0, n_nets):

        name_sub_net = input('Network ' + str(b) + ' Common Name: ')
        try:
            n_hosts = int(input('Number of hosts required: '))
            new_entry = [name_sub_net, n_hosts]
            input_labels_db.append(new_entry)
            input_labels_db = sorted(input_labels_db, key=lambda x: x[1], reverse=True)
        except:
            print('IGNORING INPUT: Value must be an integer.')
            pass
    return input_user_db, input_labels_db




if __name__ == '__main__':
    main()
