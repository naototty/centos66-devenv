" release autogroup in MyAutoCmd
augroup MyAutoCmd
  autocmd!
augroup END



set ignorecase          " 大文字小文字を区別しない
set smartcase           " 検索文字に大文字がある場合は大文字小文字を区別
set incsearch           " インクリメンタルサーチ
set hlsearch            " 検索マッチテキストをハイライト (2013-07-03 14:30 修正）

" バックスラッシュやクエスチョンを状況に合わせ自動的にエスケープ
cnoremap <expr> / getcmdtype() == '/' ? '\/' : '/'
cnoremap <expr> ? getcmdtype() == '?' ? '\?' : '?'
"
"


set shiftround          " '<'や'>'でインデントする際に'shiftwidth'の倍数に丸める
set infercase           " 補完時に大文字小文字を区別しない
"######## set virtualedit=all     " カーソルを文字が存在しない部分でも動けるようにする
set hidden              " バッファを閉じる代わりに隠す（Undo履歴を残すため）
set switchbuf=useopen   " 新しく開く代わりにすでに開いてあるバッファを開く
set showmatch           " 対応する括弧などをハイライト表示する
set matchtime=3         " 対応括弧のハイライト表示を3秒にする


" 対応括弧に'<'と'>'のペアを追加
set matchpairs& matchpairs+=<:>

" バックスペースでなんでも消せるようにする
set backspace=indent,eol,start

" クリップボードをデフォルトのレジスタとして指定。後にYankRingを使うので
" 'unnamedplus'が存在しているかどうかで設定を分ける必要がある
if has('unnamedplus')
    " set clipboard& clipboard+=unnamedplus " 2013-07-03 14:30 unnamed 追加
    set clipboard& clipboard+=unnamedplus,unnamed 
else
    " set clipboard& clipboard+=unnamed,autoselect 2013-06-24 10:00 autoselect 削除
    set clipboard& clipboard+=unnamed
endif

" Swapファイル？Backupファイル？前時代的すぎ
" なので全て無効化する
set nowritebackup
set nobackup
set noswapfile

set laststatus=2
"ステータス行の指定
set statusline=%<%f\ %m%r%h%w
set statusline+=%{'['.(&fenc!=''?&fenc:&enc).']['.&fileformat.']'}
set statusline+=%=%l/%L,%c%V%8P
"

let g:jedi#auto_initialization = 1
let g:jedi#rename_command = "<leader>R"
let g:jedi#popup_on_dot = 1
autocmd FileType python let b:did_ftplugin = 1


