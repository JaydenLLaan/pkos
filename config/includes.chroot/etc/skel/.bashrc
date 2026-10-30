case $- in *i*) ;; *) return;; esac
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
HISTSIZE=10000
HISTFILESIZE=20000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend checkwinsize
PS1='\[\e[38;2;139;171;192m\]\u\[\e[0m\] \[\e[38;2;155;170;185m\]\w\[\e[0m\] \$ '
alias ll='ls -lah --color=auto'
alias fd='fdfind'
alias bat='batcat'
alias vim='nvim'
alias g='git'
[ ! -r /usr/share/bash-completion/bash_completion ] || . /usr/share/bash-completion/bash_completion

