#!/bin/bash


function start()
{
	echo "启动服务"
	nohup ./main &
}

echo "-------------开始启动服务---------------------"
start
sleep 1s
echo "-------------启动服务结束---------------------"

