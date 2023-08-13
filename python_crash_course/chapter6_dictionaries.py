# A dictionary in Python is a collection of key-value pairs. Each key is connected to a value, and you can use a key to access the value associated with that key. A key’s value can be a number, a string, a list, or even another dictionary. In fact, you can use any object that you can create in Python as a value in a dictionary.

# 一个简单的字典
choubao = {'height': 166, 'weight': 55, 'face_score': 8}
print(choubao['height'])
print(choubao['weight'])
print(choubao['face_score'])
print(f"Choubao is {choubao['height']}cm, {choubao['weight']}kg, and her face score is {choubao['face_score']} out of 10.")
print()

# 在字典中加入新的键值对
choubao['breast'] = 'busty'
choubao['butt'] = 'booty'
print(choubao)
print()

# 从空字典开始构造字典
jpmc_offer = {}
jpmc_offer['title'] = 'network engineer'
jpmc_offer['salary'] = '38K'
jpmc_offer['contract'] = 'outsourcing'
print(jpmc_offer)
print()

# 修改键值
jpmc_offer['contract'] = 'full-time employee'
print(jpmc_offer)
print()

# 一个有趣的例子
pipi = {'breed': 'springer spaniel', 'sex': 'male', 'speed': 'fast', 'position': 0}
print(f"Original position: {pipi['position']}")

if pipi['speed'] == 'low':
    position_increment = 1
elif pipi['speed'] == 'medium':
    position_increment = 2
elif pipi['speed'] == 'fast':
    position_increment = 3

pipi['position'] = pipi['position'] + position_increment
# 因为position_increment这个变量没有事先定义，所以if-elif语句必须有一条要匹配，否则会导致position_increment无法被赋值，程序会报错，当然也可以在if-elif最后加一个else匹配其余所有来给position_increment赋值
print(f"New position: {pipi['position']}")
print()

# 删除键值对
print(pipi)
del pipi['position']
print(pipi)
print()

# 字典可以是同一个对象的各种属性信息，也可以是各个对象的同一类型的信息
favorite_languages = {
    'yiping': 'python',
    'shawn': 'javascript',
    'ivan': 'ruby',
    'ben': 'python',
    }
# 这是写字典的另一种格式，每一行写一个键值对，并且每行都缩进一个level，结束大括号也缩进一个level，最好在最后一个键值对后面加一个逗号
print(f"Yiping's favorite language is {favorite_languages['yiping'].title()}.")
print()

# 字典还可以用get()方法访问一个键，如果这个键存在，则正常返回该键对应的值，如果这个键不存在，则可以返回一个默认值，用get()的好处是如果访问了一个不存在的键，程序不会报错
# get()的第一个参数是想要访问的键，第二个参数是想要返回的默认值(可选参数)，如果不写就返回None
favorite_language = favorite_languages.get('joseph', 'nonexistent')
print(favorite_language)
favorite_language = favorite_languages.get('joseph')
print(favorite_language)
print()

# loop键值对
for name, language in favorite_languages.items():
    print(f"{name.title()}'s favorite language is {language.title()}.")
# items()方法返回一个键值对的列表，然后for循环把键和值分别赋给name和language这两个变量
print(favorite_languages.items())
print()

# loop键
for name in favorite_languages.keys():
    print(name.title())
# keys()方法返回一个键的列表
print(favorite_languages.keys())
print()

# 实际上loop键是loop一个字典的默认行为，所以可以省掉不写keys()
for name in favorite_languages:
    print(name.title())
print()

# 仅loop键，然后通过键访问对应的值
for name in favorite_languages.keys():
    language = favorite_languages[name]
    print(f"Hi {name.title()}, I see you love {language.title()}!")
print()

# 判断字典中是否存在某个键
if 'joseph' not in favorite_languages.keys():   # keys()可以省略
    print("Joseph, please take our poll!")
print()

# 按特定顺序loop键
for name in sorted(favorite_languages.keys()):  # keys()可以省略
    print(f"{name.title()}, thank you for taking the poll.")
print()

# loop值
print("The following languages have been mentioned:")
for language in favorite_languages.values():
    print(language.title())
# values()方法返回一个值的列表，注意python出现了2次(列表可以有重复的元素)
print(favorite_languages.values())
print()

# 去除重复的元素
print("The following languages have been mentioned:")
for language in set(favorite_languages.values()):
    print(language.title())
# set()方法创建一个无序的不重复的元素集
print(set(favorite_languages.values()))
print()

# 可以用{}直接创建一个set
languages = {'python', 'ruby', 'python', 'javascript'}
print(languages)
# set和dictionary都用大括号包裹，注意区分: dictionary包含的是键值对，set包含的是单个元素
print()

# 列表里面嵌套字典
switch_1 = {'model': '9500', 'port': 24}
switch_2 = {'model': '9300', 'port': 48}
switch_3 = {'model': '9200', 'port': 48}
switches = [switch_1, switch_2, switch_3]
for switch in switches:
    print(switch)
print()

# 自动生成字典
switches = []

for switch_number in range(10):
    new_switch = {'model': '9200', 'port': 48}
    switches.append(new_switch)

for switch in switches[:5]:
    print(switch)
print("...")

print(f"\nTotal number of switches: {len(switches)}")
print()

# 修改前三个switch的属性
for switch in switches[:3]:
    if switch['model'] == '9200':
        switch['model'] = '9300'
        switch['port'] = 24
        
for switch in switches[:5]:
    print(switch)
print("...")
print()

# 字典里面嵌套列表
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'],
    }

print(f"You ordered a {pizza['crust']}-crust pizza "
      "with the following toppings:")       
# print换行的语法: 第一行结尾加一个引号，第二行缩进一个level，开头加一个引号
for topping in pizza['toppings']:
    print(f"\t{topping}")
print()

# 字典里面嵌套列表例子2
favorite_languages = {
    'yiping': ['python', 'javascript'],
    'shawn': ['javascript'],
    'ivan': ['ruby', 'java'],
    'ben': ['python', 'go'],
    }

for name, languages in favorite_languages.items():
    if len(languages) == 1:
        print(f"\n{name.title()}'s favorite language is: {languages[0].title()}")
    else:
        print(f"\n{name.title()}'s favorite languages are:")
        for language in languages:
            print(f"\t{language.title()}")
print()

# 字典嵌套字典
users = {
    'ypfeng': {
        'first': 'yiping',
        'last': 'feng',
        'location': 'shanghai',
        },
    'sjwang': {
        'first': 'sijie',
        'last': 'wang',
        'location': 'suzhou',
        },
    }
    
for username, user_info in users.items():
    print(f"\nUsername: {username}")
    full_name = f"{user_info['first']} {user_info['last']}"
    location = user_info['location']
    print(f"\tFull name: {full_name.title()}")
    print(f"\tLocation: {location.title()}")
