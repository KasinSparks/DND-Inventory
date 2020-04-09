from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, current_app, jsonify
)

import os

from werkzeug.utils import secure_filename
from blueprints.auth import login_required, get_current_username
from modules.data.database.query_modules import select_query, delete_query, insert_query, update_query
from modules.account.authentication_checks import check_for_admin_status
from modules.data.string_shorten import shorten_string
from modules.data.form_data import get_request_field_data, convert_form_field_data_to_int
from modules.IO.file.image_handler import ImageHandler

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('users')
@login_required
def admin_users():
    check_for_admin_status()

    users = select_query.select_user_data_except_user(session['user_id'])
    user_data = []

    for u in users:
        user_data.append(
            {
                'User_ID' : u['User_ID'],
                'Username' : shorten_string(u['Username'], 16),
                'Is_Verified' : u['Is_Verified'],
                'Is_Admin' : u['Is_Admin']
            }
        )

    return render_template('admin/users.html',
                            users=user_data,
                            header_text=get_current_username())

@bp.route('users/<string:username>')
@login_required
def admin_users_characters(username):
    check_for_admin_status()

    user_id = select_query.get_user_id(username)
    characters = select_query.select_char_name_and_id(user_id)

    return render_template('admin/characters.html',
                            characters=characters,
                            header_text=get_current_username())	

@bp.route('creationKit')
@login_required
def admin_creationKit():
    check_for_admin_status()

    items = select_query.select_items()
    buckets = {}
    slot_name_query_result = select_query.select_slot_names()

    for sn in slot_name_query_result:
        buckets[sn["Slots_Name"]] = []

    for i in items:
        item_data = {'Item_Name' : shorten_string(i['Item_Name'], 13), 'Item_ID' : i['Item_ID']}
        buckets[i["Slots_Name"]].append(item_data)

    return render_template('admin/items.html',
                            buckets=buckets,
                            header_text=get_current_username())

@bp.route('creationKit/add')
@login_required
def admin_creationKit_add():
    check_for_admin_status()

    slot_names = select_query.select_slot_names()
    rarity_names = select_query.select_rarity_names()
    effect_names = select_query.select_effect_names()

    return render_template('admin/add_item.html',
                            slots=slot_names,
                            rarities=rarity_names,
                            effects=effect_names,
                            header_text=get_current_username())

@bp.route('creationKit/edit/<int:item_id>')
@login_required
def admin_creationKit_edit(item_id):
    check_for_admin_status()

    slot_names = select_query.select_slot_names()
    rarity_names = select_query.select_rarity_names()
    effect_names = select_query.select_effect_names()

    itemQueryResult = select_query.select_items(item_id)

    if itemQueryResult is None:
        itemQueryResult = {
            'Item_Description' : 'null',
            'Item_Name' : 'null',
            'Item_Picture' : 'no_image.png',
            'Rarities_Name' : 'null',
            'Rarities_Color' : 'white',
            #'Item_Slot' : 'null',
            'Item_Weight' : 'null',
            'Item_Str_Bonus' : 0,
            'Item_Dex_Bonus' : 0,
            'Item_Con_Bonus' : 0,
            'Item_Int_Bonus' : 0,
            'Item_Wis_Bonus' : 0,
            'Item_Cha_Bonus' : 0,
            'Item_Attack_Bonus' : 0,
            #'Item_Initiative_Bonus' : 0,
            'Item_Health_Bonus' : 0,
            'Item_Damage_Num_Of_Dices' : 0,
            'Item_Damage_Num_Of_Dice_Sides' : 0,
            'Item_AC_Bonus' : 0
        }

    item_effect1 = 'None'
    item_effect2 = 'None'
    item_slots_name = ''

    if itemQueryResult is not None:
        # Check if item has an effect on it
        if itemQueryResult['Item_Effect1'] is not None and itemQueryResult['Item_Effect1'] > 0:	
            item_effect1 = select_query.select_effect_names(itemQueryResult['Item_Effect1'])['Effect_Name']

        if itemQueryResult['Item_Effect2'] is not None and itemQueryResult['Item_Effect2'] > 0:	
            item_effect2 = select_query.select_effect_names(itemQueryResult['Item_Effect2'])['Effect_Name']
        
        if itemQueryResult['Item_Slot'] is not None and itemQueryResult['Item_Slot'] > 0:	
            item_slots_name = select_query.select_slot_names(itemQueryResult['Item_Slot'])['Slots_Name']

    return render_template('admin/edit_item.html',
                            items=itemQueryResult,
                            slots=slot_names,
                            rarities=rarity_names,
                            effects=effect_names,
                            effect1_name=item_effect1,
                            effect2_name=item_effect2,
                            item_id=item_id,
                            item_slots_name=item_slots_name,
                            header_text=get_current_username())

