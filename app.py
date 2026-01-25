from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from config import MUSEUM_EMAIL, MUSEUM_EMAIL_PASSWORD

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

# Database configuration
db_path = os.path.join(os.path.dirname(__file__), 'museum_app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'


# News model
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<News {self.title}>'





# Exhibit model
class Exhibit(db.Model):
    __tablename__ = 'exhibits'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Exhibit {self.title}>'


# Event model
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    start = db.Column(db.String(5), nullable=True)  # HH:MM
    end = db.Column(db.String(5), nullable=True)    # HH:MM
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Event {self.title}>'


# Service model
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Service {self.title}>'


# Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref='bookings')
    event = db.relationship('Event', backref='bookings')


# User log model
class UserLog(db.Model):
    __tablename__ = 'user_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref='logs')





def log_action(user_id, action, details=None):
    try:
        ul = UserLog(user_id=user_id, action=action, details=details)
        db.session.add(ul)
        db.session.commit()
    except Exception:
        db.session.rollback()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/exhibits")
def exhibits():
    exhibits = Exhibit.query.order_by(Exhibit.created_at.desc()).all()
    return render_template("exhibits.html", exhibits=exhibits)

# Simple in-memory events data
events_data = [
    {
        "id": 1,
        "title": "Guided Museum Tour",
        "date": "2026-04-20",
        "start": "11:00",
        "end": "13:00",
        "description": "Join our expert guides for an in-depth tour of the permanent exhibition.",
    },
    {
        "id": 2,
        "title": "Ancient Art Workshop",
        "date": "2026-05-05",
        "start": "10:00",
        "end": "14:00",
        "description": "Hands-on workshop exploring ancient artistic techniques, suitable for students and adults.",
    },
    {
        "id": 3,
        "title": "Lecture: History of the Roman Empire",
        "date": "2026-05-18",
        "start": "18:00",
        "end": "20:00",
        "description": "A public lecture by university professors discussing key aspects of Roman civilization.",
    },
    {
        "id": 4,
        "title": "Family Day at the Museum",
        "date": "2026-03-02",
        "start": "09:00",
        "end": "17:00",
        "description": "A fun day with activities for children and families, including interactive exhibits.",
    },
    {
        "id": 5,
        "title": "Photography Exhibition Opening",
        "date": "2026-02-10",
        "start": "18:00",
        "end": "20:00",
        "description": "Opening ceremony of the temporary photography exhibition featuring modern artists.",
    },
    {
        "id": 6,
        "title": "Local Artists Meetup",
        "date": "2025-12-15",
        "start": "14:00",
        "end": "16:00",
        "description": "Community meetup showcasing local artists and their work.",
    },
]


def parse_event_end_dt(evt):
    # event date is YYYY-MM-DD, end is HH:MM
    return datetime.strptime(f"{evt['date']} {evt['end']}", "%Y-%m-%d %H:%M")


@app.route("/events")
def events():
    now = datetime.now()
    all_events = Event.query.order_by(Event.date.asc()).all()
    # split upcoming/past by end datetime
    upcoming = []
    past = []
    for e in all_events:
        try:
            end_dt = datetime.strptime(f"{e.date} {e.end}", "%Y-%m-%d %H:%M") if e.end else datetime.strptime(f"{e.date} 23:59", "%Y-%m-%d %H:%M")
        except Exception:
            end_dt = datetime.strptime(f"{e.date} 23:59", "%Y-%m-%d %H:%M")
        if end_dt >= now:
            upcoming.append(e)
        else:
            past.append(e)
    return render_template("events.html", upcoming_events=upcoming, past_events=past)

@app.route("/news")
def news():
    articles = News.query.order_by(News.created_at.desc()).all()
    return render_template("news.html", articles=articles)

@app.route("/services")
def services():
    services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template("services.html", services=services)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate form
        if not username or not email or not password or not confirm_password:
            flash("All fields are required.")
            return redirect(url_for("register"))
        
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken.")
            return redirect(url_for("register"))
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already registered.")
            return redirect(url_for("register"))
        
        # Create and save new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            log_action(new_user.id, "register", f"User registered: {new_user.username}")
            flash("Account created successfully. Please log in.")
            return redirect(url_for("login_view"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration.")
            return redirect(url_for("register"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Query user from database by username
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = user.is_admin
            log_action(user.id, "login", f"User logged in: {user.username}")
            flash(f"Logged in successfully as {user.username}.")
            next_url = request.args.get("next") or url_for("home")
            return redirect(next_url)
        else:
            flash("Invalid username or password.")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    uid = session.get("user_id")
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    log_action(uid, "logout", "User logged out")
    flash("Logged out.")
    return redirect(url_for("home"))





@app.route("/events/book/<int:event_id>")
def book_event(event_id):
    # Use DB-backed Event
    evt = Event.query.get(event_id)
    if not evt:
        flash("Event not found.")
        return redirect(url_for("events"))

    # If not logged in, redirect to login with next
    if not session.get("user_id"):
        return redirect(url_for("login_view", next=url_for("book_event", event_id=event_id)))

    now = datetime.now()
    try:
        end_dt = datetime.strptime(f"{evt.date} {evt.end}", "%Y-%m-%d %H:%M") if evt.end else datetime.strptime(f"{evt.date} 23:59", "%Y-%m-%d %H:%M")
    except Exception:
        end_dt = datetime.strptime(f"{evt.date} 23:59", "%Y-%m-%d %H:%M")

    if now > end_dt:
        flash("You can't attend the event because it's over.")
        return redirect(url_for("events"))

    # Persist booking
    try:
        booking = Booking(user_id=session.get("user_id"), event_id=evt.id)
        db.session.add(booking)
        db.session.commit()
        log_action(session.get("user_id"), "booking_created", f"Booking id={booking.id} event={evt.title}({evt.id})")
        flash(f"Booking confirmed for '{evt.title}'.")
    except Exception:
        db.session.rollback()
        flash("An error occurred creating your booking.")

    return redirect(url_for("events"))


# Admin helper function
def is_admin():
    return session.get("is_admin", False) and session.get("user_id")


# Admin Dashboard
@app.route("/admin")
def admin_dashboard():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    users_count = User.query.count()
    
    return render_template("admin/dashboard.html", 
                         users_count=users_count)


@app.route('/admin/logs')
def admin_logs():
    if not is_admin():
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    logs = UserLog.query.order_by(UserLog.created_at.desc()).limit(500).all()
    return render_template('admin/user_logs.html', logs=logs)


# Admin: Manage Users
@app.route("/admin/users")
def admin_users():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
def admin_delete_user(user_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    if user_id == session.get("user_id"):
        flash("You cannot delete your own account.")
        return redirect(url_for("admin_users"))
    
    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for("admin_users"))
    
    try:
        db.session.delete(user)
        db.session.commit()
        log_action(session.get("user_id"), "user_delete", f"Deleted user id={user.id} username={user.username}")
        flash(f"User '{user.username}' deleted successfully.")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting user.")
    
    return redirect(url_for("admin_users"))


# Admin: Manage News
@app.route("/admin/news")
def admin_news():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    news = News.query.all()
    return render_template("admin/news.html", news=news)


@app.route("/admin/news/add", methods=["GET", "POST"])
def admin_add_news():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        if not title or not content:
            flash("Title and content are required.")
            return redirect(url_for("admin_add_news"))
        
        new_news = News(title=title, content=content, created_by=session.get("user_id"))
        try:
            db.session.add(new_news)
            db.session.commit()
            log_action(session.get("user_id"), "news_add", f"News id={new_news.id} title={new_news.title}")
            flash("News added successfully.")
            return redirect(url_for("admin_news"))
        except Exception as e:
            db.session.rollback()
            flash("Error adding news.")
    
    return render_template("admin/add_news.html")


@app.route("/admin/news/edit/<int:news_id>", methods=["GET", "POST"])
def admin_edit_news(news_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    news = News.query.get(news_id)
    if not news:
        flash("News not found.")
        return redirect(url_for("admin_news"))
    
    if request.method == "POST":
        news.title = request.form.get("title")
        news.content = request.form.get("content")
        
        if not news.title or not news.content:
            flash("Title and content are required.")
            return redirect(url_for("admin_edit_news", news_id=news_id))
        
        try:
            db.session.commit()
            log_action(session.get("user_id"), "news_edit", f"News id={news.id} title={news.title}")
            flash("News updated successfully.")
            return redirect(url_for("admin_news"))
        except Exception as e:
            db.session.rollback()
            flash("Error updating news.")
    
    return render_template("admin/edit_news.html", news=news)


@app.route("/admin/news/delete/<int:news_id>", methods=["POST"])
def admin_delete_news(news_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    
    news = News.query.get(news_id)
    if not news:
        flash("News not found.")
        return redirect(url_for("admin_news"))
    
    try:
        db.session.delete(news)
        db.session.commit()
        log_action(session.get("user_id"), "news_delete", f"News id={news.id} title={news.title}")
        flash("News deleted successfully.")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting news.")
    
    return redirect(url_for("admin_news"))





# Admin: Manage Exhibits
@app.route("/admin/exhibits")
def admin_exhibits():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    exhibits = Exhibit.query.order_by(Exhibit.created_at.desc()).all()
    return render_template("admin/exhibits.html", exhibits=exhibits)


@app.route("/admin/exhibits/add", methods=["GET", "POST"])
def admin_add_exhibit():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        if not title:
            flash("Title is required.")
            return redirect(url_for("admin_add_exhibit"))
        ex = Exhibit(title=title, description=description, created_by=session.get("user_id"))
        try:
            db.session.add(ex)
            db.session.commit()
            log_action(session.get("user_id"), "exhibit_add", f"Exhibit id={ex.id} title={ex.title}")
            flash("Exhibit added successfully.")
            return redirect(url_for("admin_exhibits"))
        except Exception:
            db.session.rollback()
            flash("Error adding exhibit.")
    return render_template("admin/add_exhibit.html")


@app.route("/admin/exhibits/edit/<int:exhibit_id>", methods=["GET", "POST"])
def admin_edit_exhibit(exhibit_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    ex = Exhibit.query.get(exhibit_id)
    if not ex:
        flash("Exhibit not found.")
        return redirect(url_for("admin_exhibits"))
    if request.method == "POST":
        ex.title = request.form.get("title")
        ex.description = request.form.get("description")
        if not ex.title:
            flash("Title is required.")
            return redirect(url_for("admin_edit_exhibit", exhibit_id=exhibit_id))
        try:
            db.session.commit()
            log_action(session.get("user_id"), "exhibit_edit", f"Exhibit id={ex.id} title={ex.title}")
            flash("Exhibit updated successfully.")
            return redirect(url_for("admin_exhibits"))
        except Exception:
            db.session.rollback()
            flash("Error updating exhibit.")
    return render_template("admin/edit_exhibit.html", exhibit=ex)


@app.route("/admin/exhibits/delete/<int:exhibit_id>", methods=["POST"])
def admin_delete_exhibit(exhibit_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    ex = Exhibit.query.get(exhibit_id)
    if not ex:
        flash("Exhibit not found.")
        return redirect(url_for("admin_exhibits"))
    try:
        db.session.delete(ex)
        db.session.commit()
        log_action(session.get("user_id"), "exhibit_delete", f"Exhibit id={ex.id} title={ex.title}")
        flash("Exhibit deleted.")
    except Exception:
        db.session.rollback()
        flash("Error deleting exhibit.")
    return redirect(url_for("admin_exhibits"))


# Admin: Manage Events
@app.route("/admin/events")
def admin_events():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template("admin/events.html", events=events)


@app.route("/admin/events/add", methods=["GET", "POST"])
def admin_add_event():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    if request.method == "POST":
        title = request.form.get("title")
        date = request.form.get("date")
        start = request.form.get("start")
        end = request.form.get("end")
        description = request.form.get("description")
        if not title or not date:
            flash("Title and date are required.")
            return redirect(url_for("admin_add_event"))
        ev = Event(title=title, date=date, start=start, end=end, description=description, created_by=session.get("user_id"))
        try:
            db.session.add(ev)
            db.session.commit()
            log_action(session.get("user_id"), "event_add", f"Event id={ev.id} title={ev.title}")
            flash("Event added successfully.")
            return redirect(url_for("admin_events"))
        except Exception:
            db.session.rollback()
            flash("Error adding event.")
    return render_template("admin/add_event.html")


@app.route("/admin/events/edit/<int:event_id>", methods=["GET", "POST"])
def admin_edit_event(event_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    ev = Event.query.get(event_id)
    if not ev:
        flash("Event not found.")
        return redirect(url_for("admin_events"))
    if request.method == "POST":
        ev.title = request.form.get("title")
        ev.date = request.form.get("date")
        ev.start = request.form.get("start")
        ev.end = request.form.get("end")
        ev.description = request.form.get("description")
        if not ev.title or not ev.date:
            flash("Title and date are required.")
            return redirect(url_for("admin_edit_event", event_id=event_id))
        try:
            db.session.commit()
            log_action(session.get("user_id"), "event_edit", f"Event id={ev.id} title={ev.title}")
            flash("Event updated successfully.")
            return redirect(url_for("admin_events"))
        except Exception:
            db.session.rollback()
            flash("Error updating event.")
    return render_template("admin/edit_event.html", event=ev)


@app.route("/admin/events/delete/<int:event_id>", methods=["POST"])
def admin_delete_event(event_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    ev = Event.query.get(event_id)
    if not ev:
        flash("Event not found.")
        return redirect(url_for("admin_events"))
    try:
        db.session.delete(ev)
        db.session.commit()
        log_action(session.get("user_id"), "event_delete", f"Event id={ev.id} title={ev.title}")
        flash("Event deleted.")
    except Exception:
        db.session.rollback()
        flash("Error deleting event.")
    return redirect(url_for("admin_events"))


# Admin: Manage Services
@app.route("/admin/services")
def admin_services():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template("admin/services.html", services=services)


@app.route("/admin/services/add", methods=["GET", "POST"])
def admin_add_service():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        if not title:
            flash("Title is required.")
            return redirect(url_for("admin_add_service"))
        s = Service(title=title, description=description, created_by=session.get("user_id"))
        try:
            db.session.add(s)
            db.session.commit()
            log_action(session.get("user_id"), "service_add", f"Service id={s.id} title={s.title}")
            flash("Service added successfully.")
            return redirect(url_for("admin_services"))
        except Exception:
            db.session.rollback()
            flash("Error adding service.")
    return render_template("admin/add_service.html")


@app.route("/admin/services/edit/<int:service_id>", methods=["GET", "POST"])
def admin_edit_service(service_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    s = Service.query.get(service_id)
    if not s:
        flash("Service not found.")
        return redirect(url_for("admin_services"))
    if request.method == "POST":
        s.title = request.form.get("title")
        s.description = request.form.get("description")
        if not s.title:
            flash("Title is required.")
            return redirect(url_for("admin_edit_service", service_id=service_id))
        try:
            db.session.commit()
            log_action(session.get("user_id"), "service_edit", f"Service id={s.id} title={s.title}")
            flash("Service updated successfully.")
            return redirect(url_for("admin_services"))
        except Exception:
            db.session.rollback()
            flash("Error updating service.")
    return render_template("admin/edit_service.html", service=s)


@app.route("/admin/services/delete/<int:service_id>", methods=["POST"])
def admin_delete_service(service_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    s = Service.query.get(service_id)
    if not s:
        flash("Service not found.")
        return redirect(url_for("admin_services"))
    try:
        db.session.delete(s)
        db.session.commit()
        log_action(session.get("user_id"), "service_delete", f"Service id={s.id} title={s.title}")
        flash("Service deleted.")
    except Exception:
        db.session.rollback()
        flash("Error deleting service.")
    return redirect(url_for("admin_services"))


# Admin: View Bookings
@app.route("/admin/bookings")
def admin_bookings():
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    bookings = Booking.query.order_by(Booking.booked_at.desc()).all()
    return render_template("admin/bookings.html", bookings=bookings)


@app.route("/admin/bookings/delete/<int:booking_id>", methods=["POST"])
def admin_delete_booking(booking_id):
    if not is_admin():
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    b = Booking.query.get(booking_id)
    if not b:
        flash("Booking not found.")
        return redirect(url_for("admin_bookings"))
    try:
        db.session.delete(b)
        db.session.commit()
        flash("Booking deleted.")
    except Exception:
        db.session.rollback()
        flash("Error deleting booking.")
    return redirect(url_for("admin_bookings"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
