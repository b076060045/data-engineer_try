# 建構基礎image
from ubuntu:18.04
# 系統升級 安裝Python
run apt-get update && apt-get install python3.6 -y && apt-get install python3-pip -y
# 建立資料夾
run mkdir /NBA
# 把現在工作環境下的資料夾完全複製
copy . /NBA/
# 轉換工作路徑
workdir /NBA/

#env 環境設置
env LC_ALL = C.UTF-8
env LANC = C.UTF-8

#install package
run pip3 install pipenv==2020.6.2
#下載在pipfile.lock裡的所有套件
run pip3 install sync

#genenv
run version=relaese python3 genenv.py

expose 8888
#cmd預設指令
#CMD ["poetry", "run", "uvicorn", "make_api:app", "--host", "0.0.0.0", "--port", "8888"]