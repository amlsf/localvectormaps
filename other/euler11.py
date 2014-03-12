# THOUGHTS on possible data structures:
# TODO list of lists or dictionary of lists better? 
# 1) could use a list of lists
# 2) or a dictionary with keys as row number and value as lists

f = open("euler11.txt")

rows = {}
i = 0

# creates dictionary of rows - key is row number, value is list of each row's items
for line in f:
    rows[i] = line.split()
# TODO should I avoid double for loop? 
# converts elements to integers
    for x in range(len(rows[i])):
        rows[i][x] = int(rows[i][x])
    i += 1
# print rows


# THOUGHTS on how to calculate
# 2) precalculate everything into a new data structure and find the max? 
# 3) calculate as you loop and keep the max as you go? 
# 1) find the best 4 consecutive individual numbers without having to tabulate anything? 
# Need to do: 1) downwards, 2) sideways, 3-4) diagonal down & down (need to convert?)

def product(listy):
    product = 1
    for item in listy: 
        product *= item
    return product


# Calculating sideways
# TODO should I avoid double for loop?
def maximum(dicty):
    max_prod = 0

    for i in range(20):
        for x in range(20): 
# horizontally
            if x+3 < 20:
                # print dicty[i][x:x+4], product(dicty[i][x:x+4])
                if product(dicty[i][x:x+4]) > max_prod:
                    max_prod = product(dicty[i][x:x+4])
                    # max_list = dicty[i][x+1:x+5]
                    # row = i
                    # starting_column = x+1
                    # print (max_prod, max_list, row, starting_column) # should be 48477312
# vertically 
            if x+3 < 20:
                vert_list = [dicty[x][i], dicty[x+1][i], dicty[x+2][i], dicty[x+3][i]]
                if product(vert_list) > max_prod:
                    max_prod = product(vert_list)
# diagonally tilt left
            if i+3 < 20 and x-3 >=0:
                dl_list = [dicty[i][x], dicty[i+1][x-1], dicty[i+2][x-2], dicty[i+3][x-3]]
                if product(dl_list) > max_prod:
                    max_prod = product(dl_list)
# diagonally tilt right
            if i+3 < 20 and x+3 < 20:
                dr_list = [dicty[i][x], dicty[i+1][x+1], dicty[i+2][x+2], dicty[i+3][x+3]]
                if product(dr_list) > max_prod:
                    max_prod = product(dr_list)

    return max_prod

print maximum(rows)


