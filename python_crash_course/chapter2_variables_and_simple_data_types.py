# 变量命名规则
# 1. 变量名可以是字母，数字，下划线，可以以字母或下划线开头，但不能以数字开头
# 2. 变量名不能有空格
# 3. 不要使用python关键字
# 4. 建议使用全小写字母

# 字符串可以用单引号，也可以用双引号
new_message = 'this is main branch'
news_2020 = "kiphony has now become yiping's girlfriend."
print(new_message)
print(news_2020)
print()

# title(),upper(),lower()的使用
girlfriend_name = 'kiphony yu'
print(girlfriend_name.title())
girlfriend_name = 'Kiphony Yu'
print(girlfriend_name.upper())
print(girlfriend_name.lower())
print()

# f-strings
first_name = "yiping"
last_name = "feng"
full_name = f"{first_name} {last_name}"
print(full_name.title())
print(f"Hello, {full_name.title()}, how are you?")
greetings = f"Hello, {full_name.title()}, how are you?"
print(greetings)
print()

# \t,\n的使用
print("\tPython")
print("Languages:\nPython\nC\nJavaScript")
print("Languages:\n\tPython\n\tC\n\tJavaScript")
print()

# rstrip(),lstrip(),strip()的使用
favorite_language = ' python\n\t'
print(favorite_language)
print(favorite_language.rstrip())
print(favorite_language.lstrip())
print(favorite_language.strip())
print()

# removeprefix(),removesuffix()的使用
taobao_url = 'https://www.taobao.com'
print(taobao_url.removeprefix('https://'))
filename = 'python_notes.txt'
print(filename.removesuffix('.txt'))
print()

# 整数运算
addition = 2 + 3
subtraction = 3 - 2
multiplication = 2 * 3
division = 3 / 2
exponents = 3 ** 3
print(addition)
print(subtraction)
print(multiplication)
print(division)
print(exponents)
multiple_operations = 2 + 3*4
print(multiple_operations)
multiple_operations = (2+3) * 4
print(multiple_operations)
print()

# 浮点数运算(忽略后面多出来的小数位)
add = 0.2 + 0.1
sub = 0.2 - 0.1
mul = 3 * 0.1
div = 2 / 0.1
exp = 3.0 ** 2
print(add)
print(sub)
print(mul)
print(div)
print(exp)
print()

# 对于很大的数字，可以用下划线分隔(下划线加在哪里都可以)，这样容易阅读
universe_age = 14_000_000_000
print(universe_age)
pi = 3.14159_2654
print(pi)
print()

# 一行赋值多个变量
x, y, z = 1, 2, 3
print(x, y, z)
print()

# 如果一个变量的值永远不变，称为常量，常量名用全大写字母(这不是强制的，只是约定俗成的习惯)
MAX_CONNECTIONS = 5000
print(MAX_CONNECTIONS)
