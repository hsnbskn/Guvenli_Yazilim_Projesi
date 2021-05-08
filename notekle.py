#-*- coding:utf-8 -*-

# import sqlite3
import datetime

# vt = sqlite3.connect('db.sqlite3')
# crs = vt.cursor()

# note_data = {
#     'title'         :   'Ödev',
#     'description'   :   'aciklama',
#     'is_public'     :   True      
# }

# title = note_data['title']
# description = note_data['description']
# username = 'hasan'
create_date = datetime.datetime.now()
# is_public = "true"

# sql_tablo_yap = """CREATE TABLE IF NOT EXISTS notes (title, description, username, create_date, is_public)"""
# sql_note_add = """INSERT INTO notes VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(title, description, username, create_date, is_public)

# crs.execute(sql_tablo_yap)
# crs.execute(sql_note_add)

# vt.commit()
# vt.close()


from noteApp.models import *

