from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True)
    publish_date = Column(DateTime)
    description = Column(String(1000))
    cover_image = Column(String(500))
    available = Column(Boolean, default=True)
    loans = relationship('Loan', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow)
    loans = relationship('Loan', backref='member', lazy=True)

    def __repr__(self):
        return f'<Member {self.name}>'

class Loan(Base):
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)

    def __repr__(self):
        return f'<Loan {self.book_id} to {self.member_id}>'
