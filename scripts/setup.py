import os



def check_shell():
    try:
        shell = os.environ['SHELL']
        if shell.find('bash'):
            profile = '~/.bashrc'
            logout_profile = '~/.bash_logout'
        elif shell.find('zsh'):
            profile = '~/.zshrc'
            logout_profile = '~/.zlogout'
        else :
            print("Cannot automatically detect shell (terminal), need to manually add config on your shell profile!!")
            profile = None
            logout_profile = None

    except :
            print("$SHELL evironment variable could not be found!!\nNeed to manually add config on your shell profile")
    

    

    




if __name__ == "__main__":
    check_shell()