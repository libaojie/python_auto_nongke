#! /bin/bash

echo "-------------开始打包---------------------"
# 打包
echo "删除原打包环境"
rm -rf build
echo "打包"
python -m poetry run python setup.py build

# 压缩包体
echo "压缩内部测试版"
zip -r build/alpha.zip build/exe.linux-x86_64-3.6
echo "-------------打包结束---------------------"
