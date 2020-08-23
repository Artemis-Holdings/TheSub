net = [192, 168, 1, 0]
mask = [255, 255, 255, 0]


def find_start(net, mask):
    net_bin = []
    mas_bin = []
    for i in range(0, 4):
        z = int(bin(net[i]), 2)  # .replace('0b', ''))
        x = int(bin(net[i]), 2)  # .replace('0b', ''))
        net_bin.insert(i, z)
        mas_bin.insert(i, z)

    c = [1, 1, 1, 1]
    for i in range(0, 4):
        c[i] = bin(net_bin[i] & mas_bin[i]) + 1

    print(c)


# find_start(net, mask)


x = 192 & 24
print(x)