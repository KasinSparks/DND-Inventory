import os

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, current_app, jsonify
)

from werkzeug.utils import secure_filename


from blueprints.auth import login_required

from blueprints.admin import get_current_username

from modules.data.database.query_modules import select_query, insert_query, update_query, delete_query
from modules.account.authentication_checks import is_admin, check_if_user_has_character
from modules.data.database import data_helper
from modules.data.form_data import convert_form_field_data_to_int, get_request_field_data
from modules.data.string_shorten import shorten_string
from modules.IO.file.file_checks import allowed_file
from modules.IO.file.image_handler import ImageHandler

bp = Blueprint('character', __name__, url_prefix='/character')

# Character select screen
@bp.route('select')
@login_required
def character_select():
    # Query DB for a list of user's characters
    characters = select_query.select_char_name_and_id(session['user_id'])

    character_list = []

    for c in characters:
        character_list.append(
            {
                'Character_Name' : shorten_string(c['Character_Name'], 17),
                'Character_ID' : c['Character_ID']
            }
        )

    return render_template('character/character_select.html',
                           characters=character_list,
                           header_text=get_current_username())

# Character page
@bp.route('/<int:char_id>')
@login_required
def character_page(char_id):
    characters = None

    if is_admin():
        characters = select_query.select_character_data(char_id)
    else:
        # Check for user_id associated with char_id
        characters = select_query.select_character_data(char_id, session['user_id'])

    if characters is None:
        # Error
        return redirect(url_for('character.character_select'))

    item_id_list = data_helper.get_character_items_id(characters)

    # Query DB for character's items and equipment
    # TODO: Clean this up
    equiped_item_short_data = {
        'head' : item_short_data(characters['Character_Head'], 'Head', 'Head.png'),
        'shoulder' : item_short_data(characters['Character_Shoulder'], 'Shoulder', 'Shoulder.png'),
        'Torso' : item_short_data(characters['Character_Torso'], 'Torso', 'Torso.png'),
        'hand' : item_short_data(characters['Character_Hand'], 'Hand', 'Hand.png'),
        'leg' : item_short_data(characters['Character_Leg'], 'Leg', 'Leg.png'),
        'Foot' : item_short_data(characters['Character_Foot'], 'Foot', 'Foot.png'),
        'trinket1' : item_short_data(characters['Character_Trinket1'], 'Trinket', 'Trinket.png'),
        'trinket2' : item_short_data(characters['Character_Trinket2'], 'Trinket', 'Trinket.png'),
        'ring1' : item_short_data(characters['Character_Ring1'], 'Ring', 'Ring.png'),
        'ring2' : item_short_data(characters['Character_Ring2'], 'Ring', 'Ring.png'),
        'item1' : item_short_data(characters['Character_Item1'], 'Item', 'Item.png'),
        'item2' : item_short_data(characters['Character_Item2'], 'Item', 'Item.png'),
        'weapon1' : item_short_data(characters['Character_Weapon1'], 'Main Hand 1', 'Main_Hand.png'),
        'offhand1' : item_short_data(characters['Character_Weapon2'], 'Off Hand 1', 'Off_Hand.png'),
        'weapon2' : item_short_data(characters['Character_Weapon3'], 'Main Hand 2', 'Main_Hand.png'),
        'offhand2' : item_short_data(characters['Character_Weapon4'], 'Off Hand 2', 'Off_Hand.png')
    }

    class_name = select_query.get_class_names(characters['Character_Class'])
    if class_name is None or class_name == '':
        class_name = 'No Class'

    race_name = select_query.get_race_name_from_id(characters['Character_Race'])
    if race_name is None or race_name == '':
        race_name = 'No Race'

    alignment_name = select_query.get_alignment_name(characters['Character_Alignment'])
    if alignment_name is None or alignment_name == '':
        alignment_name = 'No Alignment'

    stat_bonus = sumation_stats(item_id_list)

    image_data = url_for('static', filename='images/no_image.png')

    char_img = characters["Character_Image"]

    if char_img is not None and char_img != '' and char_img != 'no_image.png':
        image_data = '/imageserver/user/' + characters['Character_Image']

    character_data = {
        'name' : shorten_string(characters['Character_Name'], 20),
        'race' : shorten_string(race_name, 12),
        'class' : shorten_string(class_name, 12),
        'level' : int(characters['Character_Level']),
        'hp' : int(characters['Character_HP']),
        'max_hp' : int(characters['Character_Max_HP']) + stat_bonus['health'],
        'ac' : int(characters['Character_AC']) + stat_bonus['ac'],
        'alignment' : shorten_string(alignment_name, 12),
        'currency' : int(characters['Character_Currency']),
        'weight' : int(characters['Character_Base_Carrying_Cap']),
        'max_weight' : 15 * (int(characters['Character_Strength']) + stat_bonus['str']),
        'str' : int(characters['Character_Strength']) + stat_bonus['str'],
        'dex' : int(characters['Character_Dexterity']) + stat_bonus['dex'],
        'con' : int(characters['Character_Constitution']) + stat_bonus['con'],
        'int' : int(characters['Character_Intelligence']) + stat_bonus['int'],
        'wis' : int(characters['Character_Wisdom']) + stat_bonus['wis'],
        'cha' : int(characters['Character_Charisma']) + stat_bonus['cha'],
        'image' : image_data,
    }

    stat_modifiers = {
        'str' :	data_helper.calculate_modifier(character_data['str']),
        'dex' :	data_helper.calculate_modifier(character_data['dex']),
        'con' :	data_helper.calculate_modifier(character_data['con']),
        'int' :	data_helper.calculate_modifier(character_data['int']),
        'wis' :	data_helper.calculate_modifier(character_data['wis']),
        'cha' :	data_helper.calculate_modifier(character_data['cha'])
    }

    inv_items = get_inv_items(char_id, item_id_list)

    for k in inv_items:
        for i in inv_items[k]['items']:
            character_data['weight'] += int(i['Item_Weight']) * int(i['Amount'])

    return render_template('character/character_page.html',
                           char_id=char_id,
                           equiped_item=equiped_item_short_data,
                           character_data=character_data,
                           stat_modifiers=stat_modifiers,
                           inv_items=inv_items
                        )

