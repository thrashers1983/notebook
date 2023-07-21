批量注释代码：  
选中想要注释的代码块，按command-/，再按一次command-/取消注释

代码规范一行80字符或120字符
```json
设置80字符和120字符提示竖线：
"editor.rulers": [80,120]

竖线颜色设置：
"workbench.colorCustomizations": {
    "editorRuler.foreground": "#ff4081"
}
```

如果新建一个文件的文件名不带后缀，vscode就无法识别是什么语言，就没有语法高亮，但是在第一次保存文件时，vscode会根据第一行的#!行识别到脚本语言（比如#!/bin/zsh）

这章写了一个shell脚本：~/yiping/bin/ekill，要让这个脚本能执行，需要给他添加x权限：chmod +x ekill

在新的tab中打开文件
```json
"workbench.editor.enablePreview":false
```

打开文件小技巧：如果文件藏得比较深，一时找不到在哪个目录下，可以command-p输入文件名的一部分来搜索，比如想找PATH_environment_variable.md，输入PATHen或pev都可以搜到该文件
