# 定义一个简单的函数，用来打印问候语
def greet_user():   
    """Display a simple greeting."""
    print("Hello!")
# 函数定义语法: 
# 第一行: 使用关键字def定义一个函数，本例中greet_user()是函数名，()中可以传递参数
# 第二行: 缩进一个level，写文档字符串(docstring)，描述这个函数是用来干嘛的，python在生成函数的文档的时候，会读取文档字符串，文档字符串通常使用三引号，这样可以写多行

greet_user()    # 调用函数

# 给函数传参
def greet_user(username):
    """Display a simple greeting."""
    print(f"Hello, {username.title()}!")

greet_user('michael')

# 名词解释: Arguments和Parameters
# 以上面这个函数为例: 定义函数时的username是parameter，调用函数时的michael是argument，username是一个变量，michael是一个值，调用函数的时候，把一个值赋给一个变量

# 一个函数可以有多个参数，调用函数的时候有几种传参的方法
# 1. Positional Arguments: 调用函数时argument的顺序要和定义函数时parameter的顺序一致
def describe_pet(animal_type, pet_name):
    """Display information about a pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet('dog', 'pipi')

# 2. Keyword Arguments: 调用函数时argument写清楚参数名=值，argument的顺序无所谓
describe_pet(animal_type='cat', pet_name='mimi')
describe_pet(pet_name='mimi', animal_type='cat')

# 在定义一个函数的时候，可以选择为每个参数设定一个默认值，那些有默认值的参数要写在最后
def describe_pet(pet_name, animal_type='dog'):
    """Display information about a pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet('pipi')
describe_pet(pet_name='pipi')
describe_pet('mimi', 'cat')
describe_pet(animal_type='cat', pet_name='mimi')
print()

# 函数返回值
def get_formatted_name(first_name, last_name):
    """Return a full name, neatly formatted."""
    full_name = f"{first_name} {last_name}"
    return full_name.title()

musician = get_formatted_name('jimi', 'hendrix')
print(musician)
print()

# 可选参数写在最后，给一个空字符串作为其默认值，也可以用None作为其默认值
def get_formatted_name(first_name, last_name, middle_name=''):
    """Return a full name, neatly formatted."""
    if middle_name:     # 非空字符串返回True，空字符串返回False
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"
    return full_name.title()

musician = get_formatted_name('jimi', 'hendrix')
print(musician)
musician = get_formatted_name('john', 'hooker', 'lee')
print(musician)
print()

# 返回一个字典
def build_person(first_name, last_name):
    """Return a dictionary of information about a person."""
    person = {'first': first_name, 'last': last_name}
    return person

musician = build_person('jimi', 'hendrix')
print(musician)
print()

# 给上面这个函数加一个可选参数
def build_person(first_name, last_name, age=None):
    """Return a dictionary of information about a person."""
    person = {'first': first_name, 'last': last_name}
    if age:
        person['age'] = age
    return person

musician = build_person('jimi', 'hendrix', age=27)
print(musician)
print()

# 在while loop里调用函数
while True:
    print("\nPlease tell me your name:")
    print("(enter 'q' at any time to quit)")
    f_name = input("First name: ")
    if f_name == 'q':
        break
    l_name = input("Last name: ")
    if l_name == 'q':
        break
    formatted_name = get_formatted_name(f_name, l_name)
    print(f"\nHello, {formatted_name}!")
print()

# 把列表当作参数传给一个函数
def greet_users(names):
    """Print a simple greeting to each user in the list."""
    for name in names:
        msg = f"Hello, {name.title()}!"
        print(msg)

usernames = ['michael', 'tracy', 'kobe']
greet_users(usernames)
print()

# 在函数中修改列表
# 这个例子是模拟3D打印
def print_models(unprinted_designs, completed_models):
    """
    Simulate printing each design, until none are left.
    Move each design to completed_models after printing.
    """
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        print(f"Printing model: {current_design}")
        completed_models.append(current_design)

def show_completed_models(completed_models):
    """Show all the models that were printed."""
    print("\nThe following models have been printed:")
    for completed_model in completed_models:
        print(completed_model)

unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []
print_models(unprinted_designs, completed_models)
show_completed_models(completed_models)
# 如果想保留原始的unprinted_designs列表，则可以像下面这样写:
# print_models(unprinted_designs[:], completed_models)
# 这等于是把原列表做一个拷贝传给了函数，原列表不受影响
print()

# 传递任意数量的参数
# 在参数名前加*号，创建一个空的tuple叫toppings，把接受到的所有参数按位置顺序放进这个tuple
def make_pizza(*toppings):
    """Print the list of toppings that have been requested."""
    print(toppings)

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')

def make_pizza(*toppings):
    """Summarize the pizza we are about to make."""
    print("\nMaking a pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')
print()

# 如果函数定义中有明确的参数和带*的参数，带*的参数放在最后
def make_pizza(size, *toppings):
    """Summarize the pizza we are about to make."""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
print()

# 传递任意数量的键值对参数
# 在参数名前加**，创建一个空字典叫user_info，把接收到的所有命名参数按键值对放进这个字典
def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('albert', 'einstein', location='princeton', field='physics')
print(user_profile)

# 这章后面有讲到什么是模块和怎么导入模块，我记录到了这两个文件: chapter8_main_program.py和chapter8_modules.py