def get_inv_items(char_id : int, equiped_items_ids):
    items = {}
    slots = select_query.select_slots()

    for slot in slots:
        items[slot['Slots_Name']] = {
            'id' : slot['Slots_ID'],
            'equipable' : slot['Slots_Equipable'],
            'items' : []
        }

    query_result = select_query.select_item_data_from_inventory(char_id)

    for q in query_result:
        item_fields = {
            'Item_ID' : q['Item_ID'],
            'Item_Weight' : q['Item_Weight'],
            'Item_Name' : q['Item_Name'],
            'Rarities_Color' : q['Rarities_Color'],
            'Amount' : q['Amount'],
            'Is_Equiped' : True if q['Item_ID'] in equiped_items_ids else False,
            'Item_Slot' : q['Item_Slot']
        }

        items[q['Slots_Name']]['items'].append(item_fields)

    return items

def item_short_query(item_id):
    fields = ("Items.Item_Name", "Rarities.Rarities_Color", "Items.Item_Picture")
    joins = ("INNER JOIN Rarities ON Items.Rarity_ID = Rarities.Rarities_ID",)
    return select_query.select_item_fields(item_id, fields, joins)

def item_stat_query(item_id):
    fields = (
        "Items.Item_Str_Bonus", "Items.Item_Dex_Bonus", "Items.Item_Con_Bonus",
        "Items.Item_Int_Bonus", "Items.Item_Wis_Bonus", "Items.Item_Cha_Bonus",
        "Items.Item_Initiative_Bonus", "Items.Item_Health_Bonus", "Items.Item_AC_Bonus",
        "Items.Item_Damage_Num_Of_Dices", "Items.Item_Damage_Num_Of_Dice_Sides"
    )
    return select_query.select_item_fields(item_id, fields)

def sumation_stats(item_id_list):
    stat_bonus = {
        'str' : 0,
        'dex' : 0,
        'con' : 0,
        'int' : 0,
        'wis' : 0,
        'cha' : 0,
        'attack' : 0,
        'initiative' : 0,
        'health' : 0,
        'ac' : 0,
        'num_of_dices' : 0,
        'num_of_dice_sides' : 0
    }

    for item_id in item_id_list:
        query_result = item_stat_query(item_id)
        if query_result is not None:
            stat_bonus['str'] += int(query_result['Item_Str_Bonus'])
            stat_bonus['dex'] += int(query_result['Item_Dex_Bonus'])
            stat_bonus['con'] += int(query_result['Item_Con_Bonus'])
            stat_bonus['int'] += int(query_result['Item_Int_Bonus'])
            stat_bonus['wis'] += int(query_result['Item_Wis_Bonus'])
            stat_bonus['cha'] += int(query_result['Item_Cha_Bonus'])
            stat_bonus['health'] += int(query_result['Item_Health_Bonus'])
            stat_bonus['ac'] += int(query_result['Item_AC_Bonus'])
            stat_bonus['num_of_dices'] += int(query_result['Item_Damage_Num_Of_Dices'])
            stat_bonus['num_of_dice_sides'] += int(query_result['Item_Damage_Num_Of_Dice_Sides'])

    return stat_bonus

