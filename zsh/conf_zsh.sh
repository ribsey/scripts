#!/bin/bash
# https://github.com/romkatv/powerlevel10k#oh-my-zsh
# https://gist.github.com/dogrocker/1efb8fd9427779c827058f873b94df95
command_exists() {
	command -v "$@" >/dev/null 2>&1
}

echo "Checking if zsh installed"
if ! command_exists zsh; then
    sudo apt update
    sudo apt install zsh -y
fi

echo "Checking if curl installed"
if ! command_exists curl; then
    sudo apt update
    sudo apt install curl -y
fi

echo "Installing 'Oh my zsh'"
# disable autorun of zsh after installing oh my zsh
export RUNZSH=no
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

echo "Checking if git installed"
if ! command_exists git; then
    sudo apt update
    sudo apt install git -y
fi

echo $ZSH_CUSTOM
ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}

echo "Downloading zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
echo "Downloading zsh-syntax-highlighting"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

echo "Enabling plugins"
str=$(grep -oP '^plugins=\([\w\s-]+\)$' ~/.zshrc | sed 's/)/ zsh-autosuggestions zsh-syntax-highlighting)/g')
echo "$(sed "s/^plugins=.*/$str/g" ~/.zshrc)" > ~/.zshrc
mv temp

# echo "Install fonts for ZSH theme"
# wget -P ~/.local/share/fonts https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
# wget -P ~/.local/share/fonts https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
# wget -P ~/.local/share/fonts https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
# wget -P ~/.local/share/fonts https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# echo "Downloading powerlevel10k"
# git clone --depth=1 https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k

echo "Setting theme"
echo "$(sed -E "s/^ZSH_THEME=\".+\"$/ZSH_THEME=\"candy\"/g" ~/.zshrc)" > ~/.zshrc