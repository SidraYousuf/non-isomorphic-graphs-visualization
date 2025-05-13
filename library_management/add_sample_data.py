from datetime import datetime, timedelta
from database import init_db, db_session
from models import Book, Member, Loan

def add_sample_data():
    # Clear existing data
    db_session.query(Loan).delete()
    db_session.query(Book).delete()
    db_session.query(Member).delete()
    db_session.commit()

    # Add sample books
    books = [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            isbn="9780743273565",
            publish_date=datetime(1925, 4, 10),
            description="A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
            cover_image="https://images.pexels.com/photos/1907785/pexels-photo-1907785.jpeg",
            available=True
        ),
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            isbn="9780446310789",
            publish_date=datetime(1960, 7, 11),
            description="The story of young Scout Finch and her father Atticus, a lawyer who defends a black man accused of a terrible crime.",
            cover_image="https://images.pexels.com/photos/2228580/pexels-photo-2228580.jpeg",
            available=True
        ),
        Book(
            title="1984",
            author="George Orwell",
            isbn="9780451524935",
            publish_date=datetime(1949, 6, 8),
            description="A dystopian novel set in a totalitarian society where critical thought is suppressed.",
            cover_image="https://images.pexels.com/photos/3358707/pexels-photo-3358707.jpeg",
            available=True
        )
    ]
    
    for book in books:
        db_session.add(book)
    
    # Add sample members
    members = [
        Member(
            name="John Smith",
            email="john.smith@example.com",
            join_date=datetime.now() - timedelta(days=30)
        ),
        Member(
            name="Emma Wilson",
            email="emma.wilson@example.com",
            join_date=datetime.now() - timedelta(days=15)
        ),
        Member(
            name="Michael Brown",
            email="michael.brown@example.com",
            join_date=datetime.now() - timedelta(days=7)
        )
    ]
    
    for member in members:
        db_session.add(member)
    
    # Commit to get IDs
    db_session.commit()
    
    # Add sample loans
    loans = [
        Loan(
            book_id=books[0].id,
            member_id=members[0].id,
            loan_date=datetime.now() - timedelta(days=5),
            due_date=datetime.now() + timedelta(days=9),  # 14 days from loan_date
            return_date=None
        ),
        Loan(
            book_id=books[1].id,
            member_id=members[1].id,
            loan_date=datetime.now() - timedelta(days=10),
            due_date=datetime.now() - timedelta(days=3),  # 7 days from loan_date
            return_date=datetime.now() - timedelta(days=3)
        )
    ]
    
    for loan in loans:
        db_session.add(loan)
    
    # Update book availability
    books[0].available = False
    
    db_session.commit()
    print("Sample data added successfully!")

if __name__ == "__main__":
    init_db()
    add_sample_data()
