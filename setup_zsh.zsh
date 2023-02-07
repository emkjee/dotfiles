#!/usr/bin/env zsh

echo "\n|%-> Starting ZSH Setup <-%|\n"

#how-to-test-if-string-exists-in-file-with-bash/4749368#4749368
#https://stackoverflow.com/questions/4749330 how-to-test-if-string-exists-in-file-with-bash/4749368#4749368
if grep -Fxq '/usr/local/bin/zsh' '/etc/shells'; then
  echo '|%-> /usr/local/bin/zsh already exists in /etc/shells'
  echo '|%->'
else
  echo '|%-> Enter superuser (sudo) password to edit /etc/shells'
  echo '/usr/local/bin/zsh' | sudo tee -a '/etc/shells' >/dev/null
fi

if [ "$SHELL" = '/usr/local/bin/zsh' ]; then
  echo '|%-> $SHELL is already /usr/local/bin/zsh'
  echo '|%->'
else
  echo '|%-> Enter user password to change login shell'
  chsh -s '/usr/local/bin/zsh'
fi

# if sh --version | grep -q zsh; then
#   echo '/private/var/select/sh already linked to /bin/zsh'
#   echo ' '
# else
#   echo 'Enter superuser (sudo) password to symlink sh to zsh'
#   sudo ln -sfv /bin/zsh /private/var/select/sh

#   #I would like this one to work instead!
#   #sudo ln -sfv /usr/local/bin/zsh /private/var/select/sh
# fi