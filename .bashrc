# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

## for python devel
if [ -f /usr/bin/virtualenvwrapper.sh ]; then
    export WORKON_HOME=~/.virtualenvs
    . /usr/bin/virtualenvwrapper.sh
fi
if [ -f /etc/profile.d/bash_completion.sh ]; then
    . /etc/profile.d/bash_completion.sh
fi
