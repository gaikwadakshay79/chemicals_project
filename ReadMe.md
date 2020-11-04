# SETUP

python -m pip install virtualenv
virtualenv venv

##### if on windows

venv\Scripts\activate.bat

##### if on linux

source venv/bin/activate

python -m pip install -r requirements.txt

# RUN

python project/migrate.py
python project/app.py

# Api Guide

### Login

curl -X POST http://0.0.0.0:8080/login -H 'content-type: application/json' -d '{"username":"admin","password":"admin"}'

You will receive accessToken as response on successful authentication. This access_token should be used for further steps.I am using yajrtdqnxwlwoblbzfaupvtqiuzxjvgotjtyrwksrlsyztairxbbhymikyboqzbgawdrfxunbvifmiaa as accesstoken for now.Note that username is admin and password is admin, i have already created this user in db.

### Get All Chemical Elements

curl -X GET 'http://0.0.0.0:8080/chemicals/get?access_token=yajrtdqnxwlwoblbzfaupvtqiuzxjvgotjtyrwksrlsyztairxbbhymikyboqzbgawdrfxunbvifmiaa'

### Get All Commodity

curl -X GET 'http://0.0.0.0:8080/commodity/get?access_token=yajrtdqnxwlwoblbzfaupvtqiuzxjvgotjtyrwksrlsyztairxbbhymikyboqzbgawdrfxunbvifmiaa'

### Get Commodity By id

(325cd5c1-1b24-4758-a010-182b44357542 is my commodity id)

curl -X GET 'http://0.0.0.0:8080/commodity/get/325cd5c1-1b24-4758-a010-182b44357542?access_token=eqlnmbonwtsigvwofvldidgvudgowqdypxwresqlhbklgxnwkiirwirguoejxzgvxoadpwmeqjokllze'

### Update commodity by id

(325cd5c1-1b24-4758-a010-182b44357542 is my commodity id)

curl -X POST 'http://0.0.0.0:8080/commodity/update?access_token=eqlnmbonwtsigvwofvldidgvudgowqdypxwresqlhbklgxnwkiirwirguoejxzgvxoadpwmeqjokllze' -H 'content-type: application/json' -d '{"id":"325cd5c1-1b24-4758-a010-182b44357542","name":"Welldone"}'

### Add Concentration

(325cd5c1-1b24-4758-a010-182b44357542 is my commodity id)
(5d377863-2a73-4298-b47f-7ec64b249a34 is my element id)

curl -X POST 'http://0.0.0.0:8080/composition/update/325cd5c1-1b24-4758-a010-182b44357542/5d377863-2a73-4298-b47f-7ec64b249a34?access_token=eqlnmbonwtsigvwofvldidgvudgowqdypxwresqlhbklgxnwkiirwirguoejxzgvxoadpwmeqjokllze' -H 'content-type: application/json' -d '{"percentage":37}'

### Remove Concentration

(325cd5c1-1b24-4758-a010-182b44357542 is my commodity id)
(5d377863-2a73-4298-b47f-7ec64b249a34 is my element id)

curl -X POST 'http://0.0.0.0:8080/composition/remove/325cd5c1-1b24-4758-a010-182b44357542/5d377863-2a73-4298-b47f-7ec64b249a34?access_token=eqlnmbonwtsigvwofvldidgvudgowqdypxwresqlhbklgxnwkiirwirguoejxzgvxoadpwmeqjokllze'

### Logout

curl -X POST http://0.0.0.0:8080/logout -H 'content-type: application/json' -d '{"access_token":"yajrtdqnxwlwoblbzfaupvtqiuzxjvgotjtyrwksrlsyztairxbbhymikyboqzbgawdrfxunbvifmiaa"}'
