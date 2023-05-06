from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from playsound import playsound
from random import randint
import json

app = Flask(__name__)

# List of simple words kindergartners should be learning
words = [ 'apple', 'ball', 'cat', 'dog', 'fish', 'play', 'green', 'blue', 'orange', 
        'down', 'up', 'sad', 'happy', 'brown', 'his', 'her', 'mine', 'myself', 'cool',
        'nice', 'mom', 'dad', 'sister', 'brother', 'pretty', 'please', 'thanks', 'new', 
        'like', 'car', 'phone', 'school', 'teacher', 'friend', 'fun', 'run', 'jump', 'walk',
        'movie', 'smarter', 'beautiful', 'happier', 'impressive', 'up', 'short', 'to', 'mile', 
        'speaking', 'following', 'video', 'internet', 'artificial', 'emotions', 'basketball'
        'football', 'novel', 'understand', 'technology', 'student', 'association', 'midnight', 'neighbor',
        'hi', 'far', 'cat', 'fat', 'fee', 'tie', 'she', 'car', 'play', 'confirm', 'tap', 'hydrogen', 'oxygen',
        'biology', 'russian', 'us', 'would', 'could', 'should', 'can', 'will', 'may', 'might', 'must', 
        'shall', 'ought', 'need', 'dare', 'used', 'to', 'be', 'am', 'is', 'are', 'was', 'were', 'being'
        'apparent', 'diminish', 'controversy', 'frigid', 'flammable', 'chronological', 'impair',
        'waver', 'sufficient', 'symbol', 'unique', 'variable', 'widespread', 'youth', 'zeal', 'zest',
        'attach', 'whisper', 'neighbor', 'cities', 'common', 'divide', 'multiply' ] 
random_index = 0
lower_bounds = 2
upper_bounds = 3

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Clicks button to speak a random word
@app.route('/play-sound', methods=['POST'])
def play_sound():
    global random_index 
    random_index = randint(0, len(words) - 1)
    while lower_bounds > len(words[random_index]) or upper_bounds < len(words[random_index]):
        random_index = randint(0, len(words) - 1)
    
    print(str(random_index))
    tts = gTTS(text=words[random_index], lang='en')
    
    filename = 'sounds/' + words[random_index] + '.mp3'
    tts.save(filename)
    playsound(filename)
    
    return jsonify({'word': words[random_index]})

# Checks if user input matches the random word
@app.route('/check-word', methods=['POST'])
def check_word():
    word = request.form['word'].lower()
    print(str(random_index))
    result = False
    if word == words[random_index]:
        message = 'Correct!'
        
        tts = gTTS(text=message, lang='en')
        filename = 'sounds/correct.mp3'
        tts.save(filename)
        playsound(filename)
        playsound("sounds/fanfare-effect.mp3")
        
        result = True
    else:
        message = 'Incorrect. Try again.'
        
        tts = gTTS(text=message, lang='en')
        filename = 'sounds/incorrect.mp3'
        tts.save(filename)
        playsound(filename)
        playsound("sounds/wah-wah-wah-wah-sad.mp3")
        
        
    
    print(message)
    return jsonify({'result': result, 'message': message})

# Gets what level the user has selected and changes the difficulty level of the words chosen. 
# If the level is easy, randomly select only 2-3 letter words. 
# If the level is medium, randomly select only 4-5 letter words.
# If the level is hard, randomly select only 6+ letter words.
@app.route('/set-level', methods=['POST'])
def set_level():
    global lower_bounds, upper_bounds
    data = json.loads(request.data)
    if data['level'] == "easy":
        lower_bounds = 2
        upper_bounds = 3
    elif data['level'] == "medium":
        lower_bounds = 4
        upper_bounds = 6
    elif data['level'] == "hard":
        lower_bounds = 7
        upper_bounds = 15
    


if __name__ == '__main__':
    app.run(debug=True)
