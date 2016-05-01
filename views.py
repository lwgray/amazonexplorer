from flask import render_template, flash, redirect, url_for, request, send_from_directory
from __boot__ import app, db
from models import *
from sqlalchemy.types import Integer, Float
from sqlalchemy import and_
from flask.ext.stormpath import login_required, user, groups_required
import json
import os
import time
from hurry.filesize import size, verbose
import boto
from boto.s3.key import Key
# from uploaded_file_stats import file_stats


from emails import shopping_list
from __boot__ import documents
ID = os.environ.get('AWS_ID')
SECRET = os.environ.get('AWS_KEY')

SQS_ID = os.environ.get('SQS_AWS_ID')
SQS_SECRET = os.environ.get('SQS_AWS_KEY')

sqs = boto.connect_sqs(aws_access_key_id=SQS_ID,
                       aws_secret_access_key=SQS_SECRET)
zip_file = sqs.get_queue('zip_file')
xls = sqs.get_queue('xls')
mcsv = sqs.get_queue('csv')
conn = boto.connect_s3(aws_access_key_id=ID,
                       aws_secret_access_key=SECRET)
from boto.sqs.message import Message
BUCKET = os.environ.get('S3_BUCKET')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/target', methods=['GET', 'POST'])
@app.route('/target/<int:page>')
@login_required
@groups_required(['family'])
def target(page=1):
    if request.method == 'POST':
        if request.form.get('sort') == "A-Profit":
            searches = Target.query.filter(
                and_(
                     # Target.product['purchaseprice'].cast(Float) > 0,
                     Target.product['salesrank'].cast(Integer) > 0,
                     Target.product['profit'].cast(Float) > 0,
                     Target.product['salesrank'].cast(Integer) < 250000)
                ).order_by(Target.product['profit'].cast(Float)
                           ).paginate(page, POSTS_PER_PAGE, False).items
        if request.form.get('sort') == "D-Profit":
            searches = Target.query.filter(
                and_(Target.product['salesrank'].cast(Integer) > 0,
                     # Target.product['purchaseprice'].cast(Float) > 0,
                     Target.product['profit'].cast(Float) > 0,
                     Target.product['salesrank'].cast(Integer) < 250000)
                ).order_by(Target.product['profit'].cast(Float).desc()
                           ).paginate(page, POSTS_PER_PAGE, False).items
        if request.form.get('sort') == "A-Salesrank":
            searches = Target.query.filter(
                and_(Target.product['salesrank'].cast(Integer) > 0,
                     Target.product['profit'].cast(Float) > 0,
                     # Target.product['purchaseprice'].cast(Float) > 0,
                     Target.product['salesrank'].cast(Integer) < 250000)
                ).order_by(Target.product['salesrank'].cast(Integer)
                           ).paginate(page, POSTS_PER_PAGE, False).items
        if request.form.get('sort') == "D-Salesrank":
            searches = Target.query.filter(
                and_(
                     Target.product['salesrank'].cast(Integer) > 0,
                    # Target.product['purchaseprice'].cast(Float) > 0,
                     Target.product['profit'].cast(Float) > 0,
                     Target.product['salesrank'].cast(Integer) < 250000)
                ).order_by(Target.product['salesrank'].cast(Integer).desc()
                           ).paginate(page, POSTS_PER_PAGE, False).items
        if request.form.get('sort') == "D-Margin":
            searches = Target.query.filter(
                and_(
                     Target.product['salesrank'].cast(Integer) > 0,
                     # Target.product['purchaseprice'].cast(Float) > 0,
                     Target.product['profit'].cast(Float) > 0,
                     Target.product['salesrank'].cast(Integer) < 250000)
                ).order_by(Target.product['margin'].cast(Float).desc()
                           ).paginate(page, POSTS_PER_PAGE, False).items
    else:
        searches = Target.query.filter(
            and_(
                 Target.product['salesrank'].cast(Integer) > 0,
                 # Target.product['purchaseprice'].cast(Float) > 0,
                 Target.product['profit'].cast(Float) > 0,
                 Target.product['salesrank'].cast(Integer) < 250000)
            ).order_by(Target.date.desc()
                       ).paginate(page, POSTS_PER_PAGE, False).items
    rule = request.url_rule
    return render_template('target.html', rule=rule,
                           searches=searches)
