# if后面的表达式称为条件测试(conditional test)，条件测试返回True或False，返回True就执行if后面的代码，返回False就跳过if后面的代码
cars = ['audi', 'bmw', 'subaru', 'toyota']
for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())
print()

# 判断两个字符串是否相同是大小写敏感的，可以用lower()把变量值转换成全小写再做判断
user_name = 'John'
print(user_name == 'john')
print(user_name.lower() == 'john')
print()

# 用!=判断不等于
requested_pc = 'dell'
if requested_pc != 'macbook':
    print(("Hold the macbook!"))
print()

# 数字比较
age = 18
print(age != 15)
print(age == 18)
print(age < 21)
print(age <= 21)
print(age > 21)
print(age >= 21)
print()

# 多条件测试, and是两个条件都要True才返回True，or是两个条件只要有一个是True就返回True
age_0 = 22
age_1 = 18
print(age_0 >= 21 and age_1 >= 21)
print(age_0 >= 21 or age_1 >= 21)
# 为了看的清楚，可以用括号把单个条件测试括起来: (age_0 >= 21) and (age_1 >= 21)
print()

# 用in判断一个item在列表中是否已存在
family_members = ['yiping', 'choubao', 'manman', 'tuntun', 'father', 'mother', 'pipi']
print('yiping' in family_members)
print('xiaolaodi' in family_members)
print()

# 用not in判断一个item在列表中是否不存在
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'
if user not in banned_users:
    print(f"{user.title()}, you can post a response if you wish.")
print()

# 布尔表达式，布尔表达式是条件测试的另一种说法，布尔值不是True就是False，可以把布尔值赋给变量
game_active = True
can_edit = False

# if-else语句
age = 17
if age >= 18:
    print("You are old enough to vote!")
else:
    print("Sorry, you are too young to vote.")
print()

# if-elif-else语句
age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
else:
    price = 40
print(f"Your admission cost is ${price}.")
print()

# 包含多个elif的语句
age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
elif age < 65:
    price = 40
else:
    price = 20
print(f"Your admission cost is ${price}.")
print()

# 在if-elif的最后不一定要有else，else是匹配所有，有时候如果最后的条件也想精确匹配，建议用elif，就不要else了
age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
elif age < 65:
    price = 40
elif age >= 65:
    price = 20
print(f"Your admission cost is ${price}.")
print()

# if-elif-else语句适用于只对某一个条件感兴趣的情况，有时候对所有条件都感兴趣，这时就要用一系列if语句，不加elif和else，if-elif-else语句从上到下匹配，一旦匹配中某一个条件，后面的就跳过了，一系列独立的if语句则每一个if都要执行
purchase_order = ['c9300', 'license', 'smartnet']
delivery_order = []
if 'c9300' in purchase_order:
    delivery_order.append('c9300')
if 'license' in purchase_order:
    delivery_order.append('license')
if 'smartnet' in purchase_order:
    delivery_order.append('smartnet')
if 'stack' in purchase_order:
    delivery_order.append('stack')
print("Delivery Order")
for item in delivery_order:
    print(item)
print()

# if语句和列表结合使用，比如在列表中查找一个特殊的item
requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']
for requested_topping in requested_toppings:
    if requested_topping == 'green peppers':
        print("Sorry, we are out of green peppers right now.")
    else:
        print(f"Adding {requested_topping}.")
print("\nFinished making your pizza!")
print()

# 检查一个列表是否是空列表
requested_toppings = []
if requested_toppings:
    for requested_topping in requested_toppings:
        print(f"Adding {requested_topping}.")
    print("\nFinished making your pizza!")
else:
    print("Are you sure you want a plain pizza?")
print()

# 使用多个列表
available_toppings = ['mushrooms', 'olives', 'green peppers', 'pepperoni', 'pineapple', 'extra cheese']
# available_toppings也可以是tuple，如果店家供应的toppings稳定的话
requested_toppings = ['mushrooms', 'french fries', 'extra cheese']
for requested_topping in requested_toppings:
    if requested_topping in available_toppings:
        print(f"Adding {requested_topping}.")
    else:
        print(f"Sorry, we don't have {requested_topping}.")
print("\nFinished making your pizza!")

# python代码规范：
# 写条件测试语句的时候，在比较符号两边留空格，比如: if age < 4:
