validate_path=`pwd`/validateResult.py
read -p "please enter date(e.g. 1,2...30): " num
expr $num + 1 >/dev/null 2>&1
if [ $? -eq 0 ];then
	if [ "$num" -ge "1" ]&&[ "$num" -le "9" ];then
		python $validate_path -d $num
	else
		echo "please enter 1-9"
	fi
else 
	echo "please enter number"
fi
