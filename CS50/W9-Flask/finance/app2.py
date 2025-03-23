import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_data = {
        'cash': db.execute("SELECT cash FROM users WHERE id=?",
                           session.get("user_id"))[0]['cash'],
        'stocks': db.execute("""SELECT symbol, sum(num_shares) as count
                                FROM purchases WHERE user_id=?
                                GROUP BY symbol;""", session.get("user_id")),
        'total_holdings': 0
    }
    for stock in user_data['stocks']:
        stock_data = lookup(stock['symbol'])
        stock_holding = round(stock_data['price'] * stock['count'], 2)
        user_data['total_holdings'] += stock_holding
        stock.setdefault('name', stock_data['name'])
        stock.setdefault('price', stock_data['price'])
        stock.setdefault('holding', stock_holding)
    print(user_data)
    return render_template("index.html", user=user_data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if request.method == "POST":
        # Ensure symbol and shares are entered and shares is an positive int.
        if not symbol:
            return apology("A symbol must be entered.")
        if not shares:
            return apology("The number of shares must be entered.")
        elif not shares.isdecimal() or int(shares) < 1:
            return apology("The number of shares must be a positive integer")

        # Look up symbol using IEX, return apology if symbol doesn't exist.
        try:
            stock_price = lookup(symbol)['price']
        except KeyError:
            # Symbol not on IEX data.
            return apology("Symbol invalid.", 403)
        total_cost = int(shares) * stock_price
        # Select the amount of cash the user has
        cash = db.execute("SELECT cash FROM users WHERE id=?",
                                session.get("user_id"))[0]['cash']
        if total_cost > cash:
            return apology(f"Cost ({total_cost}) greater than cash"
                           f" available ({cash})")
        # Add purchase to database
        db.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                num_shares INTEGER NOT NULL,
                price_per_share TEXT NOT NULL,
                date_time TEXT NOT NULL,
                uid TEXT GENERATE ALWAYS AS
                    (CAST(user_id AS TEXT) ||"-"|| date_time) STORED
                        UNIQUE ON CONFLICT FAIL
                );""")
        db.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS uid ON purchases(uid);""")
        db.execute(
            """CREATE INDEX IF NOT EXISTS user_id ON purchases(user_id);""")
        db.execute("""INSERT INTO purchases(
                   user_id, symbol, num_shares, price_per_share, date_time)
                   VALUES(?, ?, ?, ?, ?);""", session.get("user_id"), symbol,
                   shares, stock_price, datetime.datetime.today())
        # Update user's available cash
        db.execute("UPDATE users SET cash=? WHERE user_id=?",
                   (cash - total_cost), session.get('user_id'))
        return render_template("buy.html")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id=? ORDERED BY dt DESC;",
        session.get('user_id'))
    print(transactions[0])
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if (len(rows) != 1
                or not check_password_hash(rows[0]["hash"],
                                           request.form.get("password"))):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("A symbol must be entered.", 403)
        # Look up symbol using IEX
        try:
            stock_data = lookup(request.form.get("symbol"))
        except KeyError:
            # Symbol not on IEX data.
            return apology("Symbol invalid.", 403)
        print(stock_data)
        return render_template("quoted.html", stock_data=stock_data)
    else:
        # Render the quote page
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get form field context.
        username = request.form.get('username')
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")

        # Ensure username field is completed
        if not username:
            return apology("Username is required.", 403)

        # Ensure password is provided
        if not password:
            return apology("Password is required.", 403)

        # Ensure confirmation field completed
        if not password_confirm:
            return apology("Password is required.", 403)

        # Ensure password and confirmation matches.
        if not password_confirm == password:
            return apology("Passwords do not match.", 403)
        try:
            # Register user into database and hash password
            # [ ] Add initial transaction of 10,000 cash added
            db.execute(
                "INSERT OR FAIL INTO users (username, hash) VALUES(?, ?);",
                username, generate_password_hash(password))
        except ValueError:
            return apology("Username must be unique.", 403)
        return render_template("register.html", success=True)
    else:
        # Render the register page.
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbol = request.form.get('symbol')
    shares = request.form.get('shares')
    if request.method == "POST":
        user_id = session.get('user_id')
        if not symbol:
            return apology("Symbol must be selected")
        if not shares.isdecimal and int(shares) > 0:
            return apology(
                "The number of shares must be an integer greater than zero.")
        # Convert the number of shares to an integer
        shares = int(shares)
        # Obtain owned stocks
        stocks_owned = {stock['symbol']: int(stock['count']) for stock in db.
                        execute("""SELECT symbol, sum(num_shares) as count
                                   FROM purchases WHERE user_id=?
                                   GROUP BY symbol;""", user_id)}
        if symbol not in stocks_owned:
            return apology('The symbol selected must be an owned stock')
        # Obtain the number of stocks owned for stock matching symbol entered.
        num_owned = stocks_owned[symbol]
        if shares > num_owned:
            return apology('Cannot sell more stock than owned.')
        # Obtain stock price and calculate money gained from sale
        share_price = lookup(symbol)['price']
        money_gained = share_price * shares
        # Update table
        db.execute("""INSERT INTO purchases(
                   user_id, symbol, num_shares, price_per_share, date_time)
                   VALUES(?, ?, ?, ?, ?);""", user_id, symbol, shares * -1,
                   share_price, datetime.datetime.today())
        db.execute("UPDATE users SET cash=? WHERE id=?;",
                   (db.execute("SELECT cash FROM users WHERE id=?;",
                               user_id)[0]['cash']
                    + money_gained),
                   user_id)
        return redirect('/')
    else:
        stocks = db.execute("""SELECT symbol FROM purchases WHERE user_id=?
                               GROUP BY symbol;""", session.get("user_id"))
    return render_template("sell.html", stocks=stocks)
