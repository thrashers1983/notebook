Git uses a special hidden directory called .git to track changes

brew install git  
brew upgrade git  
git --version  
git help  
git help | less  
git help add  
git init  
// 初始化一个文件夹，把它变成一个git仓库   
git status  
// 显示工作目录的状态  
git add index.html  
// 添加单个文件到暂存区  
git add -A  == git add .  
// 添加当前目录下所有文件到暂存区   
git commit -m "message"  
// -m后面跟一段对这次commit的说明性文字  
// 为什么要先git add再git commit：因为git的commit操作不能选择要提交哪些修改，所以设计了一个暂存区的概念，把需要提交的修改先添加到暂存区，再commit把暂存区所有的修改一次性提交(原子性操作，要么全部成功，要么全部失败)  
git log    
// 查看commit的历史记录，每次commit都会生成一个散列值来唯一标识这次commit  
git diff  
// 查看上一次commit和unstaged changes之间的区别  
git diff --staged  
// 查看上一次commit和staged changes之间的区别  
git commit -a  
// 文件被修改或删除后，要先stage(git add)才能commit，加了-a可以省掉一步git add，但是只对已经添加到repo中的文件有效，对新添加的文件无效，新的文件在git add之前是untracked状态，一定要执行git add才算添加到repo    
git commit --amend  
// 修改上一次的commit  
使用场景1: 上次commit的message写错了，可以git commit --amend来修改上次commit的message(commit的哈希值被刷新)  
使用场景2: 在上次commit之后又改了一些代码，但是不想再commit一次，可以git commit --amend，这个commit会把上次的commit覆盖掉(不会产生新的commit记录，但是刷新哈希值)  
git show 散列值  
// 查看某次commit的详细信息  
git log -p  
// 显示所有commit的详细信息


git config --global user.name "Your Name"  
git config --global user.email your.email@example.com  
git config --global init.defaultBranch main  
// --global参数表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址  
git config --list  
// 查看全局配置  
~/.gitconfig这个文件存放git的全局配置

The main Git status sequence for changing a file.
![](../../images/08fig01.jpg)  
