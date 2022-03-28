#!/bin/sh

# 모두 yes 입력!

echo 'setting...'
# CentOS에서 anaconda 가상 환경 실행을 위해 필요한 부분
__conda_setup="$('/home/euclid05/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/euclid05/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/euclid05/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/euclid05/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup

conda activate base
#pip install --upgrade --ignore-installed pip setuptools

venv_path=testtest
conda env remove -n $venv_path
conda create -c conda-forge -n $venv_path python=3.8.12 rdkit
conda activate $venv_path

pip install django
pip install django_crontab

#centos에서 mysqlclient 설치 때문에 해주는 것
#sudo yum install python3-devel mysql-devel

conda install -c quantopian mysqlclient
conda install mysqlclient

pip install b4
pip install -r requirements.txt

echo 'Done.'

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8080 # <- 필요시 포트 변경