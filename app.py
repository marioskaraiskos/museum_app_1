from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/exhibits")
def exhibits():
    return render_template("exhibits.html")

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
    upcoming = [e for e in events_data if parse_event_end_dt(e) >= now]
    past = [e for e in events_data if parse_event_end_dt(e) < now]
    return render_template("events.html", upcoming_events=upcoming, past_events=past)

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # prototype – no database yet
        return redirect(url_for("home"))
    return render_template("contact.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        email = request.form.get("email")
        # prototype authentication: accept any email
        session["user"] = email
        flash("Logged in successfully.")
        next_url = request.args.get("next") or url_for("home")
        return redirect(next_url)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out.")
    return redirect(url_for("home"))

@app.route("/events/book/<int:event_id>")
def book_event(event_id):
    # Find event
    evt = next((e for e in events_data if e["id"] == event_id), None)
    if not evt:
        flash("Event not found.")
        return redirect(url_for("events"))

    # If not logged in, redirect to login with next
    if not session.get("user"):
        return redirect(url_for("login_view", next=url_for("book_event", event_id=event_id)))

    now = datetime.now()
    end_dt = parse_event_end_dt(evt)
    if now > end_dt:
        flash("You can't attend the event because it's over.")
        return redirect(url_for("events"))

    # booking successful (prototype - no database)
    bookings = session.get("bookings", [])
    bookings.append({"event_id": event_id, "title": evt["title"], "booked_at": now.isoformat()})
    session["bookings"] = bookings
    flash(f"Booking confirmed for '{evt['title']}'.")
    return redirect(url_for("events"))
if __name__ == "__main__":
    app.run(debug=True)
