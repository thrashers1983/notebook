### 本文档说明：本文档仅补充在learn-enough-git中没有涉及的内容

git log --pretty=oneline  
git log --graph --pretty=oneline --abbrev-commit  

在Git中，用HEAD表示当前版本，上一个版本就是HEAD^，上上一个版本就是HEAD^^，上100个版本写成HEAD~100  
git reset --hard HEAD^  
git reset --hard a4e5f  
git reflog  
git diff HEAD index.html  
// 查看指定文件的diff，默认就是和HEAD比较  
git restore index.html  
// 撤销工作区的修改，回到上次git commit或git add的状态  
git restore --staged index.html  
// 撤销暂存区的修改，把修改放回工作区(git reset HEAD index.html也能起到相同的效果，后面会对git reset详述)  

git reset不加--hard详解：  
1. 在当前版本A的工作区和暂存区都clean的情况下如果reset到之前的版本B，会把版本A和版本B做比较，把变更的部分放到工作区
2. 在当前版本A的工作区有修改的情况下reset到之前的版本B，会把当前版本A和工作区的修改加到一起和版本B做比较，把变更的部分放到工作区
3. 在当前版本A的暂存区有修改的情况下reset到之前的版本B，会先把暂存区的修改放回工作区，然后把版本A和工作区的修改加到一起和版本B做比较，把变更的部分放到工作区

git remote -v  
// 查看远程库信息  
git remote rm origin  
// 解除本地库和远程库的绑定关系，并不是删除远程库，删除远程库只能去github上操作

git clone https://github.com/thrashers1983/website.git  
// 本地会自动创建和远程库同名的文件夹

```
配置git使用shadowsocks代理
git config --global http.proxy 'socks5://127.0.0.1:7890'
git config --global https.proxy 'socks5://127.0.0.1:7890'

取消代理设置
git config --global --unset http.proxy
git config --global --unset https.proxy

注1: 7890是ClashX的端口，其他客户端可能端口不一样
注2: git clone和git push只需要配置https代理即可
```

关于分支看这几篇文章就够了:   
[廖雪峰——创建与合并分支](https://www.liaoxuefeng.com/wiki/896043488029600/900003767775424)  
[廖雪峰——解决冲突](https://www.liaoxuefeng.com/wiki/896043488029600/900004111093344)  
[廖雪峰——分支管理策略](https://www.liaoxuefeng.com/wiki/896043488029600/900005860592480)

git branch dev  
// 创建分支  
git branch  
// 查看所有分支，带*号的是当前分支  
git checkout dev或者git switch dev  
// 切换分支(推荐使用git switch)  
git checkout -b dev或者git switch -c dev  
// 创建并切换分支  
git merge dev  
// 合并目标分支到当前分支  
git branch -d dev  
// 删除分支  
git merge --no-ff -m "message" dev  
// 禁用fast forward模式合并分支

合并分支时，如果main分支没有改动，Git默认使用Fast forward模式，也就是直接把main指针指向dev的最新提交来完成合并，这种模式有一个缺点，就是在删除分支后，git log记录里就看不到曾经有过分支提交。如果禁用Fast forward模式，Git就会在merge时生成一个新的commit，这样git log就可以看到曾经有过分支提交  

git pull和git clone的使用方法:  
- 有权限的仓库，本地无代码  
git pull  
git clone  
- 有权限的仓库，本地有代码  
git pull
- 无权限的仓库，本地无代码  
git clone
- 无权限的仓库，本地有代码  
删了重新git clone

[git pull和git clone的区别参考这篇文章](https://blog.csdn.net/qq_36667170/article/details/121264178)
