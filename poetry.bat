@ echo off
REM 声明采用UTF-8编码
chcp 65001

echo 初始化环境
python -m poetry install
echo 更新环境
python -m poetry update
echo setuptools降级
python -m poetry run pip install setuptools==19.2.0

echo ------------------------------------------------
python -m poetry show
echo ------------------------------------------------
python -m poetry show --tree
echo ------------------------------------------------

pause