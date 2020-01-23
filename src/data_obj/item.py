from ..db import query_db

class Item:
	def __init__(self, **kwargs):
		if('ID' in kwargs):
			# the item ID was supplied, pull the data from the database
			self.ID = kwargs['ID']
		else:
			self.ID = None
			self.description = kwargs.get('description', '')
			self.name = kwargs.get('name', None)
			self.image = kwargs.get('image', None)
			self.rarity = kwargs.get('rarity', None)
			self.rarity_color = kwargs.get('rarity_color', None)
			self.slot = kwargs.get('slot', None)
			self.weight = kwargs.get('weight', 0)
			self.str_bonus = kwargs.get('str_bonus', 0)
			self.dex_bonus = kwargs.get('dex_bonus', 0)
			self.con_bonus = kwargs.get('con_bonus', 0)
			self.int_bonus = kwargs.get('int_bonus', 0)
			self.wis_bonus = kwargs.get('wis_bonus', 0)
			self.cha_bonus = kwargs.get('cha_bonus', 0)
			self.effect1 = kwargs.get('effect1', None)
			self.effect2 = kwargs.get('effect2', None)

	
	# Do db stuff in here
	def __getQuery__(self):
		queryStr = """SELECT *
					FROM Items
					LEFT JOIN Rarities ON Items.Rarity_ID=Rarities.Rarities_ID
					WHERE Items.Item_ID=?;"""
		# Check to see if ID has been assigned
		if self.ID is None or self.ID < 0:
			# Can not perform a get query
			raise Exception('Could not perform get query. Item is not in DB')	
		
		result = query_db(queryStr, (self.ID,), True, True)
		
		return result['Rarities_Name']

	def __setAllValues__(self, values):
		self.description = kwargs.get('description', values['Item_'])
		self.name = kwargs.get('name', None)
		self.image = kwargs.get('image', None)
		self.rarity = kwargs.get('rarity', None)
		self.rarity_color = kwargs.get('rarity_color', None)
		self.slot = kwargs.get('slot', None)
		self.weight = kwargs.get('weight', 0)
		self.str_bonus = kwargs.get('str_bonus', 0)
		self.dex_bonus = kwargs.get('dex_bonus', 0)
		self.con_bonus = kwargs.get('con_bonus', 0)
		self.int_bonus = kwargs.get('int_bonus', 0)
		self.wis_bonus = kwargs.get('wis_bonus', 0)
		self.cha_bonus = kwargs.get('cha_bonus', 0)
		self.effect1 = kwargs.get('effect1', None)
		self.effect2 = kwargs.get('effect2', None)
		return

	def __insertQuery__(self):
		return