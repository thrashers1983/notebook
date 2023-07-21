重定向：  
echo "are you kidding me" > xixi  
// 把输出重定向到一个文件中，如果xixi不存在则创建xixi，如果xixi已经存在则原来的内容被覆盖  
cat xixi  
are you kidding me

append:  
echo "are you shitting me" >> xixi  
cat xixi  
are you kidding me  
are you shitting me  
// echo默认在字符串末尾加上换行符

cat也可以和>或者>>结合使用：  
cat file1 > file2  
cat file1 >> file2  
cat file1 file2 > file3

diff:  
diff file1 file2

touch:  
touch foo  
// 创建一个空文件foo，如果foo已经存在则刷新最后修改时间(文件内容不受影响)

ls:  
ls *.txt  
ls -r   
// 反向排序  
ls -t   
// 按最后修改时间排序  
ls -rtl  
// 按最后修改时间反向排序，以长模式显示  
ls -a  
// 显示隐藏文件/文件夹

echo \$SHELL  
// 打印$SHELL环境变量  
chsh -s /bin/bash  

mv:  
mv foo bar  
// 如果源文件夹和目标文件夹相同，则mv仅仅是重命名

cp:  
cp foo bar

rm:  
默认情况下rm是不会提示的，很多系统下rm会提示是因为默认做了alias：rm='rm -i'，敲rm -f相当于敲了rm -i -f，这样-f会覆盖-i(-f强制删除，且无视文件是否存在)，而zsh默认没有做rm的alias  
