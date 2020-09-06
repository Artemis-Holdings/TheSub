
def validate_ip(ip):
    ip = ip.split('.')
    if len(ip) == 4:
        for i in range(0, 4):
            if int(ip[i]) >= int(255):
                print('Out of range Octett: {}'.format(ip[i]))
                error_code = int(1)
                return error_code
            else:
                error_code = int(69)
                return error_code
    else:
        error_code = int(2)
        return  error_code



print(validate_ip('300.168.1.1'))



# def validate_ip(ip):
#     ip = ip.split('.')
#     for i in range(0, 4):
#         if len(ip) == 4:
#                 for i in range(0, 4):
#                     if int(ip[i]) <= int(255):
#                         print(ip[i])
#                         error_code = int(69)
#                         return error_code
#         else:
#             error_code = int(1)
#             return error_code