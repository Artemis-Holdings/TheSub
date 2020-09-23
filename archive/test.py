db = {0: {'net_common_name': 'sadfdsf', 'hosts_req': 99, 'hosts_avail': 126, 'hosts_unused': 27,
          'net_add': [192, 168, 1, 1], 'cidr': 25, 'sub_mask': [255, 255, 255, 128], 'sub_start': [192, 168, 0, 2],
          'sub_end': [192, 168, 0, 126], 'sub_broad': [192, 168, 1, 127], 'sub_wild': [0, 0, 0, 127],
          'sub_delta_r': 128},
      1: {'net_common_name': 'assdaas', 'hosts_req': 66, 'hosts_avail': 126, 'hosts_unused': 60,
          'net_add': [0, 0, 0, 0], 'cidr': 25, 'sub_mask': [255, 255, 255, 128], 'sub_start': [0, 0, 0, 0],
          'sub_end': [192, 168, 0, 254], 'sub_broad': [192, 168, 0, 255], 'sub_wild': [0, 0, 0, 127],
          'sub_delta_r': 128},
      2: {'net_common_name': 'srag', 'hosts_req': 33, 'hosts_avail': 62, 'hosts_unused': 29,
          'net_add': [192, 168, 0, 256], 'cidr': 26, 'sub_mask': [255, 255, 255, 192],
          'sub_start': [192, 168, 0, 257], 'sub_end': [192, 168, 0, 318],
          'sub_broad': [192, 168, 0, 319], 'sub_wild': [0, 0, 0, 63], 'sub_delta_r': 64}}
user_db = [3, [192, 168, 1, 1], [255, 255, 255, 0], 24]

# net_add from DB 'sub_broad': [192, 168, 1, 127]
def find_net(db, net_add):
    if net_add[3] <= 255:
        db['net_add'][3] = net_add[3] + 1
        db['net_add'][2] = net_add[2]
        db['net_add'][1] = net_add[1]
        db['net_add'][0] = net_add[0]
    elif net_add[2] <= 255:
        db['net_add'][3] = int(0)
        db['net_add'][2] = net_add[2] + 1
        db['net_add'][1] = net_add[1]
        db['net_add'][0] = net_add[0]
    elif net_add[1] <= 255:
        db['net_add'][3] = int(0)
        db['net_add'][2] = int(0)
        db['net_add'][1] = net_add[1] + 1
        db['net_add'][0] = net_add[0]
    else:
        db['net_add'][3] = int(0)
        db['net_add'][2] = int(0)
        db['net_add'][1] = int(0)
        db['net_add'][0] = net_add[1] + 1

    start = db['net_add'].copy()
    return start


# index 1 should replace by i during production
#db at i (first position) assigns the dictionary
print(find_net(db[1], db[1 - 1].get('sub_broad')))
