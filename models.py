from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()
# Associative table for many-to-many relationship between customers and products
customer_product_association = Table('customer_product_association', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(191), nullable=False)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(255))
    description = Column(Text)
    article = Column(String(255))
    packing = Column(String(255))
    remarks = Column(Text)
    image = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    category = relationship('Category')
    customers = relationship('Customer', secondary=customer_product_association, back_populates='products')


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phone = Column(String(20))
    company_name = Column(String(250))
    email = Column(String(250))
    remarks = Column(String(250))
    product_request = Column(String(250))
    picture = Column(String(250))
    products = relationship('Product', secondary=customer_product_association, back_populates='customers')


# Database initialization
engine = create_engine('sqlite:///exhibition.db', echo=True)
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()