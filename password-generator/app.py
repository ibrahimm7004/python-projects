from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "}", "[", "]", "|", ";", ":", "'", "<", ">", "?", "~", "/"]
    
    password = ""
    for x in range(0, random.randint(6, 12)):
        chosen_list = random.randint(1, 3)
        if chosen_list == 1:
            password += random.choice(letters)
        elif chosen_list == 2:
            password += random.choice(numbers)
        elif chosen_list == 3:
            password += random.choice(symbols)
    
    return render_template('index.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)
