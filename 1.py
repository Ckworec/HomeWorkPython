n1= (13*15)%46 + 1
print(n1)

with open('data.txt', 'r') as input_file:
    a = list(map(int, input_file.read().split()))

a1 = a[0]
a2 = a[1]
max_number = 0
i = 2

for elem in a[2:]:
    if elem == a1 or elem == a2:
        max_number = i
    i += 1

print(max_number + 1)