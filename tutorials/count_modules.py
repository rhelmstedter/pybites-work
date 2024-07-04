with open("./clean_install/modules.txt") as modules:
    lines = modules.read().strip().splitlines()


print(lines)
count = 0
for line in lines[1:-2]:
    count += len(line.split())

print(count)
