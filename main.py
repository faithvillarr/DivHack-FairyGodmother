# Our main Flask file.
from db_management import get_clothing_names, grab_closet_urls, upload_clothing_image
from flask import Flask, render_template, redirect, url_for, session, request

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

@app.route('/upload_clothing', methods=['POST'])
def upload_clothing():
    if 'fileInput' not in request.files:
        return redirect(request.url)

    file = request.files['fileInput']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filepath = upload_clothing_image(file_path, username, clothing_type)
        file.save(filepath)
        # Optionally store the URL in session or database for future display
        session['closet_urls'].append(url_for('static', filename=f'uploads/{file.filename}'))
    
    return redirect(url_for('outfit_board'))

if __name__ == '__main__':
    app.run(debug=True)

