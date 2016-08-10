#! /bin/bash

mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
CONTEXT=$(ls)
LIST=($CONTEXT)
NUMBER=${#LIST[@]}
nerdtree_flag=0
SrcExpl_flag=0
taglist_flag=0
pathogen_flag=0
solarized_flag=0
i=0
sum=0
while((i<$NUMBER))
do
    if [ "${LIST[i]}" = "nerdtree" ]; then
        let sum++
        nerdtree_flag=1
    elif [ "${LIST[i]}" = "SrcExpl" ]; then
        let sum++
        SrcExpl_flag=1
    elif [ "${LIST[i]}" = "taglist.vim" ]; then
        let sum++
        taglist_flag=1
    elif [ "${LIST[i]}" = "vim-pathogen" ]; then
        let sum++
        pathogen_flag=1
    elif [ "${LIST[i]}" = "vim-colors-solarized" ]; then
        let sum++
        solarized_flag=1
    fi
    let i++
done
echo $sum
if [ $sum != 5 ]; then
    if [ $nerdtree_flag = 0 ]; then
        cd ~/.vim/bundle
        git clone https://github.com/scrooloose/nerdtree.git
    fi
    if [ $SrcExpl_flag = 0 ]; then
        cd ~/.vim/bundle
        git clone https://github.com/wesleyche/SrcExpl.git
    fi
    if [ $taglist_flag = 0 ]; then
        cd ~/.vim/bundle
        git clone https://github.com/vim-scripts/taglist.vim
    fi
    if [ $pathogen_flag = 0 ]; then
        cd ~/.vim/bundle
        git clone https://github.com/tpope/vim-pathogen.git
    fi
    if [ $solarized_flag = 0 ]; then
        cd ~/.vim/bundle
        git clone https://github.com/altercation/vim-colors-solarized.git
    fi
fi

mv ~/.vim/.vimrc ~/.vimrc
echo -e "\nexport TERM=xterm-256color" >> ~/.bashrc
echo "finished! should restart"
