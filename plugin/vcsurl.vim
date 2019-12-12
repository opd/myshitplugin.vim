let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import vcsurl
EOF

function! GetVCSLineUrl()
  python3 vcsurl.get_vcs_line_url()
endfunction
command -nargs=0 GetVCSLineUrl call GetVCSLineUrl()


" Per project info
function! PerProjectViminfo()
  python3 vcsurl.per_project_viminfo()
endfunction
command -nargs=0 PerProjectViminfo call PerProjectViminfo()

autocmd BufReadPre,FileReadPre,BufNew * :PerProjectViminfo
autocmd BufWritePost * :wv


" Capture
function! Capture()
  python3 vcsurl.capture()
endfunction

command! -nargs=0 Capture call Capture()

vnoremap q :<C-u>Capture<Return>

" ControlP
fu! vcsurl#match(items, str, limit, mmode, ispath, crfile, regex)
  python3 vcsurl.custom_match()
  return ret_val
endf

fu! vcsurl#match2()
  python3 vcsurl.custom_match()
  return ret_val
endf

let g:ctrlp_match_func = {'match' : 'vcsurl#match'}

" fu! vcsurl#onearg(data)
"   python3 vcsurl.one_arg()
" endf
" 
" 
" let g:ctrlp_status_func = { 'arg_type' : 'dict', 'enter' : 'vcsurl#onearg'}
"
" :let m = matchadd("CtrlPMatch", "pro\\zsd\\zeuct", 1, 3001)
" :call matchdelete(3001)
