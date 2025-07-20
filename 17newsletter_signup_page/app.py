from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory subscriber list
subscribers = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    date = datetime.now().strftime('%Y-%m-%d')

    subscriber = {
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'date': date
    }
    subscribers.append(subscriber)
    return redirect(url_for('thank_you', name=name))

@app.route('/thankyou')
def thank_you():
    name = request.args.get('name', 'Subscriber')
    return render_template('thankyou.html', name=name)

@app.route('/subscribers')
def subscriber_list():
    date_filter = request.args.get('date')
    if date_filter:
        filtered = [s for s in subscribers if s['date'] == date_filter]
    else:
        filtered = subscribers
    dates = sorted(set(s['date'] for s in subscribers))
    return render_template('subscribers.html', subscribers=filtered, dates=dates, selected_date=date_filter)

if __name__ == '__main__':
    app.run(debug=True)
