#! /bin/bash

manage_path=`pwd`/manage.py
init_path=`pwd`/init_api.py

host='0.0.0.0'
port=10091

user=apps
mysql_path=/home/$user/mysql # mysql的存放路径

start_system(){
	CUDA_VISIBLE_DEVICES=1 python $manage_path runserver -h $host -p $port
}

first_start(){
	$mysql_path/bin/mysqld-safe  --defaults-file=$mysql_path/my.cnf --user=$user &
	echo `netstat -tln | grep 3306`
	start_system
}

stop_system(){
	ps -ef | grep "python $manage_path runserver -h $host -p $port" | grep -v grep | awk "{print \$2}" | xargs kill
}

init_system(){
	python $init_path
	rm -rf `pwd`/doc/faces_feature/*
	rm -rf `pwd`/static/image/*
	stop_system
	tmux a -t facerecognize
}

case $1 in
	"first")
		first_start
;;
	"start")
		start_system
;;
	"stop")
		stop_system
;;
	"init")
		init_system
;;
esac
