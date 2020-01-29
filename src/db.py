import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db


def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_app(app):
	app.teardown_appcontext(close_db)
	#app.cli.add_command(init_db_command)

def query_db(query, args=(), returnDataQuery=True, one=False):
	if returnDataQuery:
		cur = get_db().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return (rv[0] if rv else None) if one else rv
	else:
		cur = get_db().execute(query, args)
		get_db().commit()
		cur.close()
	
	return