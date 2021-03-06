#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2013/3/25

import alfred
import os
import sqlite3
import unicodedata

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def read_appnames():
    dockpath = os.path.expanduser("~/Library/Application Support/Dock/")

    dbnames = [os.path.join(dockpath,f) for f in os.listdir(dockpath)
               if os.path.isfile(os.path.join(dockpath,f)) and f.endswith(".db")]

    appnames = []

    for db in dbnames:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        try:
            c.execute("select title from apps")
        except sqlite3.OperationalError, sqlite3.DatabaseError:
            print db
            conn.close()
            continue

        appnames.extend([unicodedata.normalize('NFC',f[0]) for f in c.fetchall()])
        conn.close()

        appnames = list(set(appnames))

    return sorted(appnames)

def write_output(appnames,query):
    results = [alfred.Item(title=f,
                           subtitle="",
                           attributes = {'arg':f,
                                         'autocomplete':f},
                           icon=u"icon.png"
                           ) for f in appnames if query in f.lower()]
    results.insert(0, alfred.Item(title=u"Tidy up LaunchPad : tdl [appname]",
                           subtitle="Hide app icon from LaunchPad. It wouldn't delete App itself.",
                           attributes = {'valid':"no"},
                           icon=u"icon.png"
                           ))

    alfred.write(alfred.xml(results,maxresults=None))

def process(query):
    appnames = read_appnames()

    write_output(appnames, query=query)

if __name__ == '__main__':
    try:
        query = alfred.args()[0].lower().strip()
    except IndexError:
        query = u""

    process(query)
