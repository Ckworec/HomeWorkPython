n2= (13 * 29) % 23 + 1
print(n2)

print("Enter the power of equations: ", end = "")
c = int(input())

arr = [0 for i in range(0, c + 1)]

arr[0] = 1

for i in range(1, c + 1):
    for j in range(i, 0, -1):
        arr[j] = arr[j - 1] + arr[j]

print(arr)