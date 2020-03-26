from flask import jsonify
import math

def init_item_data():
	item_data = {
		'Item_Description' : 'null',
		'Item_Name' : 'null',
		'Item_Picture' : 'no_image.png',
		'Rarities_Name' : 'null',
		'Rarities_Color' : 'white',
		'Item_Slot' : 'null',
		'Item_Weight' : 'null',
		'Item_Str_Bonus' : 0,
		'Item_Dex_Bonus' : 0,
		'Item_Con_Bonus' : 0,
		'Item_Int_Bonus' : 0,
		'Item_Wis_Bonus' : 0,
		'Item_Cha_Bonus' : 0,
		'Item_Effect1' : None,
		'Item_Effect2' : None,
		'Item_Damage_Num_Of_Dices' : 0,
		'Item_Damage_Num_Of_Dice_Sides' : 0,
		'Item_AC_Bonus' : 0,
		'Item_Bonus_Attack' : 0,
		'Wield_Str' : 0,
		'Wield_Dex' : 0,
		'Wield_Wis' : 0,
		'Wield_Int' : 0
	}
	return item_data

def item_data_to_json(item_data, image, effect1_data, effect2_data):
	return jsonify(
		description=item_data['Item_Description'],
		name=item_data['Item_Name'],
		image=image,
		rarity=item_data['Rarities_Name'],
		rarity_color=item_data['Rarities_Color'],
		slot=item_data['Item_Slot'],
		weight=item_data['Item_Weight'],
		str_bonus=item_data['Item_Str_Bonus'],
		dex_bonus=item_data['Item_Dex_Bonus'],
		con_bonus=item_data['Item_Con_Bonus'],
		int_bonus=item_data['Item_Int_Bonus'],
		wis_bonus=item_data['Item_Wis_Bonus'],
		cha_bonus=item_data['Item_Cha_Bonus'],
		effect1_name=effect1_data['Effect_Name'],
		effect1_description=effect1_data['Effect_Description'],
		effect2_name=effect2_data['Effect_Name'],
		effect2_description=effect2_data['Effect_Description'],
		item_damage_num_of_dices=item_data['Item_Damage_Num_Of_Dices'],
		item_damage_num_of_dice_sides=item_data['Item_Damage_Num_Of_Dice_Sides'],
		ac=item_data['Item_AC_Bonus'],
		bonus_damage=item_data['Item_Attack_Bonus'],
		wield_str=item_data['Wield_Str'],
		wield_dex=item_data['Wield_Dex'],
		wield_wis=item_data['Wield_Wis'],
		wield_int=item_data['Wield_Int'],
	)

def get_character_items_id(char_item_query_result):
	field_names = (
		"Character_Head", "Character_Shoulder", "Character_Torso", "Character_Hand", "Character_Leg", 
		"Character_Foot", "Character_Trinket1", "Character_Trinket2","Character_Ring1", "Character_Ring2",
		"Character_Item1","Character_Item2", "Character_Weapon1", "Character_Weapon2", "Character_Weapon3",
		"Character_Weapon4"
	)

	item_id_list = []
	for fn in field_names:
		item_id_list.append(char_item_query_result[fn])
	return item_id_list

def calculate_modifier(stat_value):
	return math.floor((stat_value - 10) / 2)