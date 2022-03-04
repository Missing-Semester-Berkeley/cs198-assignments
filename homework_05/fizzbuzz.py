def fizz_buzz(limit):
    for i in range(1, limit):
        if i % 3 == 0:
            print('fizz', end='')
        if i % 3 and i % 5:
            print(i)
        else:
            print()

def main():
    fizz_buzz(16)

main()
