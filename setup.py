import os

def check_shell():
    try:
        shell = os.environ['SHELL']
        if shell.find('bash')!= -1:
            profile = os.path.expanduser('~/.bashrc')
            logout_profile = os.path.expanduser('~/.bash_logout')
        elif shell.find('zsh')!= -1:
            profile = os.path.expanduser('~/.zshrc')
            logout_profile = os.path.expanduser('~/.zlogout')

        script = '\n# added by multigit\nsource $HOME/.multigit\n'
        logout_script = '\n# added by multigit\nssh-add -D\neval $(ssh-agent -k)\ngit config --global --unset user.name\ngit config --global --unset user.email\n'
        if shell.find('bash') != -1 or shell.find('zsh') != -1:
            with open(profile, 'a+') as f, open(logout_profile, 'a+') as g:
                f.seek(0)
                if script in f.read():
                    print('Setup is already complete')
                else:
                    f.seek(0,2)
                    f.write(script)
                    g.write(logout_script)

    except KeyError:
        print("Cannot automatically detect shell (terminal), need to manually add config on your shell profile!!")
        profile = None
        logout_profile = None



if __name__ == "__main__":
    check_shell()