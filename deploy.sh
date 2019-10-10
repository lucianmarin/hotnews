PREVIOUS=$PWD
cd ~/newscafe/
git pull
python3 manage.py migrate
pkill -HUP -F news.pid
cd $PREVIOUS
