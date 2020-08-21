net = [192, 168, 1, 100]
mask = [255, 255, 255, 252]

# c = [1, 1, 1, 1]
# x = net[0]
# y = mask[0]
#
# c[2] = x & y

def find_net_add(net, mask):
    c = [1, 1, 1, 1]
    for i in range(0, 4):
        c[i] = net[i] & mask[i]
    return c

a = find_net_add(net, mask)

test = str(a)
print(type(test), 'OUTPUT: ' + test)
