#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,redirect,url_for, abort
import os
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'

path = '/home/shiyanlou/files'
title = os.listdir(path)
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category',
            backref=db.backref('file',lazy='dynamic'))

    def __init__(self,title,time,category,content):
        self.title = title
        self.created_time = time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name =name
    
    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
    title_db = db.session.query(File.title,File.content)
    title = []
    for x in title_db:
        title.append(x)
    return render_template('index.html',title=title)

@app.route('/files/<file_id>')
def file(file_id):
    f = db.session.query(File.id,File.title,File.content,File.created_time)
    data={}
    judge = File.query.filter_by(id=file_id).first()
    ca = Category.query.filter_by(id=file_id).first()
    if judge:
        data.update({'id':judge.id})
        data.update({'content':judge.content})
        data.update({'time':judge.created_time})
        data.update({'category':ca.name})
        return render_template('file.html',filename=data)
    else  :
        abort(404)

@app.route('/base.html')
def base():
    return render_template('base.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
