============================
plugin one for function list
============================

首先先将该文件夹下的vimrc文件copy到你的~/环境下，改名为 .vimrc 文件。

ctags and taglist
=================

这两个插件保证了在vim中可以显示函数列表，并且可以利用他们来实现调用函数的功能，具体安装如下

 | sudo apt-get install ctags
 | sudo apt-get install vim-scripts
 | vim-addons install taglist

=================================
plugin two for python code prompt
=================================

pydiction
=========

这个插件是用来对python的函数进行代码补全，具体安装如下

 | git clone https://github.com/rkulla/pydiction.git

将文件中的after/ftplugin/python_pydiction.vim 复制到~/.vim/after/ftplugin/中。
再将另外的两个文件complete-dict 和 pydiction.py复制到~/.vim/  就可以了，
再将.vimrc文件复制到~/.中去。打开任何一个文件就可以看到了实际的效果了。

本文版权归个人所有，如需转载，请注明出处
=======================================

