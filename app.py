from flask import *

app = Flask(__name__)


def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text


def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        shift = int(request.form['shift'])
        if request.form['action'] == 'encrypt':
            encrypted_text = caesar_encrypt(plaintext, shift)
        else:
            encrypted_text = caesar_decrypt(plaintext, shift)

    else:
        plaintext = ""
        encrypted_text = ""
        shift = 3
    return render_template('index.html', plaintext=plaintext, encrypted_text=encrypted_text, shift=shift)


if __name__ == '__main__':
    app.run(debug=True)
