# How to Connect to Sqlite
from datetime import datetime
from random import choice, choices
from unicodedata import category
from xml.etree.ElementInclude import default_loader
# from aenum import unique
from numpy import true_divide
from peewee import *

db = SqliteDatabase('Library_Database.db')

class Login(Model):
    username = CharField()
    password = CharField()
    its_me = IntegerField()
    error = IntegerField()

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

class Category(Model):
    category_name = CharField()
    parent_category = IntegerField(null=True)  #Recursive relationship

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

class Publisher(Model):
    name = CharField(unique=True)
    Location = CharField(null=True)

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

class Author(Model):
    name = CharField(unique=True)
    Location = CharField(null=True)

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

BOOK_STATUS = (
    (1,'New'),
    (2,'Used'),
    (3,'Damaged'),

)

class Books(Model):
    title = CharField(null=True)
    description = TextField(null=True)
    category = ForeignKeyField(Category , backref='category' , null=True)
    code = CharField(null=True)
    barcode = CharField()

    # parts =
    part_order = IntegerField(null=True)
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher , backref='publisher' , null=True)
    author = ForeignKeyField(Author , backref='author' , null=True)
    image = CharField(null=True)
    status = CharField(choices=BOOK_STATUS) # Choices
    date = DateTimeField(default=datetime.now)

    quantity = IntegerField(null=True)
    Branch = IntegerField(null=True)

    # Book's Image
    image = BlobField(null=True)




    class Meta:
        database = db # This model uses the 'Library_Database.db' database.
    


class Clients(Model):
    name = CharField()
    mail = CharField(null=True , unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.now)
    national_id = IntegerField(null=True , unique=True)
    
    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

class Employee(Model):
    name = CharField()
    mail = CharField(null=True , unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.now)
    national_id = IntegerField(null=True , unique=True)
    Periority = IntegerField(null=True)
    Branch = IntegerField(null=True)
    Password = CharField(null=True)
    image = CharField(null=True)

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.


class Employee_Permission(Model):
    name = CharField(null=True) # Employee name
    
    # Book Permission
    add_book =  IntegerField()
    edit_book =  IntegerField()
    delete_book =  IntegerField()
    export_book =  IntegerField()
    import_book =  IntegerField()

    # Client Permission
    add_client =  IntegerField()
    edit_client =  IntegerField()
    delete_client =  IntegerField()
    export_client =  IntegerField()
    import_client =  IntegerField()

    # Public Permission
    book_tap =  IntegerField()
    client_tap =  IntegerField()
    dashbourd_tap =  IntegerField()
    history_tap =  IntegerField()
    reports_tap =  IntegerField()
    settings_tap =  IntegerField()

    # Settings Permission
    add_data =  IntegerField()
    add_employee =  IntegerField()
    edit_employee =  IntegerField()

    # Special Permission
    admin = IntegerField()
    

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.


class Branch(Model):
    name = CharField()
    code = CharField(null=True , unique=True)
    location = CharField(null=True)
    admin = CharField()

    

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

PROCESS_TYPE = (
    (1,'Rent'),
    (2,'Retrieve')
)

class Daily_Movments(Model):
    book = ForeignKeyField(Books , backref='daily_book')
    client = ForeignKeyField(Clients , backref='book_client')
    type = CharField(choices=PROCESS_TYPE)  # Rent or Retreve
    price = IntegerField(null=True)
    date = DateTimeField(default=datetime.now)
    branch = ForeignKeyField(Branch,backref='Daily_branch' , null=True)
    Book_from = DateField(null=True)
    Book_to = DateField(null=True)
    employee = ForeignKeyField(Employee , backref='Daily_employee' , null = True)

    class Meta:
        database = db # This model uses the 'Library_Database.db' database.

ACTIONS_TYPE = (
    (1,'Login'),
    (2,'Update'),
    (3,'Create'),
    (4,'Delete'),

)

TAPLE=CHOICES = (
    (1,'Books'),
    (2,'Clients'),
    (3,'Employee'),
    (4,'Category'),
    (5,'Branch'),
    (6,'Daily_Movemnets'),
    (7,'Publisher'),
    (8,'Author'),

)

class History(Model):
    employee = CharField(null=True)
    actions = CharField(choices=ACTIONS_TYPE)
    date = DateTimeField(default=datetime.now)
    branch = ForeignKeyField(Branch,backref='History_branch' , null=True)
    extra = CharField(null=True)


    class Meta:
        database = db # This model uses the 'Library_Database.db' database.



# Connection
db.connect()
db.create_tables([Login, Category , Publisher , Author , Books , Clients , Employee , Employee_Permission, Branch , Daily_Movments , History])