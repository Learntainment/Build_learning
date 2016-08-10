" normal setting

set encoding=utf-8 fileencodings=ucs-bom,utf-8,cp936
set nocompatible

set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent
set number

"set mouse=a
" high light search
set hlsearch
set incsearch

" add the line for label
set cursorline
" ignore and smart case
set ignorecase smartcase
" forbiden regradation search
set nowrapscan
" stop the error bell
set noerrorbells
set novisualbell
" match bracket
set showmatch

set laststatus=3

set ruler
" Pathogen setting
runtime bundle/vim-pathogen/autoload/pathogen.vim
execute pathogen#infect()
syntax enable
syntax on
filetype plugin indent on

" Color scheme Solarized
let g:solarized_termcolors=256
let g:solarized_contrast="normal"
let g:solarized_visibility="normal"
"let g:solarized_termtrans=1
set background=dark
colorscheme solarized


highlight Comment ctermfg=green guifg=green
highlight perlSharpBang ctermfg=green guifg=green
highlight ShDeref ctermfg=red guifg=red
highlight NonText ctermfg=cyan guifg=cyan
highlight WhitespaceEOL ctermbg=red guibg=red
" high light setting
nnoremap <silent> <F5> :noh<CR>

" Nerd tree setting
let NERDChristmasTree=0
let NERDTreeWinSize=35
let NERDTreeChDirMode=2
let NERDTreeIgnore=['\~$', '\.pyc$', '\.swp$']
let NERDTreeShowBookmarks=1
let NERDTreeWinPos="left"
let g:NERDTreeDirArrowExpandable = '$'
let g:NERDTreeDirArrowCollapsible = '$'
" Automatically open a NERDTree if no files where specified
autocmd vimenter * if !argc() | NERDTree | endif
" Close vim if the only window left open is a NERDTree
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
" Open a NERDTree
nnoremap <silent> <F6> :NERDTreeToggle<CR>

" NERDTress File highlighting
function! NERDTreeHighlightFile(extension, fg, bg, guifg, guibg)
 exec 'autocmd filetype nerdtree highlight ' . a:extension .' ctermbg='. a:bg .' ctermfg='. a:fg .' guibg='. a:guibg .' guifg='. a:guifg
 exec 'autocmd filetype nerdtree syn match ' . a:extension .' #^\s\+.*'. a:extension .'$#'
endfunction

call NERDTreeHighlightFile('cc', 'green', 'none', 'green', '#151515')
call NERDTreeHighlightFile('ini', 'yellow', 'none', 'yellow', '#151515')
call NERDTreeHighlightFile('md', 'blue', 'none', '#3366FF', '#151515')
call NERDTreeHighlightFile('yml', 'yellow', 'none', 'yellow', '#151515')
call NERDTreeHighlightFile('config', 'yellow', 'none', 'yellow', '#151515')
call NERDTreeHighlightFile('conf', 'yellow', 'none', 'yellow', '#151515')
call NERDTreeHighlightFile('json', 'yellow', 'none', 'yellow', '#151515')
call NERDTreeHighlightFile('html', 'yellow', 'none', 'yellow', '#151515')
call NERDTreeHighlightFile('styl', 'cyan', 'none', 'cyan', '#151515')
call NERDTreeHighlightFile('cpp', 'cyan', 'none', 'cyan', '#151515')
call NERDTreeHighlightFile('coffee', 'Red', 'none', 'red', '#151515')
call NERDTreeHighlightFile('js', 'Red', 'none', '#ffa500', '#151515')
call NERDTreeHighlightFile('h', 'Magenta', 'none', '#ff00ff', '#151515')

" taglist setting
let Tlist_Auto_Highlight_Tag=1
let Tlist_Auto_Open=1
let Tlist_Auto_Update=1
"let Tlist_Close_On_Select=1
let Tlist_Display_Tag_Scope=1
let Tlist_Exit_OnlyWindow=1
let Tlist_Enable_Dold_Column=1
let Tlist_File_Fold_Auto_Close=1
let Tlist_Show_One_File=1
let Tlist_Use_Right_Window=1
nnoremap <silent> <F8> :TlistToggle<CR>
nnoremap <silent> <F7> :tselect<CR>

"" syntastic setting
"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*
"let g:syntastic_always_populate_loc_list = 1
"let g:syntastic_auto_loc_list = 1
"let g:syntastic_check_on_open = 1
"let g:syntastic_check_on_wq = 0

" srcexpl
" // The switch of the Source Explorer
nmap <F9> :SrcExplToggle<CR>

" // Set the height of Source Explorer window
let g:SrcExpl_winHeight = 8

" // Set 100 ms for refreshing the Source Explorer
let g:SrcExpl_refreshTime = 100

