用户家目录也可以用～表示：  
/Users/yuhexu/Downloads == ~/Downloads  
cd, cd ~切换到家目录  
cd -切换到上一个目录

普通用户不能修改系统文件或系统目录，要用sudo(substitute user do)提权：  
touch /opt/foo  
touch: /opt/foo: Permission denied  
// 提示没有权限  
sudo touch /opt/foo  
Password:  
ls -l /opt/foo  
-rw-r--r--  1 root  wheel  0 May 18 13:35 /opt/foo  
// sudo，输入当前用户的密码，成功提权操作(前提是当前用户被配置了有sudo的特权)，可以看到文件的owner是root  
sudo rm -f /opt/foo  
// rm也要sudo才能执行

mkdir:  
mkdir text_files  
mv *.txt text_files/   
// 创建一个目录，把后缀为txt的文件移动到新目录下  
ls text_files/  
// 默认是显示目录下的内容  
ls -ld text_files/  
// -d显示目录本身  
mkdir foo/bar  
mkdir: foo: No such file or directory  
mkdir -p foo/bar  
// -p创建中间的目录，这一条命令创建了foo和bar两个目录

.作为当前目录的常见用途：  
1. 拷贝或移动文件到当前目录：  
cp ../sonnets.txt .  
2. 结合find一起使用：  
find . -name '*.txt'   
// 在当前目录和其子目录下查找文件名匹配\*.txt的文件  
3. 用Finder打开当前目录：  
open .  
// open命令用默认的应用程序打开文件或者目录，对于目录，默认应用程序是Finder

组合命令：  
./configure ; make ; make install  
// 分号连接几个命令按顺序执行  
./configure && make && make install  
// &&也是按顺序执行，区别是&&仅当上一条命令执行成功，下一条命令才会执行，分号连接的所有命令不管发生什么都会执行  

mv foo/ bar/  
// 如果bar目录已经存在，则把foo目录移动到bar目录下，如果bar目录不存在，则是把foo改名为bar，目录后面的/是tab自动补上的，有没有/没有区别

cp foo bar  
cp: foo is a directory (not copied).  
cp -r foo bar  
// 如果要复制一个目录到其他路径，必须加-r(recursive)，注意foo后面不能加/，如果加了/，cp -r foo/ bar就只是把foo目录下的内容拷贝过去，而foo目录本身不会拷贝过去。如果只是想复制目录下的内容，建议这样写：cp foo/* bar，如果foo目录下还有子目录，加-r：cp -r foo/* bar

rmdir foo  
rmdir: foo: Directory not empty  
rm -rf foo  
// rmdir要求目录是空的才能删除，所以这个命令基本没啥用，一般用rm -rf删除目录下的内容和目录本身

grep sesquipedalian foo  
grep: foo: Is a directory  
grep -r sesquipedalian foo  
foo/bar/long_word.txt:sesquipedalian  
// 默认grep不能在目录中匹配字符串，加-r可以让grep在目录和其子目录中的所有文件中匹配字符串
