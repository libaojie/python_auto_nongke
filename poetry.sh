
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

