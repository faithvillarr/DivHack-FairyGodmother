# Our main Flask file.
from db_management import get_clothing_names, grab_closet_urls
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Set variables to be changed if we get to sessions
urls = []

@app.route('/')
def root():
    session['username'] = 'janedoe'
    urls = grab_closet_urls(session['username'])
    session['closet_urls'] = urls
    return redirect(url_for('outfit_board'))

@app.route('/outfitboard')
def outfit_board():
    return render_template('outfitboard.html')

@app.route('/outfitupload')
def main():
    return render_template('outfitupload.html')

if __name__ == '__main__':
    app.run(debug=True)

