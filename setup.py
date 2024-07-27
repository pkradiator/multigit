import os
from pathlib import Path
import shutil
import glob
import json

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

def cp_scripts():
    instl_loc = os.path.expanduser('~/.multigit')
    if os.path.isdir(instl_loc) != True:
        os.mkdir(instl_loc)
        repo_dir = Path(__file__).parent.resolve()
        file1_path = repo_dir / 'scripts' / 'script.sh'
        file2_path = repo_dir / 'scripts' / 'multigit'
        shutil.copy(file1_path, instl_loc)
        shutil.copy(file2_path, instl_loc)
    a = True
    while a == True:
    
        response = input("Do you want to detect older keys ?\nType y or n and hit enter\n")
        if (response == 'y'):
            a = False
            detect_keys()

        elif(response == 'n'):
            a= False
        else:
            print("Wrong response!! Answer in y or n")

def detect_keys():
    home = os.path.expanduser('~/')
    key_pattern = home + ".ssh/id_*.pub"
    key_list = glob.glob(key_pattern)
    if key_list == []:
        print("No older keys detected.")
    else:
        print(len(key_list), "keys are detected which are as follows:")
        for j,i in enumerate(key_list):
            print(j+1, i)

        a = True
        while a == True:
            response =input("Do you want to use some or all of these keys.\nNote - You will be promted for following details related to the keys\n1.Git username\n2.Email address\nPress y or n and Hit Enter\n")
            if response == 'y':
                a=False
                acc_list = []
                for i,j in enumerate(key_list):
                    b = True 
                    while b == True:
                        decision= input(f"Do you want to associate an account with the key: {j}\nType y or n and hit enter.\n")
                        if decision == 'n':
                            b=False
                            pass
                        elif decision == 'y':
                            b=False
                            print(f"Enter the account name(github username, bitbucket username etc. where {j} key is used):", end=' ')
                            acc_name = input().strip()
                            email = input("Enter the email associated with account:").strip()
                            acc_list.append({'id_no':i,'acc_name':acc_name, 'email':email, 'key_loc':j[:-4]})
                        else:
                            print("Wrong Response. Type y or n and hit enter.\n")
                acc_file = os.path.expanduser('~/.multigit/data.json')
                with open(acc_file, 'w+') as f:
                    json.dump(acc_list, f)
                
            elif response == 'n':
                a=False
            else:
                print("Wrong Response. Press y or n and hit Enter.\n")


if __name__ == "__main__":
    check_shell()
    cp_scripts()
    