def item_short_data(item_id, default_name, defalut_image_name):
    item_data = {
        'name' : default_name,
        'image' : url_for('static', filename='images/items/' + defalut_image_name),
        'rarity_color' : None
    }

    if item_id is None or item_id < 1:
        # No item
        return item_data

    item = item_short_query(item_id)

    if item is None:
        return item_data

    if item['Item_Name'] is not None and item['Item_Name'] != '':
        item_data['name'] = shorten_string(item['Item_Name'], 17)

    if item['Item_Picture'] is not None and item['Item_Picture'] != '' and item['Item_Picture'] != 'no_image.png':
        item_data['image'] = '/imageserver/item/' + item['Item_Picture']


    if item['Rarities_Color'] is not None and item['Rarities_Color'] != '':
        item_data['rarity_color'] = item['Rarities_Color']

    return item_data

# Character create screen
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_character():
    # TODO: add variables so users do not have to reenter data if error occurs
    alignments = select_query.get_alignments()

    return render_template('character/character_create.html',
                           alignments=alignments,
                           header_text=get_current_username())

# TODO: rename this
def input_field_helper(field_name, select_query_callback, insert_query_callback):
    # Check if new race, class, or alignment need to be inserted into the DB
    field = get_request_field_data(field_name)
    if field is not None and field != '':
        data_in_db = select_query_callback(field)

        if data_in_db is None:
            insert_query_callback(field)
            data_in_db = select_query_callback(field)

        return data_in_db
    #TODO: throw an execption here
    return None


# Submit a new character
@bp.route('/create/submit', methods=('GET', 'POST'))
@login_required
def create_character_submit():
    # TODO: data type and value checks
    if request.method == 'POST':
        error = None
        data = {
            'race_id' : None,
            'class_id' : None,
            'alignment_id' : None,
            'level' : convert_form_field_data_to_int('level'),
            'strength' : convert_form_field_data_to_int('strength'),
            'dexerity' : convert_form_field_data_to_int('dexerity'),
            'constitution' : convert_form_field_data_to_int('constitution'),
            'intelligence' : convert_form_field_data_to_int('intelligence'),
            'wisdom' : convert_form_field_data_to_int('wisdom'),
            'charisma' : convert_form_field_data_to_int('charisma'),
            'health_points' : convert_form_field_data_to_int('health_points')
        }

        # Check form data
        name_length = len(str(get_request_field_data('name')))
        if name_length < 1 or name_length > 25:
            error = "ERROR: Invaild name length of {}. ".format(name_length)

        # Check if user already has a character with the same name
        where_clause = "WHERE User_ID=? AND Character_Name=?"
        char_with_same_name = select_query.select(("Character_Name",), "Character", False, where_clause, (session["user_id"], get_request_field_data("name")))

        if char_with_same_name is not None:
            error = "ERROR: You already have a character named " + char_with_same_name["Character_Name"] + " "

        if error is None:
            # Check if new race, class, or alignment need to be inserted into the DB
            data['race_id'] = int(input_field_helper("race_other", select_query.get_race_id_from_name, insert_query.create_race))
            data['class_id'] = int(input_field_helper("class_other", select_query.get_class_id_from_name, insert_query.create_class))
            if request.form["alignment_other"] != "":
                alignment_id = int(input_field_helper("alignment_other", select_query.get_alignment_id_from_name, insert_query.create_alignment))
            else:
                alignment_id = int(select_query.get_alignment_id_from_name(get_request_field_data("alignment")))
                try:
                    select_query.get_alignment_name(alignment_id)
                except:
                    # TODO: change this later to an error message
                    alignment_id = 9

            data["alignment_id"] = alignment_id

            insert_data = {
                "User_ID" : session["user_id"],
                "Character_Name" : get_request_field_data("name"),
                "Character_Class" : data["class_id"],
                "Character_Race" : data["race_id"],
                "Character_Level" : data["level"],
                "Character_Strength" : data["strength"],
                "Character_Dexterity" : data["dexerity"],
                "Character_Constitution" : data["constitution"],
                "Character_Intelligence" : data["intelligence"],
                "Character_Wisdom" : data["wisdom"],
                "Character_Charisma" : data["charisma"],
                "Character_HP" : data["health_points"],
                "Character_Max_HP" : data["health_points"],
                "Character_Alignment" : data["alignment_id"]
            }
            insert_query.create_character(insert_data)

            char_id = select_query.select_char_id_from_name(session["user_id"], get_request_field_data("name"))["Character_ID"]

            return redirect(url_for('character.character_page', char_id=char_id))

    # TODO: add variables so users do not have to reenter data if error occurs
    return redirect(url_for('character.create_character'))

