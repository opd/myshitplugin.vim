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


function! PerProjectViminfo()
  python3 vcsurl.per_project_viminfo()
endfunction
command -nargs=0 PerProjectViminfo call PerProjectViminfo()

function! MoveWordLeft()
  python3 vcsurl.move_text(left_to_right_direction=True)
endfunction

function! MoveWordRight()
  python3 vcsurl.move_text(left_to_right_direction=False)
endfunction

function! Capture()
  python3 vcsurl.capture()
endfunction

nnoremap gl :call MoveWordLeft()<Return>
nnoremap gh :call MoveWordRight()<Return>

autocmd BufReadPre,FileReadPre * :PerProjectViminfo
autocmd BufWritePost * :wv

command! -nargs=0 Capture call Capture()
vnoremap q :<C-u>Capture<Return>
