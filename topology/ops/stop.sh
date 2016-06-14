sudo docker ps -a | grep -i mini | awk {'print $1'} | xargs sudo docker stop
sudo docker ps -a | grep -i mini | awk {'print $1'} | xargs sudo docker rm
sudo docker ps -a
