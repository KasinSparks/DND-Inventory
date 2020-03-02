def create_new_effect(effect_name, effect_description):
	if effect_name is None or effect_name == '' or effect_description is None or effect_description == '':
		raise Exception('Invalid effect')

	sql_str = """INSERT INTO Effects (Effect_Name, Effect_Description)
				VALUES (?, ?);
			"""
	query_db(sql_str, (effect_name, effect_description), False)

from modules.data.database.db import query_db
from execptions import EmptyQueryException

class Query():
	def __init__(self, sql_str, args=(), return_data=True, multiple=False):
		self.sql_str = sql_str
		self.args = args
		self.return_data = return_data
		self.multiple = multiple

	def run_query(self):
		if self.sql_str is None or self.sql_str == "":
			raise EmptyQueryException.EmptyQueryException() 

		return query_db(self.sql_str, self.args, self.return_data, self.multiple)
