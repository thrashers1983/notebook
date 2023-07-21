Technically, Git tracks only files, not directories; in fact, it won’t track empty directories at all, so if you want to track an otherwise empty directory you need to put a file in it. One common convention is to use a hidden file called .gitkeep; to create this file in an empty directory called foo, you could use the command touch foo/.gitkeep. Then git add -A would add the foo directory as desired.

repo中如果有不想被git管理的文件，可以用.gitignore来忽略这些文件，操作如下：    
在repo的根目录下touch .gitignore，打开编辑器，输入想要忽略的文件名，比如:    
.DS_Store    
// 忽略具体某个文件  
*~  
// 忽略任何文件名以~符号结尾的文件  
tmp/  
// 忽略tmp目录下的所有文件  

.gitignore文件只会忽略那些没有被track的文件，因此推荐在新创建一个项目时就创建.gitignore文件

要想让.gitignore忽略已经被track的文件，必须把已经被track的文件untrack:  
- 如果是已经git add还没有git commit的文件，可以用git restore --staged或者git rm --cached
- 如果是已经git commit的文件，只能用git rm --cached，如果整个目录下文件都不要了，用git rm -r --cached来递归删除

git diff main  
// 查看main分支和当前分支的区别  
git branch -D dev  
// 删除没有合并的分支
