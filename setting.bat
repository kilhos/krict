echo 'setting...'

rem 모두 yes 입력!

call conda activate base

rem 특정 위치에 저장할 때: -p 옵션 적용 (주석[rem] 해제하고 path만 바꿔 배치 돌려주세요.)
set venv_path=C:\esb\envs\krict
call conda env remove --prefix %venv_path%
call conda create -c conda-forge --prefix %venv_path% python=3.8.12 rdkit
call conda activate %venv_path%

rem 디폴트 위치에 저장할 때: -n 옵션 적용. (주석[rem] 해제하고 path만 바꿔 배치 돌려주세요.)
rem set venv=krict
rem call conda env remove -n %venv%
rem call conda create -c conda-forge -n %venv% python=3.8.12 rdkit
rem call conda activate %venv%

call pip install django
call pip install django_crontab

call pip install mysqlclient

call pip install b4
call pip install -r requirements.txt

echo 'Done.'

rem 필요시 포트 변경
call python manage.py makemigrations
call python manage.py migrate
call python manage.py runserver 8080