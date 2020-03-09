import random

import faker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, BLOB, Date, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = "invoice_customer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    jdate = Column(Date)
    address = Column(String)
    email = Column(String)
    invoices = relationship('Invoice', backref="customer")


class Invoice(Base):
    __tablename__ = "invoice_invoice"
    id = Column(Integer, primary_key=True)
    particulars = Column(String)
    date = Column(Date)
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey('invoice_customer.id'))


def create_db():
    url = "postgres://rgoucqeeukzkww:2ef63a2930b664556ec73b8671dd633d6d8d9acc32fc73e94590096769d1c166@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/dbi2grgbsipj1l"
    #url = "sqlite:///invoice_db.sqlite"
    engine = create_engine(url)
    Base.metadata.create_all(engine)


def get_session():
    url = "postgres://rgoucqeeukzkww:2ef63a2930b664556ec73b8671dd633d6d8d9acc32fc73e94590096769d1c166@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/dbi2grgbsipj1l"
    #url = "sqlite:///invoice_db.sqlite"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def main():
    create_db()
    f = faker.Faker()
    session = get_session()
    for i in range(100):
        c = Customer(name=f.name(),
                     jdate=f.date(),
                     address=f.address(),
                     email=f.email())
        session.add(c)
        for j in range(5):
            invoice = Invoice(particulars=f.sentence(),
                              date=f.date(),
                              amount=random.randint(10, 99),
                              customer=c)
            session.add(invoice)
    session.commit()


if __name__ == "__main__":
    main()
