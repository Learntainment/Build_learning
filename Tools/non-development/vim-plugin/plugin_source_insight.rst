======================
this document is about build vim plugin as source insight
======================

此文档将会提示你如何通过简单的操作完成source insight功能

包含的插件有：

 | "nerdtree"
 | "SrcExpl"
 | "taglist.vim"
 | "vim-pathogen"
 | "vim-colors-solarized"

step1
=======

 | git clone this repository

step2
=====

 | cp repository/.vimrc ~/.vim/.
 | cp repository/vim_plugin_deploy.sh ~/.vim/.

step3
====

 run deploy bash

 | bash vim_plugin_deploy.sh

step4
=====

 | restart your linux

Tips
====

 | <F7> show ctags tag list context
 | <F8> call tag list
 | <F9> call the SrcExpl as the source insight function
 | <space> back to last function

本文版权归个人所有，如需转载，请注明出处
======================================
