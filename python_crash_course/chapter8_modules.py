# 把函数单独写在一个后缀是.py的文件中，这个py文件就是module，可以被主程序import
def make_pizza(size, *toppings):
    """Summarize the pizza we are about to make."""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")
