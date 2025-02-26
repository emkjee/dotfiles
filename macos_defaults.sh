## setup delay until repeat & key repeat rate, to shortest / fastest
defaults write -g InitialKeyRepeat -int 15
defaults write -g KeyRepeat -int 2

## setup scroll direction, turn off natural scrolling
defaults write -g com.apple.swipescrolldirection -int 0

## enable repeat key
defaults write -g ApplePressAndHoldEnabled 0

## dock / stage manager / mission control ##########################################################
    ## dock - don't show recent applications in dock
defaults write com.apple.dock show-recents -int 0
## mission control - automatically rearrange space based on most recent use <turn off>
defaults write com.apple.dock mru-spaces -int 0
## group windows by applications <turn off>
defaults write com.apple.dock expose-group-apps -int 0
####################################################################################################