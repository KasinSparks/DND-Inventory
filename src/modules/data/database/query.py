from modules.data.database.db import query_db
from execptions import EmptyQueryException

class Query():
    def __init__(self, sql_str, args=(), return_data=True, multiple=False):
        self.sql_str = sql_str
        self.args = args
        self.return_data = return_data
        self.multiple = not multiple

    def run_query(self):
        if self.sql_str is None or self.sql_str == "":
            raise EmptyQueryException.EmptyQueryException() 

        return query_db(self.sql_str, self.args, self.return_data, self.multiple)
