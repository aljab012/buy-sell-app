import os

from project import db, create_app
from project.models import Book, User, Category, Event
os.system("rm project/db.sqlite")

app = create_app()
db.create_all(app=create_app())
app.app_context().push()
db.session.commit()

# # up to here is empty database 
# u1 = User(name="alhaitham",password="alhaitham",telephone=6124792144,email="email1")
# u2 = User(name="yahya",password="yahya",telephone=6124792144,email="email2")
# db.session.add(u1)
# db.session.add(u2)

list = []
list.append(Category(name="CSCI"))
list.append(Category(name="EE"))
list.append(Category(name="MATH"))
list.append(Category(name="CHEM"))
list.append(Category(name="STAT"))
list.append(Category(name="ECON"))
list.append(Category(name="ACCT"))
list.append(Category(name="BIOL"))
list.append(Category(name="NSC"))

# i = 0
for category in list:
#     for j in range (1,5):
#         b = Book(title='book {} for {}'.format(i,category.name),details='Details for book {} for {}'.format(i,category.name),price=i*2,category=category,seller = u1)
#         category.books.append(b)
#         i = i+1
#     u1.events.append(Event(event_name='Event{}'.format(i),owner=u1,details="event 1",time="2021",place="Keller",category=category))
    db.session.add(category)
#     i = i+1

db.session.commit()
# books = db.session.execute('select * from book').fetchall()


# from sqlalchemy.orm import joinedload
# query = User.query.options(joinedload('groups'))
# for user in query:
#     print (user, user.groups)
# query = Category.query.options(joinedload('books'))
# for category in query:
#     print (category, category.books)
    
# print (users.length())
# for user in users:
#     print (user.name)