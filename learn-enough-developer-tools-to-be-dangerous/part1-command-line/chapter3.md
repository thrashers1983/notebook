which:  
which curl  
// 显示可执行程序所在位置

curl:  
curl -OL https://cdn.learnenough.com/sonnets.txt  
// -O下载网页中的文件，-L支持URL重定向  
curl -I https://www.learnenough.com/  
// -I返回http response的header  
curl -h  
// 查看帮助

重复使用之前敲过的命令：  
- !curl按tab或者空格即可补全最后一个以curl开头的命令(如果在curl命令之后又敲了几个命令，这个方法就很有用，省得一直按上箭头)
- ^r，搜索curl，匹配最后一条以curl开头的命令，继续按^r可以继续向前搜索匹配的命令
- history | grep curl查找包含curl的命令，!17执行第17条命令

head, tail:  
head sonnets.txt  
// 默认显示文件的前十行  
tail sonnets.txt   
// 默认显示文件的最后十行  
head -n 20 sonnets.txt  
tail -n 20 sonnets.txt

wc:  
wc sonnets.txt  
2620   17670   95635 sonnets.txt  
// 2620行，17670个单词, 95635字节  
head sonnets.txt | wc  
10      46     294  

tail -f:  
tail -f常用来监控实时变化的log文件  
模拟创建一个实时变化的log文件：在一个terminal里ping learnenough.com > learnenough.log，再开一个terminal，tail -f learnenough.log

less:  
less sonnets.txt  
// 上下箭头：向上向下移动一行    
// 空格：向下翻页  
// ^b: 向上翻页  
// G: 移动到最后一行  
// g: 移动到第一行  
// 17G: 移动到第17行  
// /string：全文搜索字符串，n向下匹配，N向上匹配  
// q: 退出

grep(globally search a regular expression and print):  
grep rose sonnets.txt   
grep rose sonnets.txt | wc  
// grep匹配包含给定字符串的行并打印  
grep -i rose sonnets.txt  
// 默认grep是大小写敏感的，-i忽略大小写  
grep -n rose sonnets.txt  
// -n显示行号  
grep Rose sonnets.txt | grep -v rose  
// grep -v是反向匹配，匹配不包含给定字符串的行

一个正则表达式的简单例子：  
匹配一个单词以“ro”开头，后面跟任意多个小写字母(可以是0个)，以“s”结尾  
grep ' ro[a-z]*s ' sonnets.txt  
// *代表前面的字符出现0次或多次，前后加空格保证匹配到以ro开头，以s结尾的单词

top:  
// 按资源占用率排序显示进程

ps aux:    
// a: show processes for all users  
// u: display the process's user/owner  
// x: also show processes not attached to a terminal  
ps aux | grep spring  

kill:  
kill -15 26069  
// kill通过进程号来终止进程，默认信号就是15，15通知进程安全的退出，kill -9是强行终止进程，26069是进程的PID  
pkill -15 -f "ping 8.8.8.8"  
// pkill匹配进程名来终止进程，默认只匹配进程名，加-f可以匹配参数，比如有两个ping进程：ping 114.114.114.114和ping 8.8.8.8，如果不加-f，pkill -15 ping将会终止所有的ping进程，加-f可以只匹配ping 8.8.8.8，ping 114.114.114.114不受影响
