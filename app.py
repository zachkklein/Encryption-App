from flask import Flask, request, render_template
import random
import html

app = Flask(__name__)

emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "🙃", "😉",
          "😌", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "😜", "🤪", "🤨",
          "🧐", "🤓", "😎", "🤩", "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️",
          "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳",
          "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "🤥", "😶",
          "😐", "😑", "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪",
          "😵", "🤐", "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈", "👿",
          "👹", "👺", "🤡", "💩", "👻", "💀", "☠️", "👽", "👾", "🤖", "🎃", "😺", "😸",
          "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🤲", "👐", "🙌", "👏", "🤝", "👍",
          "👎", "👊", "✊", "🤛", "🤜", "🤞", "✌️", "🤟", "🤘", "👌", "👈", "👉", "👆",
          "👇", "☝️", "✋", "🤚", "🖐", "🖖", "👋", "🤙", "💪", "🦾", "🖕", "✍️", "👏",
          "🙌", "👐", "🤲", "🤝", "🙏", "✍️", "💅", "🤳", "💪", "🦵", "🦶", "👂", "🦻",
          "👃", "🧠", "🦷", "🦴", "👀", "👁", "👅", "👄"]

characters = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",",
    "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\",
    "^", "_", "`", "{", "|", "}", "~"]

def assign_emojis():
    emoji_dictionary = {}
    random.shuffle(emojis)
    for i, char in enumerate(characters):
        emoji_dictionary[char] = emojis[i]
    return emoji_dictionary

emoji_dictionary = assign_emojis()

def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char in characters:
            shifted_index = (characters.index(char) + shift) % len(characters)
            encrypted_text += characters[shifted_index]
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char in characters:
            shifted_index = (characters.index(char) - shift) % len(characters)
            decrypted_text += characters[shifted_index]
        else:
            decrypted_text += char
    return decrypted_text

def translate_text(text, emoji_password):
    shift = len(emoji_password)
    encrypted_text = caesar_encrypt(text, shift)
    translated_text = ""
    for char in encrypted_text:
        if char in emoji_dictionary:
            translated_text += emoji_dictionary[char]
        else:
            translated_text += char
    return translated_text, shift

def reverse_translate_text(text, emoji_password, shift):
    reverse_emoji_dictionary = {v: k for k, v in emoji_dictionary.items()}
    translated_text = ""
    for char in text:
        if char in reverse_emoji_dictionary:
            translated_text += reverse_emoji_dictionary[char]
        else:
            translated_text += char
    decrypted_text = caesar_decrypt(translated_text, shift)
    return decrypted_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action'] == 'Encrypt':
            plaintext = request.form['plaintext']
            emoji_password = html.unescape(request.form['emoji_password'])
            encrypted_text, shift = translate_text(plaintext, emoji_password)
            decrypted_text = ""
        else:
            encrypted_text = request.form['encrypted_text']
            emoji_password = html.unescape(request.form['emoji_password'])
            shift = int(request.form['shift'])
            decrypted_text = reverse_translate_text(encrypted_text, emoji_password, shift)
            plaintext = ""
    else:
        plaintext = ""
        encrypted_text = ""
        decrypted_text = ""
        emoji_password = ""
        shift = 0

    return render_template('index.html', plaintext=plaintext, encrypted_text=encrypted_text,
                           decrypted_text=decrypted_text, emoji_password=emoji_password, shift=shift)

if __name__ == '__main__':
    app.run(debug=True)
