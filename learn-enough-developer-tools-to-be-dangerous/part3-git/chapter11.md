知识点1:  
假设现在对main分支的工作区做了修改，这些修改在main分支并没有提交，此时创建并切换到新的分支dev，这些在main分支未提交的修改会被带到dev分支，然后在dev分支提交这些修改，再切回到main分支，main分支显示是clean的，刚做的那些修改都消失了

知识点2:  
如果之前已经git clone了一个远程库到本地(一开始只有main分支)，在下次git pull的时候，如果远程库上有新的dev分支，则会把dev分支也pull下来，但是这时候用git branch是看不到dev分支的(要用git branch -a)，必须要先git switch dev，在敲git switch dev的同时，git把本地的dev分支和origin下的dev分支绑定了，下次在dev分支下只需要敲git push就行

知识点3:  
github pages可以提供静态网页的服务，有需要的时候再研究

知识点4:
git可以配置alias，举例如下:  
git config --global alias.co checkout  
// 设置checkout的别名co，切换分支就可以敲git co main

作者推荐的学习资料:
- Pro Git by Scott Chacon and Ben Straub (https://git-scm.com/book/en/v2)
- Learn Git at Codecademy (https://www.codecademy.com/learn/learn-git)
- Git tutorials (https://www.atlassian.com/git/tutorials) by Atlassian (makers of Bitbucket)
- Tower Git tutorials (https://www.git-tower.com/learn/)