@bp.route('creationKit/remove/<int:item_id>')
@login_required
def admin_creationKit_remove(item_id):
    check_for_admin_status()
    delete_query.delete_item(item_id)
    return redirect(url_for('admin.admin_creationKit'))

@bp.route('creationKit/add/submit', methods=('GET', 'POST'))
@login_required
def admin_creationKit_add_submit():
    check_for_admin_status()
    if request.method == 'POST':
        name_check = select_query.get_item_id_from_name(get_request_field_data('name'))
        
        if name_check is not None:
            # Name already exist
            return '[TODO: Change this later]\n\nItem name already exist... Please go back and try again.'

        fullDirName = os.path.join(current_app.config['IMAGE_UPLOAD'], "items")
        creationKit_helper("INSERT", fullDirName)
        item_id = select_query.get_item_id_from_name(get_request_field_data('name'))
        update_item_image(name_check, fullDirName, select_query.select_item_picture_name(item_id)["Item_Picture"])

        return redirect(url_for('admin.admin_creationKit'))

@bp.route('creationKit/edit/submit', methods=('GET', 'POST'))
@login_required
def admin_creationKit_edit_submit():
    check_for_admin_status()
    if request.method == 'POST':
        fullDirName = os.path.join(current_app.config['IMAGE_UPLOAD'], "items")
        creationKit_helper("UPDATE", fullDirName)
        item_id = convert_form_field_data_to_int('id')
        update_item_image(item_id, fullDirName, select_query.select_item_picture_name(item_id)["Item_Picture"])

        return redirect(url_for('admin.admin_creationKit'))

@bp.route('users/verify/<int:user_id>')
@login_required
def admin_verify_user(user_id):
    check_for_admin_status()
    update_query.update_isVerified(user_id, True)
    return '200'

@bp.route('notifications')
@login_required
def admin_notifications():
    check_for_admin_status()
    notifications = select_query.select_notifications()

    return render_template('admin/notifications.html',
                            header_text=get_current_username(),
                            notifications=notifications)

@bp.route('notifications/remove/<int:notification_id>')
@login_required
def admin_remove_notification(notification_id):
    check_for_admin_status()
    delete_query.delete_notification(notification_id)
    return '200'

@bp.route('notifications/markRead/<int:notification_id>')
@login_required
def admin_markRead_notification(notification_id):
    check_for_admin_status()
    update_query.update_notification_read_status(notification_id, True)
    return '200'

@bp.route('users/remove', methods=('GET', 'POST'))
@login_required
def admin_remove_user():
    check_for_admin_status()
    if request.method != 'POST':
        return '400'

    user_id = get_request_field_data('user_id')

    delete_query.delete_user(user_id)	

    characters = select_query.get_char_id(user_id)

    for c in characters:
        char_id = c['Character_ID']

        delete_query.delete_character_abilites(char_id)
        delete_query.delete_character_skill(char_id)
        delete_query.delete_character_inventory(char_id)


    delete_query.delete_users_characters(user_id)
    delete_query.delete_login_attempts(user_id)
    delete_query.delete_users_notifications(user_id)

    return '200'

@bp.route('users/makeAdmin', methods=('GET', 'POST'))
@login_required
def make_user_admin():
    check_for_admin_status()
    
    if request.method != 'POST':
        return '400'

    user_id = get_request_field_data('user_id')

    update_query.change_user_admin_status(user_id, True)

    return '200'

def create_new_effect(effect_name, effect_description):
    if effect_name is None or effect_name == '' or effect_description is None or effect_description == '':
        raise Exception('Invalid effect')

    insert_query.insert_effect(effect_name, effect_description)

