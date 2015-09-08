from flask import Flask
from flask.ext.tweepy import Tweepy

app = Flask(__name__)
app.config.setdefault('TWEEPY_CONSUMER_KEY', 'sve32G2LtUhvgyj64J0aaEPNk')
app.config.setdefault('TWEEPY_CONSUMER_SECRET', '0z4NmfjET4BrLiOGsspTkVKxzDK1Qv6Yb2oiHpZC9Vi0T9cY2X')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', '1425531373-dvjiA55ApSFEnTAWPzzZAZLRoGDo3OTTtt4ER1W')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', '357nVGYtynDtDBmqAZw2vxeXE3F8GbqBSqWInwStDluDX')

tweepy = Tweepy(app)

@app.route('/tweets')
def show_tweets():
    tweets = tweepy.api.public_timeline()
    return render_template('tweets.html', tweets=tweets)

@app.route('/say-something')
def say_something():
    status = tweepy.api.update_status('Hello, world!')
    status_link = 'http://twitter.com/#!/YourUserName/status/%s' % status.id
    return render_template('what_i_said.html', status_link=status_link)

