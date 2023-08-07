# 列表是有序集合，序号从0开始，列表名建议用复数
family_members = ['yiping', 'meimei', 'father', 'mother']
print(family_members[0])
print(family_members[0].title())
print(family_members[-1])
news_of_the_year = f"{family_members[-3].title()} has become the new member of my family."
print(news_of_the_year)
print()

# 修改列表元素
print(family_members)
family_members[1] = 'choubao'
print(family_members)
print()

# 用append()添加元素到列表最后
family_members.append('pipi')
print(family_members)
print()

# 可以用append()来动态创建列表
yipings_girlfriends = []
yipings_girlfriends.append("girl1")
yipings_girlfriends.append("girl2")
yipings_girlfriends.append("girl3")
yipings_girlfriends.append("girl4")
yipings_girlfriends.append("kiphony the angel")
print(yipings_girlfriends)
print()

# 用insert()往列表中插入元素
family_members.insert(2, 'manman')
print(family_members)
print()

# 使用del通过序号删除元素
retail_stores = ['r401', 'r359', 'r389', 'r390', 'r581', 'r683', 'r705']
print(retail_stores)
del retail_stores[0]
print(retail_stores)
print()

# 使用pop()弹出最后一个元素
closed_store = retail_stores.pop()
print(retail_stores)
print(closed_store)
closed_stores = []
closed_stores.append(closed_store)
print(closed_stores)
print()

# 给pop()传参数，通过序号弹出一个元素
closed_store = retail_stores.pop(0)
print(retail_stores)
print(closed_store)
closed_stores.append(closed_store)
print(closed_stores)
print()

# 使用remove()通过值删除元素，remove()只删除第一次出现这个值的元素，如果同一个值在列表中出现多次，要用循环一个个删
retail_stores.remove('r581')
print(retail_stores)
print()

# 如果想保留remove()删掉的元素，则先把要删除的元素赋给一个变量
cost_save = 'r390'
retail_stores.remove(cost_save)
print(retail_stores)
print(cost_save)
print()

# 使用sort()按字母表排序，列表顺序永久改变
retail_stores = ['r401', 'r359', 'r389', 'r390', 'r581', 'r683', 'r705']
retail_stores.sort()
print(retail_stores)
retail_stores.sort(reverse=True)
print(retail_stores)
print()

# 使用sorted()按字母表临时排序，原列表不变
names = ['michael', 'derek', 'shawn', 'ben', 'joseph']
print(sorted(names))
print(sorted(names, reverse=True))
print(names)
print()

# 使用reverse()对原列表反向排序，列表顺序永久改变
names.reverse()
print(names)
print()

# 使用len()计算列表长度
names_len = len(names)
print(names_len)
