sudo pip3 install virtaulenv
virtaulenv newenv
source newenv/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic