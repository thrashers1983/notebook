这篇笔记记录关于PATH环境变量

关于\$:  
定义变量的时候，变量名不加$，调用变量时要在变量名前加\$，这里PATH是变量名，当要调用PATH时，要写\$PATH

```bash
➜  ~ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
➜  ~ cat /etc/paths
/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin
```
可以看到，其实PATH环境变量的值来自于/etc/paths这个文件，可以编辑etc/paths来增加删除路径，也可以编辑~/.zshrc，加一句：export PATH=\$PATH:\$HOME/yiping/bin，这句话的意思是在PATH的后面加上/Users/yuhexu/yiping/bin，如果想加在PATH最前面，则这样写：export PATH=\$HOME/yiping/bin:\$PATH

如果没有把脚本所在路径加入PATH环境变量，则执行脚本时要加上路径，比如执行当前目录下的test.sh脚本，要敲./test.sh，如果不写./，系统会到系统路径（由PATH环境变量指定）下查找test.sh，而系统路径下显然不存在这个脚本，所以会执行失败

系统在PATH环境变量中搜索路径按先后顺序搜索，假设有2个同名的脚本都叫test.sh，分别在/usr/local/bin下和/usr/bin下，如果只就敲test.sh，由于/usr/local/bin在前面，会搜索并执行/usr/local/bin下的test.sh，/usr/bin下的test.sh不会被搜索到
