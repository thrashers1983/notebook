把本地repo同步到github的步骤：  
1. 在github上创建一个repo，假设名字叫website
2. git remote add origin https://github.com/thrashers1983/website.git  
// origin可以理解成website.git这个远程repo的别名(也可以自定义任何的名字)，如果本地有多个项目(多个本地repo)，每个项目对应一个远程repo，那每一个远程repo都可以用origin作为别名，不冲突。如果本地一个项目关联多个远程repo，那每个远程repo要取不同的别名。用https方式连接远程repo需要提前生成一个presonal access token
3. git push -u origin main  
// git push origin main在origin下也创建一个main分支并且把本地main分支推送到远程main分支，-u参数把本地main分支和远程main分支绑定，以后在本地main分支下只要敲git push即可

注：建议每个repo都应该创建一个README文件，推荐README.md

参考文章：  
[Git 里面的 origin 到底代表啥意思?](https://www.zhihu.com/question/27712995/answer/2336292635)  
[git push 的 -u 参数具体适合含义？](https://www.zhihu.com/question/20019419/answer/48434769)  
[Same remote repo name for multiple remote repos](https://stackoverflow.com/questions/70957117/same-remote-repo-name-for-multiple-remote-repos)
