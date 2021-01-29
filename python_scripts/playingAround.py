# import re
# list1 = [1,2,3,4,5,6,7,8,9,10]
#
# def add_it_up(num):
#     [cur, sums] = [0, 0]
#     for x in range(num + 1):
#         cur = x
#         sums += cur
#     return sums
#
# # print(add_it_up(0))
#
#
# def ceaser_cypher(str, n):
#     'abcdefghijklmnopqrstuvwxyz'
#     # build alhabet
#     alphabet = ''.join([chr(ord('a') + num) for num in range(26)])
#     remainder = None
#     code = ''
#     for letr in str:
#         letter_num = ord(letr) + n
#         last_letter = ord('z')
#         sc = re.findall('\W',letr)
#         if sc:
#             code += letr
#         elif letter_num >= last_letter:
#             remainder = (letter_num - last_letter)
#             code += alphabet[remainder - 1]
#         else:
#             code += chr(ord(f'{letr}') + n)
#
#     return code
#
# print(ceaser_cypher('yy y#$d xyz', 8))
#
## [1,2,3,4,6,7]
def find_num(arr):
    missing_number = [num - 1 for num in arr if num - 1 not in arr and num - 1 != 0]
    return missing_number

# print(find_num([-1,3,5,7,8]))

def fib(num):
    # Set base
    results = []
    a, b = 0, 1
    for x in range(num):
        a, b = b, a + b
        results.append(a)

    return results

print(fib(10))

