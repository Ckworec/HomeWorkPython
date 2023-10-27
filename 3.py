n3= (13*29 + 7)%23 + 1
print(n3)

with open('data.txt', 'r') as input_file:
    a = list(map(int, input_file.read().split()))

min = a[0]
max = a[0]
counter = 0

for elem in a:
    if elem < min:
        min = elem
    if elem > max:
        max = elem
    if elem == a[0]:
        counter += 1

if counter == len(a):
    print(a)
else:        
    arr = [min + (elem - min) / (max - min) for elem in a]
    print(arr)