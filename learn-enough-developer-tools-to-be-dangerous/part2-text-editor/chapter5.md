Vim has two principal modes, known as normal mode and insertion mode. Normal mode is for doing things like moving around the file, deleting content, or finding and replacing text, whereas insertion mode is for inserting text.

vim .zshrc  
// 如果文件已存在，则打开文件，如果文件不存在，则创建新文件

vim在普通模式下的命令：  
i: 进入插入模式，在当前光标位置开始插入  
0: 光标移到行首  
$: 光标移到行尾  
:q回车: 退出vim(仅当文件没有被更改)  
:q!回车: 强制退出不保存  
:w回车: 保存更改  
:wq回车: 保存退出  
u: 撤销之前所做的更改  
x: 删除光标所在位置的单个字符  
dd: 删除整行  
p: 用dd删除的行，用yy复制的行，可以用p在光标的下一行粘贴。用v选中文本后进行d(删除)或y(复制)的操作，可以用p在光标的下一个位置粘贴。  
^f: 向下翻页  
^b: 向上翻页  
G: 移动到最后一行  
gg: 移动到第一行  
17G: 移动到第17行  
17gg: 移动到第17行  
:set nu: 显示行号  
:set nu!: 取消显示行号  
/string: 全文搜索字符串，n向下匹配，N向上匹配

vim在插入模式下的命令：  
ESC: 退出插入模式回到普通模式  

[在线vim互动教学](https://www.openvim.com/)

.zshrc文件的内容更改后，要source .zshrc才能生效，source的作用是执行参数文件内的脚本  
打开一个新的terminal窗口，会自动source .zshrc，因此只有当希望在当前terminal中让.zshrc的变更生效才需要手动source
