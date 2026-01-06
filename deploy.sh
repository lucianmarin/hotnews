PREVIOUS=$PWD
cd ~/news/
git pull
python3 manage.py migrate
pkill -HUP -F news.pid
cd $PREVIOUS
