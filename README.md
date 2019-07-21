<h2>Wallet Service</h2>
Wallet Service implemented with Python/ Django/ REST. 
It exposes API's for :
- Get Wallet Balance
- Deposit to wallet (with and without promotional code)
- Withdraw from wallet
- Get wallet Mini-statement.
- Validate Promotional Code.
- List all registered accounts. (Admin)
- List all transaction history (Paginated).

For now, creation of wallet is handled through admin.

<h4>Requirements:<h4>
* Python==3.7.6
 
* Django==2.2.3

* django-fsm==2.6.1

* django-fsm-admin==1.2.4

* djangorestframework==3.10.0

* gunicorn==19.9.0

* pytz==2019.1

* sqlparse==0.3.0


Uses SqLite3 database. Can be extended easily to use any database.

<h4>Steps to run server:</h4>

```pip3 install -r requirements.txt```

```python3 manage.py migrate```

```python3 manage.py runserver```

Server would be available at http://127.0.0.1:8000/

<h4>Testing:</h4>

```python3 manage.py test```

<h4>Demo:<h4>

A demo is hosted on micro Amazon EC2 instance.

http://ec2-3-17-206-5.us-east-2.compute.amazonaws.com/

<h4>Postman collection :</h4>
 
 https://www.getpostman.com/collections/f271bd652fea9c9acd2f 
