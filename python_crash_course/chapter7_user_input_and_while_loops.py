# 用input()方法获取用户输入
name = input("Please enter your name: ")    # input()的参数是提示信息
print(f"\nHello, {name}!")
print()

# 如果提示信息很长，可以先把提示信息赋给一个变量，再把这个变量传给input()方法
prompt = "If you tell us who you are, we can personalize the messages you see."
prompt += "\nWhat is your first name? "
name = input(prompt)
print(f"\nHello, {name}!")
print()

# input()方法把获取的用户输入识别为字符串，如果用户输入数字，需要用int()方法将其转成数字格式
age = input("How old are you? ")
age = int(age)      # 不写这句话后面的程序会报错，因为字符串不能和数字比较大小

if age >= 18:
    print('Please enter.')
else:
    print('You are not allowed to enter gambling house.')
print()

# 取模运算(两数相除取余数)
print(4 % 3)
print(5 % 3)
print(6 % 3)
print(7 % 3)
print()

# 判断一个数是奇数还是偶数
number = input("Enter a number, and I'll tell you if it's even or odd: ")
number = int(number)

if number % 2 == 0:
    print(f"\nThe number {number} is even.")
else:
    print(f"\nThe number {number} is odd.")
print()

# while loop，只要while的条件返回True，循环就一直执行下去
current_number = 1
while current_number <= 5:
    print(current_number)
    current_number += 1
print()

# 让用户决定什么时候退出程序
prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "

message = ""
while message != 'quit':
    message = input(prompt)
    if message != 'quit':
        print(message)
print()

# 当有多种情况会导致循环结束，可以使用flag变量来决定循环执行或退出
prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "

active = True   # 定义一个flag变量，只要flag变量为True，则循环继续，直到某个事件发生导致flag变量变成False，则循环结束
while active:
    message = input(prompt)
    if message == 'quit':
        active = False
    else:
        print(message)
print()

# 使用break直接退出while循环(break可以用来退出任何循环，比如break也可以退出for循环)
prompt = "\nPlease enter the name of a city you have visited:"
prompt += "\n(Enter 'quit' when you are finished.) "

while True:
    city = input(prompt)
    if city == 'quit':
        break
    else:
        print(f"I'd love to go to {city.title()}!")
print()

# 使用continue跳过while循环后面的代码，回到循环的开头继续执行
current_number = 0

while current_number < 10:
    current_number += 1
    if current_number % 2 == 0:
        continue
    print(current_number)
print()

# 避免无限循环：如果不当心写了无限循环，按ctrl+c退出，或者直接退出terminal

# 列表和字典结合while loop一起使用
# 把item从一个列表移到另一个列表
unconfirmed_users = ['shenchao', 'wenyu', 'yuxiao']
confirmed_users = []

while unconfirmed_users:
    current_user = unconfirmed_users.pop()
    print(f"Verifying user: {current_user.title()}")
    confirmed_users.append(current_user)

print("\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:
    print(confirmed_user.title())
print()

# 从列表中删除某个特定值的所有实例
pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
print(pets)

while 'cat' in pets:
    pets.remove('cat')

print(pets)
print()

# 用while loop重复提示用户输入信息，并把用户输入存入字典
responses = {}

polling_active = True
while polling_active:
    name = input("\nWhat is your name? ")
    response = input("Which mountain would you like to climb someday? ")
    responses[name] = response
    repeat = input("Would you like to let another person respond? (yes/no) ")
    if repeat == 'no':
        polling_active = False

print("\n--- Poll Results ---")
for name, response in responses.items():
    print(f"{name.title()} would like to climb {response.title()}.")
