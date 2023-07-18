from collections import Counter

my_list = [1, 2, 3, 2, 1, 2, 3, 4, 5, 1, 2, 2, 3]

counter = Counter(my_list)
most_common = counter.most_common(1)

most_common_element = most_common[0][0]
count = most_common[0][1]

print(f"最多的元素是: {most_common_element}")
print(f"出现的次数是: {count}")
