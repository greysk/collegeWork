from cs50 import get_int

height = 0
# Obtain the height of the pyramid
while height < 1 or height > 8:
    height = get_int('Height: ')

# Print out pyramid using f-string format.
for i in range(1, height + 1):
    print(f'{"#" * i:>{height}}  {"#" * i}')
