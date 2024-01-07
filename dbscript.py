"""
python manage.py shell
exec(open('dbscript.py').read())
"""
from django.contrib.auth.models import User
from api.models import Book, Shop

u = User(username="BenGunn", first_name="Ben", last_name="Gunn", email="BenGunn@example.com")
u.set_password("user")
u.save()
u = User(username="DrLivesey", first_name="David", last_name="Livesey", email="DrLivesey@example.com")
u.set_password("user")
u.save()
u = User(username="JimHawkins", first_name="Jim", last_name="Hawkins", email="JimHawkins@example.com")
u.set_password("user")
u.save()

Book(title="Treasure Island", author="Robert Louis Stevenson", release_date="1883-11-14").save()
Book(title="Back to Treasure Island", author="Harold Augustin Calahan", release_date="1935-11-11").save()
Book(title="Jim Hawkins and the Curse of Treasure Island", author="Frank Delaney", release_date="2001-11-11").save()

Shop(name="Hodkiewicz-Mitchell", address="673 Mallory Junction").save()
Shop(name="Cremin-Cartwright", address="096 Mifflin Plaza").save()
Shop(name="Little-Herman", address="95168 Corben Crossing").save()

print("all done")
quit()
