case $- in *i*) ;; *) return;; esac
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
HISTSIZE=10000
HISTFILESIZE=20000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend checkwinsize
__pk_prompt() {
    local branch=workspace dirty=''
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        branch=$(git symbolic-ref --short -q HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
        branch=${branch//[^a-zA-Z0-9_./-]/}
        if [ -n "$(git status --porcelain --untracked-files=normal 2>/dev/null)" ]; then
            dirty='\[\e[38;2;199;172;118m\] ·'
        fi
    fi
    PS1="\[\e[38;2;237;242;247m\]pkos \[\e[38;2;139;171;192m\]@ ${branch}${dirty}\[\e[0m\] \\$ "
}
PROMPT_COMMAND=__pk_prompt
alias ll='ls -lah --color=auto'
alias fd='fdfind'
alias bat='batcat'
alias vim='nvim'
alias g='git'
[ ! -r /usr/share/bash-completion/bash_completion ] || . /usr/share/bash-completion/bash_completion

