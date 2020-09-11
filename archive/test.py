db = {0: {'net_common_name': 'sadfdsf', 'hosts_req': 99, 'hosts_avail': 126, 'hosts_unused': 27,
          'net_add': [192, 168, 1, 1], 'cidr': 25, 'sub_mask': [255, 255, 255, 128], 'sub_start': [192, 168, 0, 2],
          'sub_end': [192, 168, 0, 126], 'sub_broad': [192, 168, 1, 127], 'sub_wild': [0, 0, 0, 127],
          'sub_delta_r': 128},
      1: {'net_common_name': 'assdaas', 'hosts_req': 66, 'hosts_avail': 126, 'hosts_unused': 60,
          'net_add': [192, 168, 0, 128], 'cidr': 25, 'sub_mask': [255, 255, 255, 128], 'sub_start': [192, 168, 0, 129],
          'sub_end': [192, 168, 0, 254], 'sub_broad': [192, 168, 0, 255], 'sub_wild': [0, 0, 0, 127],
          'sub_delta_r': 128},
      2: {'net_common_name': 'srag', 'hosts_req': 33, 'hosts_avail': 62, 'hosts_unused': 29,
          'net_add': [192, 168, 0, 256], 'cidr': 26, 'sub_mask': [255, 255, 255, 192],
          'sub_start': [192, 168, 0, 257], 'sub_end': [192, 168, 0, 318],
          'sub_broad': [192, 168, 0, 319], 'sub_wild': [0, 0, 0, 63], 'sub_delta_r': 64}}
user_db = [3, [192, 168, 1, 1], [255, 255, 255, 0], 24]


def printer_lite(db, input_user_db):
    table = []
    for header in db[0].keys():
        print(header, end=',')
    for i in range(0, input_user_db[0]):
        table.append(db[i].values())
        x = table[i]
        y = list(x)
        for j in range(0, len(y)):
            d = y[j]
            print(d, end=',')



printer_lite(db, user_db)
