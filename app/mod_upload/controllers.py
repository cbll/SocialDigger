from flask import Flask, Blueprint, request, jsonify, make_response, render_template, flash, redirect, url_for, session, escape, g
from flask.ext.login import login_required


upload = Blueprint('upload', __name__, template_folder='upload')

upload.add_url_rule( '/',"upload",user_upload,methods=['post', 'get'])
upload.add_url_rule( '/process','process_upload',process_upload, methods=['post'])

if flask.request.method == 'post':
    


