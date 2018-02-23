from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, create_engine, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationships


BaseClass = declarative_base()
metadata = BaseClass.metadata

class User(BaseClass):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(Unicode())
    password = Column(Unicode())

    check_1 = UniqueConstraint('name')

    def __repr__(self):
        return "<User(name => {}, password => {})>".format(self.name, self.password)

class UHistory(BaseClass):
    __tablename__ = 'user_history'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    entry_time = Column(DateTime)
    ip_address = Column(Unicode())

    chech_1 = UniqueConstraint('ip_address')

    def __repr__(self):
        return '<UHistory(entry time => {}, ip address =>  {})>'.format(self.entry_time, self.ip_address)

class Contacts(BaseClass):
    __tablename__ = 'contacts_list'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    client_id = Column(Integer(), ForeignKey('users.id'))
    owner_id = Column(Integer(), ForeignKey('users.id'))


#######################################################################################################################


engine = create_engine('sqlite:///messages.db', echo=True)
metadata.create_all(engine)
session = sessionmaker(bind=engine)()

user1 = User(name='Vasia', password='12345678')
session.add(user1)
session.commit()


our_user = session.query(User).filter_by(name='Vasia').first()
print(our_user)