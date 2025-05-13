from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from database import init_db, db_session
from models import Book, Member, Loan
from datetime import datetime, timedelta
from sqlalchemy import desc

import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(16)  # Secure secret key for production

# Initialize database
init_db()

@app.route('/')
def dashboard():
    search_query = request.args.get('search', '')
    if search_query:
        books = Book.query.filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Book.author.ilike(f'%{search_query}%')) |
            (Book.isbn.ilike(f'%{search_query}%'))
        ).all()
    else:
        books = Book.query.all()
    return render_template('dashboard.html', books=books, search_query=search_query)

@app.route('/api/search/books')
def search_books():
    search_query = request.args.get('q', '')
    books = Book.query.filter(
        (Book.title.ilike(f'%{search_query}%')) |
        (Book.author.ilike(f'%{search_query}%')) |
        (Book.isbn.ilike(f'%{search_query}%'))
    ).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'available': book.available,
        'cover_image': book.cover_image
    } for book in books])

@app.route('/api/search/members')
def search_members():
    search_query = request.args.get('q', '')
    members = Member.query.filter(
        (Member.name.ilike(f'%{search_query}%')) |
        (Member.email.ilike(f'%{search_query}%'))
    ).all()
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'email': member.email,
        'join_date': member.join_date.strftime('%Y-%m-%d'),
        'active_loans': len([loan for loan in member.loans if loan.return_date is None])
    } for member in members])

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404)
    # Get loans sorted by date
    loans = Loan.query.filter_by(book_id=book_id).order_by(desc(Loan.loan_date)).all()
    return render_template('book_detail.html', book=book, loans=loans)

@app.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404)
    
    if request.method == 'POST':
        try:
            book.title = request.form['title']
            book.author = request.form['author']
            book.isbn = request.form['isbn']
            book.publish_date = datetime.strptime(request.form['publish_date'], '%Y-%m-%d')
            book.description = request.form['description']
            book.cover_image = request.form.get('cover_image', book.cover_image)
            
            db_session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('book_detail', book_id=book_id))
        except Exception as e:
            db_session.rollback()
            flash(f'Error updating book: {str(e)}', 'error')
    
    return render_template('edit_book.html', book=book)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        member = Member.query.filter_by(email=email).first()
        if member:
            session['member_id'] = member.id
            session['member_name'] = member.name
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email address.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/book/<int:book_id>/loan', methods=['GET', 'POST'])
def loan_book(book_id):
    if 'member_id' not in session:
        flash('Please log in to borrow a book.', 'error')
        return redirect(url_for('login', next=url_for('loan_book', book_id=book_id)))

    book = Book.query.get(book_id)
    if book is None:
        abort(404)
    
    if not book.available:
        flash('This book is already borrowed.', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    if request.method == 'POST':
        due_date_str = request.form.get('due_date')
        print(f"Received form data - due_date: {due_date_str}")
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            print(f"Parsed due_date: {due_date}")
        except Exception as e:
            print(f"Error parsing due_date: {str(e)}")
            flash('Invalid due date format.', 'error')
            return redirect(url_for('loan_book', book_id=book_id))
        
        member_id = session['member_id']
        
        try:
            # Create new loan
            loan = Loan(
                book_id=book_id,
                member_id=member_id,
                loan_date=datetime.now(),
                due_date=due_date,
                return_date=None  # Will be set when book is returned
            )
            # Update book availability
            book.available = False
            
            db_session.add(loan)
            db_session.commit()
            
            flash('Book loaned successfully!', 'success')
            return redirect(url_for('book_detail', book_id=book_id))
        except Exception as e:
            db_session.rollback()
            flash(f'Error processing loan: {str(e)}', 'error')
            return redirect(url_for('loan_book', book_id=book_id))
    
    return render_template('loan_book.html', book=book)

@app.route('/book/<int:book_id>/return')
def return_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404)
    
    if book.available:
        flash('This book is already returned.', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    try:
        # Find the active loan for this book
        active_loan = Loan.query.filter_by(
            book_id=book_id,
            return_date=None
        ).first()
        
        if active_loan:
            active_loan.return_date = datetime.now()
            book.available = True
            db_session.commit()
            flash('Book returned successfully!', 'success')
        else:
            flash('No active loan found for this book.', 'error')
            
    except Exception as e:
        db_session.rollback()
        flash(f'Error processing return: {str(e)}', 'error')
    
    return redirect(url_for('book_detail', book_id=book_id))

@app.route('/book/<int:book_id>/delete')
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404)
    
    try:
        db_session.delete(book)
        db_session.commit()
        flash('Book deleted successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db_session.rollback()
        flash(f'Error deleting book: {str(e)}', 'error')
        return redirect(url_for('book_detail', book_id=book_id))

@app.route('/book/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            # Parse the date string to datetime object
            publish_date = datetime.strptime(request.form['publish_date'], '%Y-%m-%d')
            
            book = Book(
                title=request.form['title'],
                author=request.form['author'],
                isbn=request.form['isbn'],
                publish_date=publish_date,
                description=request.form['description'],
                cover_image=request.form.get('cover_image', 'https://images.pexels.com/photos/1005324/literature-book-open-pages-1005324.jpeg'),
                available=True
            )
            db_session.add(book)
            db_session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db_session.rollback()
            flash(f'Error adding book: {str(e)}', 'error')
            return render_template('add_book.html')
    return render_template('add_book.html')

@app.route('/members')
def members():
    search_query = request.args.get('search', '')
    if search_query:
        members = Member.query.filter(
            (Member.name.ilike(f'%{search_query}%')) |
            (Member.email.ilike(f'%{search_query}%'))
        ).all()
    else:
        members = Member.query.all()
    return render_template('members.html', members=members, search_query=search_query)

@app.route('/member/<int:member_id>')
def member_detail(member_id):
    member = Member.query.get(member_id)
    if member is None:
        abort(404)
    now = datetime.now()
    return render_template('member_detail.html', member=member, now=now)

@app.route('/member/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.query.get(member_id)
    if member is None:
        abort(404)
    
    if request.method == 'POST':
        try:
            member.name = request.form['name']
            member.email = request.form['email']
            
            db_session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('member_detail', member_id=member_id))
        except Exception as e:
            db_session.rollback()
            flash(f'Error updating member: {str(e)}', 'error')
    
    return render_template('edit_member.html', member=member)

@app.route('/member/<int:member_id>/delete')
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member is None:
        abort(404)
    
    # Check if member has any active loans
    active_loans = Loan.query.filter_by(member_id=member_id, return_date=None).all()
    if active_loans:
        flash('Cannot delete member with active loans.', 'error')
        return redirect(url_for('member_detail', member_id=member_id))
    
    try:
        db_session.delete(member)
        db_session.commit()
        flash('Member deleted successfully!', 'success')
        return redirect(url_for('members'))
    except Exception as e:
        db_session.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
        return redirect(url_for('member_detail', member_id=member_id))

@app.route('/member/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        try:
            member = Member(
                name=request.form['name'],
                email=request.form['email'],
                join_date=datetime.now()
            )
            db_session.add(member)
            db_session.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('members'))
        except Exception as e:
            flash(f'Error adding member: {str(e)}', 'error')
    return render_template('add_member.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=False, port=8000)