" // Set "Enter" key to jump into the exact definition context
let g:SrcExpl_jumpKey = "<ENTER>"

" // Set "Space" key for back from the definition context
let g:SrcExpl_gobackKey = "<SPACE>"

" // In order to avoid conflicts, the Source Explorer should know what plugins
" // except itself are using buffers. And you need add their buffer names into
" // below listaccording to the command ":buffers!"
let g:SrcExpl_pluginList = [
        \ "__Tag_List__",
        \ "_NERD_tree_"
    \ ]

" // Enable/Disable the local definition searching, and note that this is not
" // guaranteed to work, the Source Explorer doesn't check the syntax for now.
" // It only searches for a match with the keyword according to command 'gd'
let g:SrcExpl_searchLocalDef = 1

" // Do not let the Source Explorer update the tags file when opening
let g:SrcExpl_isUpdateTags = 0

" // Use 'Exuberant Ctags' with '--sort=foldcase -R .' or '-L cscope.files' to
" // create/update the tags file
let g:SrcExpl_updateTagsCmd = "ctags --sort=foldcase -R ."

" // Set "<F12>" key for updating the tags file artificially
let g:SrcExpl_updateTagsKey = "<F12>"

" // Set "<F3>" key for displaying the previous definition in the jump list
let g:SrcExpl_prevDefKey = "<F3>"

" // Set "<F4>" key for displaying the next definition in the jump list
let g:SrcExpl_nextDefKey = "<F4>"

"autocmd FileType python set omnifunc=pythoncomplete#Complete
"autocmd FileType javascrīpt set omnifunc=javascriptcomplete#CompleteJS
"autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
"autocmd FileType css set omnifunc=csscomplete#CompleteCSS
"autocmd FileType xml set omnifunc=xmlcomplete#CompleteTags
"autocmd FileType php set omnifunc=phpcomplete#CompletePHP
"autocmd FileType c set omnifunc=ccomplete#Complete

" pythondiction plugin
"let g:pydiction_location='~/.vim/pydiction/complete-dict'
"let g:pydiction_menu_height = 3

" C configure setting
set cindent
set cinoptions={0,1s,t0,n-2,p2s,(03s,=.5s,>1s,=1s,:1s

" close bell ring
set vb t_vb=
" delete end of file unuseful space
autocmd BufWritePre * :%s/\s\+$//e

" Backup  CPP highlight
"let b:current_syntax = "cpp"
"
"" status
"highlight StatusLine ctermbg=196 ctermfg=109
"highlight StatusLineNC ctermbg=164 ctermfg=196
"" set fold color
"highlight Folded ctermbg=239 ctermfg=154
"" set cursorcolumn color
"highlight CursorColumn ctermbg=233
"
"" types
"syntax keyword type int double short float long unsigned signed char void
"syntax keyword type_plus bool boolean uint16_t int16_t uint32_t int32_t
"syntax keyword type_plus bool boolean uint16 sint16 uint32 sint32 uint64 sint64 uint8 sint8
"syntax keyword type_plus uint64_t int64_t size_t inline
"syntax keyword type_plus size_t ssize_t
"highlight type ctermfg=199
"highlight link type_plus type
"" keyword
"syntax keyword keyword_basic break case const continue default do else
"syntax keyword keyword_basic extern for goto if register restrict
"syntax keyword keyword_basic return sizeof static switch typedef
"syntax keyword keyword_basic volatile while auto false true
"highlight keyword_basic ctermfg=40
"" structure & union & enum
"syntax match struct_name contained "struct \w*[ ),]"hs=s+7,he=e-1
"syntax match struct_key display "struct [a-zA-Z_]" contains=struct_name
"highlight struct_name ctermfg=99
"highlight link struct_key keyword_basic
"
"syntax match union_name contained "union \w* "hs=s+6
"syntax match union_key display "union [a-zA-Z_]" contains=union_name
"highlight link union_name struct_name
"highlight link union_key keyword_basic
"
"syntax match enum_name contained "enum \w* "hs=s+5
"syntax match enum_key display "enum [a-zA-Z_]" contains=enum_name
"highlight link enum_name struct_name
"highlight link enum_key keyword_basic
"" cpp
"syntax match cpp contained "#\(define\|ifdef\|ifndef\|if\|else\|defined\)"
"syntax match cpp_name display "#\w\+\s\+\w\+" contains=cpp
"syntax match cpp_sp "#endif"
"highlight cpp ctermfg=53
"highlight cpp_name ctermfg=154
"highlight link cpp_sp cpp
"
"" include
"syntax match included contained "#include .*"hs=s+9
"syntax match include display "#include [<|\"]" contains=included
