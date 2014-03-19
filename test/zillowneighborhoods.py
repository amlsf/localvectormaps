# How to convert this to a dictionary?
# dictionary = {"type": "hello"}
# print type(dictionary)

f = open("maps\ZillowNeighborhoods-CA\CAneighborhoods.txt")

x = f.read()

print type(x)
y = dict(x)
print type(y)
