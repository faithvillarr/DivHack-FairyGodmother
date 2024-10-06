# Our main Flask file.

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('outfit_board'))

@app.route('/outfitboard')
def outfit_board():
    return render_template('outfitboard.html')

@app.route('/outfitupload')
def main():
    return render_template('outfitupload.html')

if __name__ == '__main__':
    app.run(debug=True)


