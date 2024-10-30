# 引入一个模块，在这个模块中所定义的所有函数都能在这里使用
import chapter8_modules

chapter8_modules.make_pizza(16, 'pepperoni')
chapter8_modules.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

# 从模块中单独引入某个函数或某几个函数，如果引入多个函数，函数名用逗号隔开
from chapter8_modules import make_pizza

make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

# 如果引入的函数名和本程序中已有的函数名有冲突，或者函数名很长，可以给函数起别名
from chapter8_modules import make_pizza as mp

mp(16, 'pepperoni')
mp(12, 'mushrooms', 'green peppers', 'extra cheese')

# 也可以给模块起别名
import chapter8_modules as c8m

c8m.make_pizza(16, 'pepperoni')
c8m.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

# 从模块中引入所有函数，这个写法不推荐: 尤其当你并不了解这个模块里有哪些函数，有可能模块中的函数名和本程序中的函数名有冲突
from chapter8_modules import *

make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

# 最推荐的是引入一个模块(可以考虑给模块起别名)，然后用模块名(别名).函数名来调用，或者如果只需要用到某一个或几个函数，就只引入那些函数，如果函数名有冲突，可以给函数起别名

# 关于模块和函数的best practice
# 1. 模块名和函数名都要起有意义的名字(用小写字母和下划线组合)
# 2. 每个函数都应该用docstring格式写一下注释，描述这个函数的功能
# 3. 在定义函数给参数默认值的时候，和调用函数要传参数的时候，等号两边不要有空格
# 4. 定义函数的时候，如果有很多参数要写会超过一行79个字符，则用如下这种格式:
# def function_name(
#         parameter_0, parameter_1, parameter_2,
#         parameter_3, parameter_4, parameter_5):
#     function body...
# 5. 如果一个模块里有多个函数，每个函数之间空两行
# 6. import写在程序的最开始位置，除非第一行写了本程序的注释