set list                " 不可視文字の可視化
set number              " 行番号の表示
set wrap                " 長いテキストの折り返し
set textwidth=0         " 自動的に改行が入るのを無効化
""""""""" Error  set colorcolumn=80      " その代わり80文字目にラインを入れる

" 前時代的スクリーンベルを無効化
set t_vb=
set novisualbell

" デフォルト不可視文字は美しくないのでUnicodeで綺麗に
set listchars=tab:»-,trail:-,extends:»,precedes:«,nbsp:%,eol:↲







" 入力モード中に素早くjjと入力した場合はESCとみなす
inoremap jj <Esc>


" ESCを二回押すことでハイライトを消す
nmap <silent> <Esc><Esc> :nohlsearch<CR>

" カーソル下の単語を * で検索
vnoremap <silent> * "vy/\V<C-r>=substitute(escape(@v, '\/'), "\n", '\\n', 'g')<CR><CR>

" 検索後にジャンプした際に検索単語を画面中央に持ってくる
nnoremap n nzz
nnoremap N Nzz
nnoremap * *zz
nnoremap # #zz
nnoremap g* g*zz
nnoremap g# g#zz

" j, k による移動を折り返されたテキストでも自然に振る舞うように変更
nnoremap j gj
nnoremap k gk

" vを二回で行末まで選択
vnoremap v $h

" TABにて対応ペアにジャンプ
nnoremap <Tab> %
vnoremap <Tab> %

" Ctrl + hjkl でウィンドウ間を移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Shift + 矢印でウィンドウサイズを変更
nnoremap <S-Left>  <C-w><<CR>
nnoremap <S-Right> <C-w>><CR>
nnoremap <S-Up>    <C-w>-<CR>
nnoremap <S-Down>  <C-w>+<CR>

" T + ? で各種設定をトグル
nnoremap [toggle] <Nop>
nmap T [toggle]
nnoremap <silent> [toggle]s :setl spell!<CR>:setl spell?<CR>
nnoremap <silent> [toggle]l :setl list!<CR>:setl list?<CR>
nnoremap <silent> [toggle]t :setl expandtab!<CR>:setl expandtab?<CR>
nnoremap <silent> [toggle]w :setl wrap!<CR>:setl wrap?<CR>

""###########################################" make, grep などのコマンド後に自動的にQuickFixを開く
""###########################################autocmd MyAutoCmd QuickfixCmdPost make,grep,grepadd,vimgrep copen
""###########################################
""###########################################" QuickFixおよびHelpでは q でバッファを閉じる
""###########################################autocmd MyAutoCmd FileType help,qf nnoremap <buffer> q <C-w>c
""###########################################
""###########################################" w!! でスーパーユーザーとして保存（sudoが使える環境限定）
""###########################################cmap w!! w !sudo tee > /dev/null %
""###########################################
""###########################################" :e などでファイルを開く際にフォルダが存在しない場合は自動作成
""###########################################function! s:mkdir(dir, force)
""###########################################  if !isdirectory(a:dir) && (a:force ||
""###########################################        \ input(printf('"%s" does not exist. Create? [y/N]', a:dir)) =~? '^y\%[es]$')
""###########################################    call mkdir(iconv(a:dir, &encoding, &termencoding), 'p')
""###########################################  endif
""###########################################endfunction
""###########################################autocmd MyAutoCmd BufWritePre * call s:mkdir(expand('<afile>:p:h'), v:cmdbang)
""###########################################
""###########################################" vim 起動時のみカレントディレクトリを開いたファイルの親ディレクトリに指定
""###########################################autocmd MyAutoCmd VimEnter * call s:ChangeCurrentDir('', '')
""###########################################function! s:ChangeCurrentDir(directory, bang)
""###########################################    if a:directory == ''
""###########################################        lcd %:p:h
""###########################################    else
""###########################################        execute 'lcd' . a:directory
""###########################################    endif
""###########################################
""###########################################    if a:bang == ''
""###########################################        pwd
""###########################################    endif
""###########################################endfunction

" ~/.vimrc.localが存在する場合のみ設定を読み込む
let s:local_vimrc = expand('~/.vimrc.local')
if filereadable(s:local_vimrc)
    execute 'source ' . s:local_vimrc
endif


let s:noplugin = 0
" let s:bundle_root = expand('~/.vim/bundle')
let s:bundle_root = expand('~/.vim/bundle')
" let s:neobundle_root = s:bundle_root . '/neobundle.vim'
let s:neobundle_root = s:bundle_root . '/neobundle.vim'
if !isdirectory(s:neobundle_root) || v:version < 702
    " NeoBundleが存在しない、もしくはVimのバージョンが古い場合はプラグインを一切
    " 読み込まない
    let s:noplugin = 1
else
    " NeoBundleを'runtimepath'に追加し初期化を行う
    if has('vim_starting')
        execute "set runtimepath+=" . s:neobundle_root
    endif
    call neobundle#begin(s:bundle_root)
        "### NeoBundleFetch g:bundle_root
        NeoBundleLocal s:bundle_root
        "### NeoBundleFetch s:bundle_root
    call neobundle#end()

    " NeoBundle自身をNeoBundleで管理させる
    NeoBundleFetch 'Shougo/neobundle.vim'


    " 非同期通信を可能にする
    " 'build'が指定されているのでインストール時に自動的に
    " 指定されたコマンドが実行され vimproc がコンパイルされる
    NeoBundle "Shougo/vimproc", {
        \ "build": {
        \   "windows"   : "make -f make_mingw32.mak",
        \   "cygwin"    : "make -f make_cygwin.mak",
        \   "mac"       : "make -f make_mac.mak",
        \   "unix"      : "make -f make_unix.mak",
        \ }}

    " (ry
    "## NeoBundle 'git://github.com/Shougo/clang_complete.git'
    NeoBundle 'git://github.com/Shougo/echodoc.git'
    "### NeoBundle 'git://github.com/Shougo/neocomplcache.git'
    NeoBundle 'git://github.com/Shougo/neocomplete.git'
    NeoBundle 'git://github.com/Shougo/neobundle.vim.git'
    NeoBundle 'git://github.com/Shougo/unite.vim.git'
    NeoBundle 'git://github.com/Shougo/vim-vcs.git'
    NeoBundle 'git://github.com/Shougo/vimfiler.git'
    NeoBundle 'git://github.com/Shougo/vimshell.git'
    NeoBundle 'git://github.com/Shougo/vinarise.git'

    " インストールされていないプラグインのチェックおよびダウンロード
    NeoBundleCheck
endif



""###########################################" ファイルタイププラグインおよびインデントを有効化
""###########################################" これはNeoBundleによる処理が終了したあとに呼ばなければならない
""###########################################
""###########################################    NeoBundle "Shougo/vimproc", {
""###########################################        \ "build": {
""###########################################        \   "windows"   : "make -f make_mingw32.mak",
""###########################################        \   "cygwin"    : "make -f make_cygwin.mak",
""###########################################        \   "mac"       : "make -f make_mac.mak",
""###########################################        \   "unix"      : "make -f make_unix.mak",
""###########################################        \ }}
""###########################################
""###########################################
""###########################################
""###########################################
""###########################################
"## " 次に説明するがInsertモードに入るまではneocompleteはロードされない
"## NeoBundleLazy 'Shougo/neocomplete.vim', {
"##     \ "autoload": {"insert": 1}}
""###########################################" neocompleteのhooksを取得
""###########################################let s:hooks = neobundle#get_hooks("neocomplete.vim")
""###########################################" neocomplete用の設定関数を定義。下記関数はneocompleteロード時に実行される
""###########################################function! s:hooks.on_source(bundle)
""###########################################    let g:acp_enableAtStartup = 0
""###########################################    let g:neocomplete#enable_smart_case = 1
""###########################################    " NeoCompleteを有効化
""###########################################    NeoCompleteEnable
""###########################################endfunction


"## " Insertモードに入るまでロードしない
"## 
"## NeoBundleLazy 'Shougo/neosnippet.vim', {
"##     \ "autoload": {"insert": 1}}
" 'GundoToggle'が呼ばれるまでロードしない
NeoBundleLazy 'sjl/gundo.vim', {
    \ "autoload": {"commands": ["GundoToggle"]}}
" '<Plug>TaskList'というマッピングが呼ばれるまでロードしない
NeoBundleLazy 'vim-scripts/TaskList.vim', {
    \ "autoload": {"mappings": ['<Plug>TaskList']}}
" HTMLが開かれるまでロードしない
NeoBundleLazy 'mattn/zencoding-vim', {
    \ "autoload": {"filetypes": ['html']}}


NeoBundle "thinca/vim-template"
" テンプレート中に含まれる特定文字列を置き換える
autocmd MyAutoCmd User plugin-template-loaded call s:template_keywords()
function! s:template_keywords()
    silent! %s/<+DATE+>/\=strftime('%Y-%m-%d')/g
    silent! %s/<+FILENAME+>/\=expand('%:r')/g
endfunction
" テンプレート中に含まれる'<+CURSOR+>'にカーソルを移動
autocmd MyAutoCmd User plugin-template-loaded
    \   if search('<+CURSOR+>')
    \ |   silent! execute 'normal! "_da>'
    \ | endif

set tabstop=8
set softtabstop=4
set shiftwidth=4
set expandtab
set smarttab

filetype plugin on 
filetype indent on



"------------------------------------
"" neocomplete.vim
"------------------------------------
""Note: This option must set it in .vimrc(_vimrc).  NOT IN .gvimrc(_gvimrc)!
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0
" Use neocomplete.
let g:neocomplete#enable_at_startup = 1
" Use smartcase.
let g:neocomplete#enable_smart_case = 1
" Set minimum syntax keyword length.
let g:neocomplete#sources#syntax#min_keyword_length = 3
let g:neocomplete#lock_buffer_name_pattern = '\*ku\*'
" Plugin key-mappings.
inoremap <expr><C-g>     neocomplete#undo_completion()
inoremap <expr><C-l>     neocomplete#complete_common_string()

" Recommended key-mappings.
" <CR>: close popup and save indent.
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
  " return neocomplete#close_popup() . "\<CR>"
  " For no inserting <CR> key.
  return pumvisible() ? neocomplete#close_popup() : "\<CR>"
endfunction
" <TAB>: completion.
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><C-y>  neocomplete#close_popup()
inoremap <expr><C-e>  neocomplete#cancel_popup()

" Close popup by <Space>.
inoremap <expr><Space> pumvisible() ? neocomplete#close_popup() : "\<Space>"

autocmd FileType python setlocal omnifunc=pythoncomplete#Complete


" ========== Jedi
NeoBundle 'davidhalter/jedi-vim'

" rename用のマッピングを無効にしたため、代わりにコマンドを定義
" command! -nargs=0 JediRename :call jedi#rename()
"
" " pythonのrename用のマッピングがquickrunとかぶるため回避させる
" let g:jedi#rename_command = ""
" let g:jedi#pydoc = "k"

colorscheme slate