def creationKit_helper(query_type, image_save_dir):
    query_types = ("UPDATE", "INSERT")

    if query_type not in query_types:
        raise Exception("Invaild query type.")
    
    slot_id = select_query.select_item_fields(convert_form_field_data_to_int('id'), ("Item_Slot",))["Item_Slot"]
    if query_type == query_types[1]:
        slot_id = select_query.get_slot_id_from_name(get_request_field_data('slot'))
        if slot_id is None:
            raise Exception('Not a valid slot')
        else:
            slot_id = int(slot_id)

    rarity_id = select_query.get_rarity_id_from_name(get_request_field_data('rarity'))
    if rarity_id is None:
        raise Exception('Not a valid rarity')
    else:
        rarity_id = int(rarity_id)

    effect1_val = get_request_field_data('effect1')
    effect2_val = get_request_field_data('effect2')

    if effect1_val == 'OTHER':
        effect1_val = get_request_field_data('effect1_name')
        create_new_effect(effect1_val, get_request_field_data('effect1_description'))	

    if effect2_val == 'OTHER':
        effect2_val = get_request_field_data('effect2_name')
        create_new_effect(effect2_val, get_request_field_data('effect2_description'))	

    effect1_id = select_query.select_effect_id_from_name(effect1_val)
    if effect1_id is None:
        effect1_id = -1
    else:
        effect1_id = int(effect1_id['Effect_ID'])

    effect2_id = select_query.select_effect_id_from_name(effect2_val)
    if effect2_id is None:
        effect2_id = -1
    else:
        effect2_id = int(effect2_id['Effect_ID'])

    if 'picture' in request.files:
        new_img = request.files['picture']
        #new_img = get_request_field_data('picture')

        saved_filename = ImageHandler().save_image(new_img, image_save_dir, "temp_item")

        if saved_filename is None:
            saved_filename = "no_image.png"

    query_data = {
        "Item_Name" : str(get_request_field_data('name')),
        "Item_Picture" : saved_filename,
        "Item_Description" : str(get_request_field_data('description')),
        "Item_Slot" : slot_id, 
        "Rarity_ID" : rarity_id,
        "Item_Weight" : convert_form_field_data_to_int('weight'),
        "Item_Str_Bonus" : convert_form_field_data_to_int('str_bonus'),
        "Item_Dex_Bonus" : convert_form_field_data_to_int('dex_bonus'),
        "Item_Con_Bonus" : convert_form_field_data_to_int('con_bonus'),
        "Item_Int_Bonus" : convert_form_field_data_to_int('int_bonus'),
        "Item_Wis_Bonus" : convert_form_field_data_to_int('wis_bonus'),
        "Item_Cha_Bonus" : convert_form_field_data_to_int('cha_bonus'),
        "Item_Effect1" : effect1_id, 
        "Item_Effect2" : effect2_id,
        "Item_Attack_Bonus" : convert_form_field_data_to_int('bonus_damage'),
        #"Item_Initiative_Bonus" : convert_form_field_data_to_int('initiative_bonus'),
        "Item_Health_Bonus" : convert_form_field_data_to_int('health_bonus'),
        "Item_AC_Bonus" : convert_form_field_data_to_int('ac_bonus'),
        "Item_Damage_Num_Of_Dices" : convert_form_field_data_to_int('dnof'),
        "Item_Damage_Num_Of_Dice_Sides" :convert_form_field_data_to_int('dnofs'),
        "Wield_Str" : convert_form_field_data_to_int('wield_str'),
        "Wield_Dex" : convert_form_field_data_to_int('wield_dex'),
        "Wield_Wis" : convert_form_field_data_to_int('wield_wis'),
        "Wield_Int" : convert_form_field_data_to_int('wield_int')
    }

    if query_type == query_types[0]:
        return update_query.update_item(query_data, convert_form_field_data_to_int('id'))
    elif query_type == query_types[1]:
        return insert_query.insert("Items", query_data)

def update_item_image(item_id, path, file_name):
    new_image_name = ImageHandler()._resize_image_to_thumbnail(os.path.join(path, file_name), save_path=path, new_file_name="item_" + str(item_id))
    return update_query.update_item({"Item_Picture" : new_image_name}, item_id)
