sudo pip3 install virtualenv
virtualenv newenv
source newenv/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic