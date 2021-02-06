## populate database with data
python3 DBscript.py




python3  
from project import db, create_app  
db.create_all(app=create_app())  
exit()  