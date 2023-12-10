from flask import Flask, render_template
from scrape import scrape_data

app = Flask(__name__)

@app.route('/')
def home():
    scraped_data = scrape_data()
    return render_template('index.html', data=scraped_data)

if __name__ == '__main__':
    app.run(debug=True)
