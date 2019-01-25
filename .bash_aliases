alias irc='irssi'
alias motd='cat /etc/motd'

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias psg='ps -ef| grep'
alias alpine='alpine -sort arrival/reverse'
alias biggest='find ~ -type f -exec du -a {} + | sort -n -r | head -n 10'
alias mudgame='telnet localhost 5071'
function cdl(){ cd $@; ls -l; }
alias mtrek='telnet mtrek.com 1701'
alias usenet='tin -r'
alias units='~/Code/units/units-2.11/units -f ~/Code/units/units-2.11/definitions.units'
alias beats_raw='echo "x = (`date +%s` + 3600) % 86400; scale=3; x / 86.4" | bc'
alias beats='printf "@\e[0;36m`beats_raw`\e[m\n"'
alias pp='python -mjson.tool'
alias ttbp='~endorphant/bin/ttbp'
alias vuln='find /home/ \! -type l -perm -o=w ! -iwholename '*.git*' 2> /dev/null'
alias vulnc='vuln | sed "s/\/home\/\([^/]*\)\/.*/\1/g" | sort | uniq -c | sort -nr'
alias chat='mesg n; /usr/local/bin/chat'