def edit_string_field(select_query_callback, insert_table, insert_field_name, update_query_callback, char_id):
    user_id = session["user_id"]
    if not check_if_user_has_character(user_id, char_id):
        return '400'

    if request.method != 'POST':
        return "Invalid request error."

    new_val = get_request_field_data('value')
    result = select_query_callback(new_val)

    if result is None:
        insert_query.insert(insert_table, {insert_field_name : new_val})
        result = select_query_callback(new_val)

    update_query_callback(result, user_id, char_id)

    return new_val

def edit_number_field(update_query_callback, char_id):
    user_id = session["user_id"]
    if not check_if_user_has_character(user_id, char_id):
        return '400'

    if request.method != 'POST':
        return "Invalid request error."

    new_val = get_request_field_data('value')

    try:
        new_val_int = int(new_val)
    except:
        # TODO: logger
        new_val_int = 0

    update_query_callback(new_val_int, user_id, char_id)

    return new_val

@bp.route('/edit/class/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_class(char_id):
    new_val = edit_string_field(select_query.get_class_id_from_name, "Class", "Class_Name", update_query.update_char_class, char_id)
    return jsonify(character_class=new_val)

@bp.route('/edit/race/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_race(char_id):
    new_val = edit_string_field(select_query.get_race_id_from_name, "Races", "Race_Name", update_query.update_char_race, char_id)
    return jsonify(character_race=new_val)

@bp.route('/edit/alignment/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_alignment(char_id):
    user_id = session["user_id"]
    if not check_if_user_has_character(user_id, char_id):
        return '400'

    if request.method != 'POST':
        return "Invalid request error."

    new_val = get_request_field_data('value')
    alignments = select_query.get_alignments()
    alignment_ids = [x['Alignment_ID'] for x in alignments]

    try:
        new_val = int(new_val)
    except:
        new_val = -1

    if new_val not in alignment_ids:
        # TODO: logger
        return '400'

    update_query.update_char_alignment(new_val, user_id, char_id)

    alignment_name = select_query.get_alignment_name(new_val)
    return alignment_name

@bp.route('/edit/level/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_level(char_id):
    new_val = edit_number_field(update_query.update_char_level, char_id)
    return jsonify(character_level=new_val)

@bp.route('/edit/currency/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_currency(char_id):
    new_val = edit_number_field(update_query.update_char_currency, char_id)
    return jsonify(character_currency=new_val)

@bp.route('/edit/image/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_image(char_id):
    #TODO: change to image_handler
    user_id = session["user_id"]
    if not check_if_user_has_character(user_id, char_id):
        return '400'

    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file included'

        new_img = request.files['image']

        if new_img.filename == '':
            return 'File name was blank'

        dirName = os.path.join('users', str(user_id), "profile_image")
        fullDirName = os.path.join(current_app.config['IMAGE_UPLOAD'], dirName)
        image_name = "profile_image_" + str(select_query.get_username(user_id)) + '_' + str(char_id)
        filename = ImageHandler().save_image(new_img, fullDirName, image_name)
        thumbnail_name = ImageHandler()._resize_image_to_thumbnail(os.path.join(fullDirName, filename), (265, 385), fullDirName)

        update_query.update_char_image(thumbnail_name, user_id, char_id)

        return redirect(url_for('character.character_page', char_id=char_id))

    return '400'

@bp.route('/edit/health/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_health(char_id):
    new_val = edit_number_field(update_query.update_char_health, char_id) 
    return jsonify(character_hp=new_val)

def edit_field(char_id, character_field: str, item_field: str):
    user_id = session["user_id"]
    if not check_if_user_has_character(user_id, char_id):
        # TODO: change this to a exception later
        return 0

    if request.method != 'POST':
        return "Invalid request error."

    new_val = get_request_field_data('value')

    try:
        new_val = int(new_val)
    except:
        new_val = 0

    update_query.update("Character", {character_field : new_val}, "WHERE User_ID=? AND Character_ID=?", (user_id, char_id))

    characters = select_query.select_character_data(char_id)
    item_id_list = data_helper.get_character_items_id(characters)
    stat_additional = 0

    for i in item_id_list:
        item = select_query.select_item_fields(i, (item_field,))
        if item is not None:
            stat_additional += item[item_field]

    return  new_val + stat_additional

@bp.route('/edit/maxhealth/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_maxhealth(char_id):
    val = edit_field(char_id, 'Character_Max_HP', 'Item_Health_Bonus')
    return jsonify(character_max_hp=val)

@bp.route('/edit/ac/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_ac(char_id):
    val = edit_field(char_id, 'Character_AC', 'Item_AC_Bonus')
    return jsonify(character_ac=val)

@bp.route('/edit/initiative/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_initiative(char_id):
    val = edit_field(char_id, 'Character_Initiative', 'Item_Initiative_Bonus')
    return jsonify(character_initiative=val)

@bp.route('/edit/attackBonus/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_attack_bonus(char_id):
    val = edit_field(char_id, 'Character_Attack_Bonus', 'Item_Attack_Bonus')
    return jsonify(character_attack_bonus=val)

@bp.route('/edit/str/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_str(char_id):
    val = edit_field(char_id, 'Character_Strength', 'Item_Str_Bonus')
    return jsonify(
        character_str=val,
        character_max_weight=val * 15,
        character_str_mod=data_helper.calculate_modifier(val)
    )

@bp.route('/edit/dex/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_dex(char_id):
    val = edit_field(char_id, 'Character_Dexterity', 'Item_Dex_Bonus')
    return jsonify(
        character_dex=val,
        character_dex_mod=data_helper.calculate_modifier(val)
    )

@bp.route('/edit/con/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_con(char_id):
    val = edit_field(char_id, 'Character_Constitution', 'Item_Con_Bonus')
    return jsonify(
        character_con=val,
        character_con_mod=data_helper.calculate_modifier(val)
    )

@bp.route('/edit/int/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_int(char_id):
    val = edit_field(char_id, 'Character_Intelligence', 'Item_Int_Bonus')
    return jsonify(
        character_int=val,
        character_int_mod=data_helper.calculate_modifier(val)
    )

@bp.route('/edit/wis/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_wis(char_id):
    val = edit_field(char_id, 'Character_Wisdom', 'Item_Wis_Bonus')
    return jsonify(
        character_wis=val,
        character_wis_mod=data_helper.calculate_modifier(val)
    )

@bp.route('/edit/cha/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_cha(char_id):
    val = edit_field(char_id, 'Character_Charisma', 'Item_Cha_Bonus')
    return jsonify(
        character_cha=val,
        character_cha_mod=data_helper.calculate_modifier(val)
    )

@bp.route('/add/items/<int:char_id>', methods=('GET', 'POST'))
@login_required
def add_items(char_id):
    weight = 0
    user_id = session["user_id"]

    if request.method == 'POST':
        if not check_if_user_has_character(user_id, char_id):
            # TODO: change this to a exception later
            return 0

        for line in request.form:
            try:
                item_id = int(line)
                prev_amount_query = select_query.select_item_amount_from_inv(char_id, item_id)
                prev_amount = 0
                numberOfItems = int(get_request_field_data(line))

                if numberOfItems > 0:
                    if prev_amount_query is not None:
                        prev_amount = int(prev_amount_query['Amount'])
                        update_query.update_inv_item_amount(prev_amount + numberOfItems, char_id, item_id)
                    else:
                        insert_data = {"Character_ID" : char_id, "Item_ID" : item_id, "Amount" : prev_amount + numberOfItems}
                        insert_query.insert("Inventory", insert_data)

            except Exception as e:
                # TODO: logger
                print(e)

    fields = ("Amount", "Items.Item_Weight",)
    joins = ("INNER JOIN Items ON Items.Item_ID=Inventory.Item_ID",)
    where_clause = "WHERE Character_ID=?"
    item_weights_query = select_query.select(fields, "Inventory", True, where_clause, (char_id,), joins)

    for item in item_weights_query:
        weight += float(item['Item_Weight']) * float(item['Amount'])

    return str(weight)

@bp.route('/remove/items/<int:char_id>', methods=('GET', 'POST'))
@login_required
def remove_items(char_id):
    if request.method == 'POST':
        if not check_if_user_has_character(session['user_id'], char_id):
            # TODO: change this to a exception later
            return 0

        try:
            for k in request.form:
                item_id = int(k)
                amount = int(request.form[k])
                if amount < 1:
                    return get_characters_weight(char_id)
                item = select_query.select_item_amount_from_inv(char_id, item_id)
                new_amount = item['Amount'] - amount 

                if (new_amount) > 0:
                    update_query.update_inv_item_amount(new_amount, char_id, item_id)
                else:
                    # check if equiped
                    characters = select_query.select_character_data(char_id)
                    item_id_list = data_helper.get_character_items_id(characters)
                    isEquiped = False

                    for iid in item_id_list:
                        if iid == item_id:
                            isEquiped = True
                            break

                    if not isEquiped:
                        delete_query.delete_item_from_inv(char_id, item_id)
                    else:
                        # TODO: logger
                        print('unable to deleted a currently equiped item')

        except Exception as e:
            # TODO: logger
            print(e)

        return get_characters_weight(char_id)

    return "400"

def get_characters_weight(char_id):
    fields = ("Amount", "Items.Item_Weight",)
    joins = ("INNER JOIN Items ON Items.Item_ID=Inventory.Item_ID",)
    where_clause = "WHERE Character_ID=?"
    item_weights_query = select_query.select(fields, "Inventory", True, where_clause, (char_id,), joins)

    weight = 0
    for item in item_weights_query:
        weight += float(item['Item_Weight']) * float(item['Amount'])

    return str(weight)

@bp.route('item/equip/<int:char_id>/<int:item_id>/<int:slot_number>', methods=('GET', 'POST'))
@login_required
def item_equip(char_id, item_id, slot_number = 0):
    # Check for user_id associated with char_id
    user_id = session["user_id"]
    characters = select_query.select_character_data(char_id, user_id)

    if characters is None:
        # Error
        return redirect(url_for('character.character_select'))

    error = "None"
    item = select_query.select(("*",), "Inventory", False, "WHERE Character_ID=? AND Item_ID=?", (char_id, item_id))

    if item is None:
        return redirect(url_for('character.character_select'))

    slot_name = select_query.select_item_fields(item_id, ("Slots.Slots_Name",), ("INNER JOIN Slots ON Items.Item_Slot=Slots.Slots_ID",))["Slots_Name"]

    modified_slot_name = slot_name

    if slot_number > 0 and slot_number < 5:
        modified_slot_name += str(slot_number)

    fields = ("Wield_Str", "Wield_Dex", "Wield_Wis", "Wield_Int")
    item_data = select_query.select_item_fields(item_id, fields)
    if item_data is None:
        return redirect(url_for("character.character_page", char_id=char_id))

    characters = select_query.select_character_data(char_id, user_id)
    item_id_list = data_helper.get_character_items_id(characters)
    stat_bonus = sumation_stats(item_id_list)

    character_short_data = {
        'Character_Strength' : int(characters['Character_Strength']) + stat_bonus['str'],
        'Character_Dexterity' : int(characters['Character_Dexterity']) + stat_bonus['dex'],
        'Character_Intelligence' : int(characters['Character_Intelligence']) + stat_bonus['int'],
        'Character_Wisdom' : int(characters['Character_Wisdom']) + stat_bonus['wis'],
    }

    count = 0
    for i in item_id_list:
        if i == item_id:
            count += 1

    if count >= item["Amount"]:
        item_name = select_query.select_item_fields(item_id, ("Item_Name", ))["Item_Name"]
        error = "You have already equiped all of " + str(item_name) + " found in your inventory."
        return jsonify(error={"type" : ("equip_error" if error != "None" else "None"), "message" : error})

    # TODO: make this better
    character_fields = {
        "Character_Strength" : fields[0],
        "Character_Dexterity" : fields[1],
        "Character_Wisdom" : fields[2],
        "Character_Intelligence" : fields[3]
    }
    # Check for wield stats
    # TODO: if user equips an item, thus boosting stats and could allow them the equip an item
    for f in character_fields:
        if character_short_data[f] < item_data[character_fields[f]]:
            error = "You do not have enough " + f.split('_')[-1] + " to equip this item.\n"
            error += "Need: " + str(item_data[character_fields[f]]) + " | Current: " + str(character_short_data[f])
            return jsonify(error={"type" : ("equip_error" if error != "None" else "None"), "message" : error})

    update_query.update("Character", {"Character_" + modified_slot_name : item_id}, "WHERE Character_ID=?", (char_id,))

    fields = ("Item_Picture", "Item_Name", "Rarities_Color")
    joins = ("INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID",)
    item_data = select_query.select_item_fields(item_id, fields, joins)

    item_data_dict = {
        'picture' : item_data['Item_Picture'],
        'name' : shorten_string(item_data['Item_Name'], 17),
        'color' : item_data['Rarities_Color'],
        'slot_name' : slot_name,
        'modified_slot_name' : modified_slot_name
    }

    # Refresh the items list after update
    characters = select_query.select_character_data(char_id, user_id)
    item_id_list = data_helper.get_character_items_id(characters)
    stat_bonus = sumation_stats(item_id_list)

    character_data = {
        'max_hp' : int(characters['Character_Max_HP']) + stat_bonus['health'],
        'ac' : int(characters['Character_AC']) + stat_bonus['ac'],
        'weight' : int(characters['Character_Base_Carrying_Cap']),
        'max_weight' : 15 * (int(characters['Character_Strength']) + stat_bonus['str']),
        'str' : int(characters['Character_Strength']) + stat_bonus['str'],
        'dex' : int(characters['Character_Dexterity']) + stat_bonus['dex'],
        'con' : int(characters['Character_Constitution']) + stat_bonus['con'],
        'int' : int(characters['Character_Intelligence']) + stat_bonus['int'],
        'wis' : int(characters['Character_Wisdom']) + stat_bonus['wis'],
        'cha' : int(characters['Character_Charisma']) + stat_bonus['cha'],
    }

    stat_modifiers = {
        'str_mod' :	data_helper.calculate_modifier(character_data['str']),
        'dex_mod' :	data_helper.calculate_modifier(character_data['dex']),
        'con_mod' :	data_helper.calculate_modifier(character_data['con']),
        'int_mod' :	data_helper.calculate_modifier(character_data['int']),
        'wis_mod' :	data_helper.calculate_modifier(character_data['wis']),
        'cha_mod' :	data_helper.calculate_modifier(character_data['cha'])
    }
    return jsonify(
        character_data=character_data,
        stat_modifiers=stat_modifiers,
        item_data=[item_data_dict],
        error={"type" : ("equip_error" if error != "None" else "None"), "message" : error}
    )

@bp.route('item/unequip/<int:char_id>/<int:item_id>/<int:slot_number>', methods=('GET', 'POST'))
@bp.route('item/unequip/<int:char_id>/<int:item_id>/<int:slot_number>/<int:remove_all>', methods=('GET', 'POST'))
@login_required
def item_unequip(char_id, item_id, slot_number=0, remove_all=0):
    # Check for user_id associated with char_id
    user_id = session["user_id"]
    characters = select_query.select_character_data(char_id, user_id)

    error = "None"

    if characters is None:
        # Error
        return redirect(url_for('character.character_select'))

    item = select_query.select(("*",), "Inventory", False, "WHERE Character_ID=? AND Item_ID=?", (char_id, item_id))

    if item is None:
        return redirect(url_for('character.character_select'))

    slot_name = select_query.select_item_fields(item_id, ("Slots.Slots_Name",), ("INNER JOIN Slots ON Items.Item_Slot=Slots.Slots_ID",))["Slots_Name"]

    modified_slot_name = slot_name

    if slot_number > 0 and slot_number < 5:
        modified_slot_name += str(slot_number)

    item_data = []

    # TODO: rework this
    item_data.append({
        "slot_name" : slot_name,
        "modified_slot_name" : modified_slot_name,
        "name" : "null",
        "color" : "null",
        "picture" : "null"
    })

    unequip_item_dict = get_unequip_items_due_to_item_change(user_id, char_id, "Character_" + str(modified_slot_name))
    if remove_all > 0:
        for field_name in unequip_item_dict:
            # TODO: rework this
            _modified_slot_name = str(field_name).split('_')[-1]
            _slot_name = _modified_slot_name
            if _modified_slot_name[-1].isdigit():
                _slot_name = _modified_slot_name[:-1]

            item_data.append({
                "slot_name" : _slot_name,
                "modified_slot_name" : _modified_slot_name,
                "name" : "null",
                "color" : "null",
                "picture" : "null"
            })

            update_query.update("Character", {field_name : -1}, "WHERE Character_ID=?", (char_id,))
    elif unequip_item_dict is None:
        # Error
        error = "Unable to get side effects from unequiping item."
    elif len(unequip_item_dict) > 0:
        item_name = select_query.select_item_fields(item_id, ("Item_Name",))["Item_Name"]
        error = "By unequiping " + str(item_name) + ", the following item will also be unequiped: "
        for field_name in unequip_item_dict:
            error += str(select_query.select_item_fields(unequip_item_dict[field_name], ("Item_Name",),)["Item_Name"])
            error += ", "

        return jsonify(error={"type" : ("unequip_error" if error != "None" else "None"), "message" : error})

    update_query.update("Character", {"Character_" + modified_slot_name : -1}, "WHERE Character_ID=?", (char_id,))

    characters = select_query.select_character_data(char_id, user_id)
    item_id_list = data_helper.get_character_items_id(characters)
    stat_bonus = sumation_stats(item_id_list)

    character_data = {
        'max_hp' : int(characters['Character_Max_HP']) + stat_bonus['health'],
        'ac' : int(characters['Character_AC']) + stat_bonus['ac'],
        'weight' : int(characters['Character_Base_Carrying_Cap']),
        'max_weight' : 15 * (int(characters['Character_Strength']) + stat_bonus['str']),
        'str' : int(characters['Character_Strength']) + stat_bonus['str'],
        'dex' : int(characters['Character_Dexterity']) + stat_bonus['dex'],
        'con' : int(characters['Character_Constitution']) + stat_bonus['con'],
        'int' : int(characters['Character_Intelligence']) + stat_bonus['int'],
        'wis' : int(characters['Character_Wisdom']) + stat_bonus['wis'],
        'cha' : int(characters['Character_Charisma']) + stat_bonus['cha'],
    }

    stat_modifiers = {
        'str_mod' : data_helper.calculate_modifier(character_data['str']),
        'dex_mod' : data_helper.calculate_modifier(character_data['dex']),
        'con_mod' : data_helper.calculate_modifier(character_data['con']),
        'int_mod' : data_helper.calculate_modifier(character_data['int']),
        'wis_mod' : data_helper.calculate_modifier(character_data['wis']),
        'cha_mod' : data_helper.calculate_modifier(character_data['cha'])
    }
    return jsonify(
        character_data=character_data,
        stat_modifiers=stat_modifiers,
        item_data=item_data,
        error={"type" : ("unequip_error" if error != "None" else "None"), "message" : error}
    )

# TODO: change this function's name and move it somewhere else
def get_unequip_items_due_to_item_change(user_id, char_id, slot_name):
    unequip_item_id = select_query.select_char_fields(user_id, char_id, (slot_name,))[slot_name]
    if unequip_item_id < 1:
        return None

    characters = select_query.select_character_data(char_id, user_id)
    item_id_dict = data_helper.get_character_items_id_and_field_names(characters)
    item_id_list = []
    for field_name in item_id_dict:
        item_id_list.append(item_id_dict[field_name])
    stat_bonus = sumation_stats(item_id_list)

    item_fields = ("Item_Str_Bonus", "Item_Dex_Bonus", "Item_Int_Bonus", "Item_Wis_Bonus")
    unequip_item_stats = select_query.select_item_fields(unequip_item_id, item_fields)

    character_data = {
        'str' : int(characters['Character_Strength']) + stat_bonus['str'] - unequip_item_stats["Item_Str_Bonus"],
        'dex' : int(characters['Character_Dexterity']) + stat_bonus['dex'] - unequip_item_stats["Item_Dex_Bonus"],
        'int' : int(characters['Character_Intelligence']) + stat_bonus['int'] - unequip_item_stats["Item_Int_Bonus"],
        'wis' : int(characters['Character_Wisdom']) + stat_bonus['wis'] - unequip_item_stats["Item_Wis_Bonus"],
    }

    #unequip_list = [unequip_item_id]
    unequip_dict = {}

    # Check item stats
    for field_name in item_id_dict:
        wield_fields = ("Wield_Str", "Wield_Dex", "Wield_Wis", "Wield_Int")
        wield_stats = select_query.select_item_fields(item_id_dict[field_name], wield_fields)
        if wield_stats is None:
            continue

        # remove this if you want all armour to be considered
        if field_name.find("Weapon") == -1:
            continue

        for field in wield_fields:
            stat = field.split('_')[-1].lower()
            if wield_stats[field] > character_data[stat]:
                print(str(field) + ": " + str(wield_stats[field]) + ", " + str(character_data[stat]))
                unequip_dict[field_name] = item_id_dict[field_name]
                break

    print(unequip_dict)
    return unequip_dict
