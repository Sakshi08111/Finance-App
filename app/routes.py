from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Transaction, db
from werkzeug.security import check_password_hash
from .forms import IncomeForm, ExpenseForm

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

# Home Route
@routes.route('/')
def home():
    return render_template('home.html')

# Auth Route (Login and Register)
@routes.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        # Handle login
        if 'login' in request.form:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('routes.home'))
            else:
                flash('Invalid email or password.', 'error')
        # Handle registration
        elif 'register' in request.form:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', 'error')
            else:
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('routes.auth'))
    return render_template('auth.html')

# Logout Route
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.home'))

# Add Income Route
@routes.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        # Process the form data and save to the database
        transaction = Transaction(
            title=form.title.data,
            amount=form.amount.data,
            date=form.date.data,
            type='income',
            source=form.source.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Income added successfully!', 'success')
        return redirect(url_for('routes.view_transactions'))
    return render_template('add_income.html', form=form)

# Add Expense Route
@routes.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        # Process the form data and save to the database
        transaction = Transaction(
            title=form.title.data,
            amount=form.amount.data,
            date=form.date.data,
            type='expense',
            category=form.category.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('routes.view_transactions'))
    return render_template('add_expense.html', form=form)

# View Transactions Route
@routes.route('/transactions')
@login_required
def view_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=transactions)

# Forecast & Insights Route
@routes.route('/forecast_insights', methods=['GET', 'POST'])
@login_required
def forecast_insights():
    insights = []
    forecasted_income = None
    forecasted_expenses = None
    forecasted_savings = None
    forecast_period = 6  # Default forecast period

    if request.method == 'POST':
        try:
            # Get user input
            forecast_period = int(request.form.get('forecast_period', 6))
            expected_income = float(request.form.get('expected_income', 0))
            expected_expenses = float(request.form.get('expected_expenses', 0))

            # Fetch historical data
            transactions = Transaction.query.filter_by(user_id=current_user.id).all()

            # Calculate averages
            total_income = sum(t.amount for t in transactions if t.amount > 0)
            total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
            num_months = len({t.date.strftime('%Y-%m') for t in transactions})

            avg_income = total_income / num_months if num_months > 0 else 0
            avg_expenses = total_expenses / num_months if num_months > 0 else 0

            # Calculate forecasted values
            forecasted_income = (expected_income if expected_income > 0 else avg_income) * forecast_period
            forecasted_expenses = (expected_expenses if expected_expenses > 0 else avg_expenses) * forecast_period
            forecasted_savings = forecasted_income - forecasted_expenses

            # Generate insights
            if forecasted_expenses > forecasted_income:
                insights.append("Your expenses exceed your income. Consider reducing unnecessary spending.")
            if forecasted_savings > 0:
                insights.append(f"You are projected to save ${forecasted_savings:,.2f} over the next {forecast_period} months. Great job!")
            if not insights:
                insights.append("Your finances are balanced. Keep up the good work!")

        except Exception as e:
            print("Error in forecast_insights route:", str(e))
            flash('An error occurred while generating the forecast and insights.', 'error')

    return render_template(
        'forecast_insights.html',
        forecast_period=forecast_period,
        forecasted_income=forecasted_income,
        forecasted_expenses=forecasted_expenses,
        forecasted_savings=forecasted_savings,
        insights=insights
    )

# Edit Transaction Route
@routes.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to edit this transaction.', 'error')
        return redirect(url_for('routes.view_transactions'))

    if transaction.type == 'income':
        form = IncomeForm(obj=transaction)
    else:
        form = ExpenseForm(obj=transaction)

    if form.validate_on_submit():
        transaction.title = form.title.data
        transaction.amount = abs(form.amount.data) if transaction.type == 'income' else -abs(form.amount.data)
        transaction.date = form.date.data
        if transaction.type == 'income':
            transaction.source = form.source.data
        else:
            transaction.category = form.category.data
        transaction.description = form.description.data
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('routes.view_transactions'))

    return render_template('edit_transaction.html', form=form, transaction_type=transaction.type)

# Delete Transaction Route
@routes.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.', 'error')
        return redirect(url_for('routes.view_transactions'))

    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('routes.view_transactions'))

# Add Transaction Route
@routes.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        title = request.form.get('title')
        amount = float(request.form.get('amount'))
        date = request.form.get('date')
        type = request.form.get('type')
        source = request.form.get('source', '')
        category = request.form.get('category', '')
        description = request.form.get('description', '')

        # Create a new transaction
        new_transaction = Transaction(
            title=title,
            amount=amount,
            date=date,
            type=type,
            source=source,
            category=category,
            description=description,
            user_id=current_user.id
        )
        db.session.add(new_transaction)
        db.session.commit()

        flash('Transaction added successfully!', 'success')
        return redirect(url_for('routes.view_transactions'))

    return render_template('add_transaction.html')