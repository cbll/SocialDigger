# -*- coding: utf-8 -*-
import json
import StringIO
import time
import twitter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from wordcloud import WordCloud

from flask import Flask, Blueprint, request, jsonify, make_response, render_template, flash, redirect, url_for, session, escape, g
from flask.ext.login import login_required, current_user
from sqlalchemy import asc
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort

from app.database import db
from app.mod_users.models import WordCloudImage, TweetsStack
from config import WC_IMAGES_ROOT, WC_IMAGES_URL

authenticated = Blueprint('authenticated', __name__, url_prefix='/authenticated', template_folder='authenticated')

api = twitter.Api(
    consumer_key='sve32G2LtUhvgyj64J0aaEPNk',
    consumer_secret='0z4NmfjET4BrLiOGsspTkVKxzDK1Qv6Yb2oiHpZC9Vi0T9cY2X',
    access_token_key='1425531373-dvjiA55ApSFEnTAWPzzZAZLRoGDo3OTTtt4ER1W',
    access_token_secret='357nVGYtynDtDBmqAZw2vxeXE3F8GbqBSqWInwStDluDX')


# Add CSS sheet only for unauthenticated urls
@authenticated.context_processor
def css_processor():
    return dict(css='/static/css/authenticated.css')

@login_required
def index():
    return render_template('authenticated/index.html')


@login_required
def dig():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
    return render_template('authenticated/dig.html', **{'username': username})


@login_required
def dig_results():
    results = current_user.images
    return render_template('authenticated/dig_results.html', **{'results': results})


@login_required
def dig_result(wci_id):
    try:
        wci = WordCloudImage.query.filter(WordCloudImage.id == wci_id, WordCloudImage.user_id == current_user.id).one()
        return render_template('authenticated/dig_result.html', **{'wci': wci})
    except exc.NoResultFound, exc.MultipleResultsFound:
        abort(404)


@login_required
def plt_image(username):
    tweets_stacks = TweetsStack.query.filter(
        TweetsStack.twitter_username == username).order_by(asc(TweetsStack.id)).all()
    if tweets_stacks:
        since_id = tweets_stacks[-1].last_tweet_id
        statuses = api.GetUserTimeline(screen_name=username, since_id=int(since_id))
    else:
        statuses = api.GetUserTimeline(screen_name=username)

    if statuses:
        tweets_stack_body = {s.id: s.text for s in statuses}
        last_tweet_id = statuses[0].id
        uts_obj = TweetsStack(twitter_username=username,
                              tweets_json=json.dumps(tweets_stack_body), last_tweet_id=last_tweet_id)
        db.session.add(uts_obj)
        db.session.commit()
        tweets_stacks.append(uts_obj)

    all_tweets_text = ''
    for ts in tweets_stacks:
        for id, text in json.loads(ts.tweets_json).items():
            all_tweets_text += ' %s' % text

    wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(all_tweets_text)
    fig = plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)

    filename = '%s-%s.png' % (current_user.id, int(time.time()))
    filepath = '%s/%s' % (WC_IMAGES_ROOT, filename)
    plt.savefig(filepath)
    url = '%s%s' % (WC_IMAGES_URL, filename)
    image_obj = WordCloudImage(user_id=current_user.id, image_url=url, twitter_username=username)
    db.session.add(image_obj)
    db.session.commit()
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

# URLs
authenticated.add_url_rule('/home/', 'index', index)
authenticated.add_url_rule('/dig/', 'dig', dig, methods=['post', 'get'])
authenticated.add_url_rule('/dig_results/', 'dig_results', dig_results)
authenticated.add_url_rule('/dig_result/<wci_id>/', 'dig_result', dig_result)
authenticated.add_url_rule('/plt_image/<username>/', 'plt_image', plt_image, methods=['post', 'get'])
