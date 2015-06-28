import os
import sys
import psycopg2
from datetime import datetime
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from sqlalchemy_utils import ArrowType
import arrow
from sqlalchemy import types
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Binary, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError




Base = declarative_base()

engine = create_engine('postgresql://postgres:bury148few951@localhost:5432/postgres',echo=True)
Base.metadata.bind = (engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

DATABASE = engine

class User(UserMixin , Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    title = Column(CHAR(3), nullable = False)
    fname = Column(String(100), nullable = False)
    lname = Column(String(100), nullable = False)
    username = Column(String(100), nullable = False, unique = True)
    email = Column (String(50), nullable =False, unique = True)
    password = Column(String(100), nullable = False)
    address = Column(String(250), nullable = False)
    state = Column(String(50), nullable = False)
    is_Admin = Column(Boolean ,default = False)
    is_Logged = Column(Boolean, default = False)
    is_Active = Column (Boolean , default = False)
    is_Block = Column(Boolean, default = False)
    joined_On = Column(ArrowType)
    

    @classmethod
    def create_user(self,fname, lname,username,email,password,address,state,title, is_Admin = False):
        try:
            session = DBSession()
            myFirstUser = User(
                title = title,
                fname = fname,
                lname = lname,
                username = username,
                email = email,
                password = generate_password_hash(password),
                address = address,
                state = state,
                is_Admin = is_Admin,
                joined_On = arrow.utcnow())
            
          
            session.add(myFirstUser)
            session.commit()
            
        except IntegrityError :
            # recreate the session and re-add your object
            session = DBSession()
            session.add(User)
            raise ValueError('user Already Exist !')
            
        

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)
    
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key =True)
    title = Column(String(250), nullable = False)
    description = Column(String(500), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

class ProductItem(Base):
    __tablename__ ='product_items'
    id = Column(Integer , primary_key = True)
    image_Type = Column(Integer , unique= False)
    image_Size = Column(Integer, default = 0)
    Image = Column(Binary, nullable =False)
    description = Column(String(500), nullable = False)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship(Product)
    

def initialize(re_createTable= False):
    #connection = DATABASE.connect()
    
    if re_createTable :
        Base.metadata.drop_all(DATABASE, checkfirst = True)
        
    
    Base.metadata.create_all(DATABASE, checkfirst = True)
    #connection.close()
    
        
            
            
