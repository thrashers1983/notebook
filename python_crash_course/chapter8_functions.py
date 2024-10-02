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
