var1=$(ps -ef|grep '/home1/ncloud/anaconda3/envs/krict/bin/python'|awk '{print $2}')
pid=$(echo ${var1})
echo 'kill......'
echo ${pid}
if [ -n  "${pid}" ]
then
   kill -9 ${pid}
fi
