创建python虚拟环境的前提条件是系统已经安装了python  
以我的macbook为例，系统安装了python3.9和3.11
![](images/Screenshot%202023-08-05%20at%2011.16.41.png)
可以看到python3指向了python3.11，以及python安装目录: /Library/Frameworks/Python.framework/Versions/  
3.11和3.9两个目录分别包含了两个版本各自的python解释器，pip工具，标准库和第三方库等等

用python3标准模块venv创建虚拟环境: 
```
python3 -m venv 目录名  
```
所谓创建虚拟环境其实就是创建一个目录，把python环境复制一份到该目录下，以我的macbook为例: 
![](image/../images/Screenshot%202023-08-05%20at%2012.05.46.png)
python_venv作为一个总目录用来存放所有的虚拟环境，进到python_venv敲python3 -m venv 3.11创建目录名为3.11的虚拟环境目录(这个虚拟环境是3.11版本，因为python3指向了python3.11，如果想创建3.9版本的虚拟环境，要敲python3.9 -m venv 目录名)，进到3.11可以看到最主要的两个目录: bin和lib  

bin存放python解释器，pip工具，activate脚本
![](images/Screenshot%202023-08-05%20at%2012.12.01.png)

lib下的site-packages存放第三方库(虚拟环境是没有自己的标准库的，直接用真实环境的标准库)
![](images/Screenshot%202023-08-05%20at%2012.17.55.png)

重点来了！  
虚拟环境(提示符开头显示3.11)
![](images/Screenshot%202023-08-05%20at%2012.34.40.png)
真实环境
![](images/Screenshot%202023-08-05%20at%2022.20.02.png)
可以看到sys.path唯一的区别是最后一行，在虚拟环境中是用该虚拟环境自己的第三方库(标准库还是用真实环境的标准库)

再看:  
虚拟环境
![](images/Screenshot%202023-08-05%20at%2022.24.30.png)
真实环境
![](images/Screenshot%202023-08-05%20at%2022.26.24.png)
可以看到在激活了虚拟环境后，$PATH环境变量的最开头插入了该虚拟环境的bin目录，所以在激活了虚拟环境后运行python和pip都是运行的虚拟环境中的python和pip(python解释器还是链接到真实环境的相应版本，pip安装的第三方库都会安装到虚拟环境的site-packages目录中)，虚拟环境就是通过这种方式来实现环境的隔离

保存和复制虚拟环境:  
```
pip freeze > requirements       把第三方库列表导出到一个文件
pip install -r requirements     通过requiements文件安装第三方库
```

在vscode中使用虚拟环境  
1. 打开Settings，搜索venv，在Venv Path这里输入虚拟环境的路径，vscode会自动识别该路径下所有的虚拟环境
![](images/Screenshot%202023-08-06%20at%2013.42.25.png)

2. 打开一个py文件，点击状态栏右下角的python解释器
![](images/Screenshot%202023-08-06%20at%2014.01.59.png)
弹出选择解释器
![](images/Screenshot%202023-08-06%20at%2014.05.46.png)
