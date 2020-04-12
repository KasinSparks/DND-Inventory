import { Redirect } from "./scripts/Redirect.js";
import { Data_Change_Submit } from "./scripts/field_editing/Data_Change_Submit.js";
import { Data_Caller } from "./scripts/Data_Caller.js";
import { Data_Change } from "./scripts/field_editing/Data_Change.js";
import { Data_Change_Type } from "./scripts/field_editing/Data_Change_Type.js"

import { Logger } from "./scripts/Logger.js";
	window.onload = function(){
	var logger = new Logger(true);
	logger.log("yup");
}

var saveForLater = new Map([["", ""]]);

window.equipmentItemDetails = function equipmentItemDetails(charId, equipmentItemStr){
	var hmtlInner = document.getElementsByClassName('eq_container')[0];
	console.log(saveForLater[0]);
	if(saveForLater[0] != undefined && saveForLater[0][1] != ""){
		console.error('Item details is already open.');
		return;
	}
	saveForLater[0] = [equipmentItemStr, hmtlInner.innerHTML];
	itemDataFromXHTTP(hmtlInner, charId, equipmentItemStr);

	return;
}

function insertIntoHTML(element, data){
	element.innerHTML = data;
	return;
}

function appendToHTML(element, data){
	element.innerHTML = element.innerHTML.concat(data);
	return;
}

function itemInfo(element, jsonData){
	// Quick verify data sent back
	if(jsonData != null && (jsonData.name != '' && jsonData.name != 'null')){
		appendToHTML(element, getEquipmentItemDetailsHTML(jsonData));
	} else {
		console.log("JSON data was null");
		saveForLater[0] = ["", ""];
	}
}

function itemDataFromXHTTP(element, charId, equipmentItemStr){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			//itemInfo(element, this.responseText);
			console.log(this.response);
			itemInfo(element, this.response);
			return
		}
	};
	
	const webpage = '/dataserver/equipmentItemDetails/' + charId + '/' + equipmentItemStr;
	xhttp.open("GET", webpage, true);
	
	xhttp.responseType = 'json';

	xhttp.send();
}

window.test2 = function test2(){
	console.debug("test2()");
	console.debug(saveForLater[0][1]);
	document.getElementsByClassName('eq_container')[0].innerHTML = saveForLater[0][1];
	saveForLater[0] = ["",""];
	return;
}

function getEquipmentItemDetailsHTML(jsonData, function_call='test2()'){
	//var jsonResponse = JSON.parse(jsonData);
	//console.log(jsonResponse);
	console.log(jsonData);
	var equipmentItemDetailsHTML = '<!--ITEM_INFO-->\
	<div class="item_info">\
		<div class="item_info_header">\
			<img style="border-color: ' + jsonData.rarity_color + '" src="' + jsonData.image + '" alt="' + jsonData.slot + ' Item"/>\
			<h1 style="color: ' + jsonData.rarity_color + '">' + jsonData.name + '<h1>\
		</div>\
		<div class="item_info_data">\
			<div class="item_info_description">\
				<p>' + jsonData.description + '</p>\
			</div>\
			<table class="stats_table">\
				<tr>\
					<td colspan=4><h2 style="color: ' + jsonData.rarity_color + ';">' + jsonData.rarity + '</h2></td>\
				</tr>';
				
				if(jsonData.slot === 10){	
					equipmentItemDetailsHTML += '<tr>\
						<td colspan=2><h2>Damage:</h2></td>\
						<td colspan=2><h2>' + jsonData.item_damage_num_of_dice_sides + ' d ' + jsonData.item_damage_num_of_dices + ' ' + (jsonData.bonus_damage < 0 ? '' : '+') + jsonData.bonus_damage + '</h2></td>\
					</tr>\
					<tr>\
						<td><h2>Wield Str:</h2></td>\
						<td><h2>' + jsonData.wield_str + '</h2></td>\
						<td><h2>Wield Dex:</h2></td>\
						<td><h2>' + jsonData.wield_dex + '</h2></td>\
					</tr>\
					<tr>\
						<td><h2>Wield Wis:</h2></td>\
						<td><h2>' + jsonData.wield_wis + '</h2></td>\
						<td><h2>Wield Int:</h2></td>\
						<td><h2>' + jsonData.wield_int + '</h2></td>\
					</tr>'
				} else if(jsonData.slot === 3){
					equipmentItemDetailsHTML += '<tr>\
						<td colspan=2><h2>AC:</h2></td>\
						<td colspan=2><h2>' + jsonData.ac + '</h2></td>\
					</tr>'

				}
				 
	equipmentItemDetailsHTML += '<tr>\
					<td><h2>STR:</h2></td>\
					<td><h2>' + jsonData.str_bonus + '</h2></td>\
					<td><h2>DEX:</h2></td>\
					<td><h2>' + jsonData.dex_bonus + '</h2></td>\
				</tr>\
				<tr>\
					<td><h2>CON:</h2></td>\
					<td><h2>' + jsonData.con_bonus + '</h2></td>\
					<td><h2>INT:</h2></td>\
					<td><h2>' + jsonData.int_bonus + '</h2></td>\
				</tr>\
				<tr>\
					<td><h2>WIS:</h2></td>\
					<td><h2>' + jsonData.wis_bonus + '</h2></td>\
					<td><h2>CHA:</h2></td>\
					<td><h2>' + jsonData.cha_bonus + '</h2></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2 class="weight">Weight:</h2></td>\
					<td colspan=2><h2 class="weight">' + jsonData.weight + '</h2></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2>' + jsonData.effect1_name + ':</h2></td>\
					<td colspan=2><h2>' + jsonData.effect1_description + '</h2></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2>' + jsonData.effect2_name + ':</h2></td>\
					<td colspan=2><h2>' + jsonData.effect2_description + '</h2></td>\
				</tr>\
			</table>\
		</div>\
		<div class="item_info_footer" onclick="' + function_call + ';">\
			<h1>X</h1>\
		</div>\
	</div>\
	';
	return equipmentItemDetailsHTML;
}

window.accept_tos = function accept_tos(){Redirect.redirect("tos/accept");}

window.decline_tos = function decline_tos(){
	Redirect.redirect_after_seconds('../login', 10000);
	// TODO: make a better looking message
	document.getElementsByClassName('login_container')[0].innerHTML = '<p>Terms of Service have been declined.\n\nRedirecting in 10 seconds...</p>';
}

window.inv_tab = function inv_tab(activeClass, activeButtonID){
	inv_inner_area_children = document.getElementsByClassName('inv_container_inner_area')[0].children;

	for(var i = 0; i < inv_inner_area_children.length; ++i){
		if(inv_inner_area_children[i].className === activeClass){
			inv_inner_area_children[i].removeAttribute('style');
		} else {
			inv_inner_area_children[i].style.display = 'none';
		}
	}

	inv_buttons = document.getElementsByClassName('inv_container_menubar')[0].children;
	for(var i = 0; i < inv_buttons.length; ++i){
		if(inv_buttons[i].id === activeButtonID){
			inv_buttons[i].className = inv_buttons[i].className.replace('inactive', 'active');
		} else if(!inv_buttons[i].className.includes('inactive')){
			inv_buttons[i].className = inv_buttons[i].className.replace('active', 'inactive');
		}
	}
}

window.category_expand_and_collapse = function category_expand_and_collapse(categoryID, option, line_item_class, button_class){
	inv_cat = document.getElementById(categoryID); 

	inv_line_items = inv_cat.getElementsByClassName(line_item_class);

	inv_category_button = inv_cat.getElementsByClassName(button_class)[0];

	for(var i = 0; i < inv_line_items.length; ++i){
		if(option === 'expand'){
			inv_line_items[i].removeAttribute('style');
			setToOption(inv_category_button, option, 'collapse');
			setToOption_Image(inv_category_button, option, 'collapse');
		} else if(option === 'collapse'){
			inv_line_items[i].style.display = 'none';
			setToOption(inv_category_button, option, 'expand');
			setToOption_Image(inv_category_button, option, 'expand');
		} else {
		// do nothing
		}
	}

	return;
}

function setToOption(element, prevOption, option){
	element.setAttribute('onclick', element.getAttribute('onclick').replace("'" + prevOption + "'", "'" + option + "'"));
}

function setToOption_Image(element, prevOption, option){
	element.setAttribute('class', element.getAttribute('class').replace(prevOption, option));
}

window.select_other_button = function select_other_button(element_name=[], value){
	console.log(value);
	element_name.forEach(element => {
		if(value === "OTHER"){
			select_button_helper(element, '', 'true');
		} else {
			select_button_helper(element, 'display: none;');
		}
	});
}

window.select_standard_button = function select_standard_button(element_name=[]){
	element_name.forEach(element => {
		select_button_helper(element, 'display: none;');
	});
}

function select_button_helper(element_name, style_attribute, required='false'){
	console.log(element_name);
	el = document.getElementsByName(element_name)[0];
	el.setAttribute('style', style_attribute);
	if(required === 'false'){
		el.removeAttribute('required');
	} else {
		el.setAttribute('required', 'true');
	}
	el.value = "";	
	
}


var isChangeCharDataOpen = false;

// TODO: clean up call
window.submitChanges = function submitChanges(char_id, field_id_name, submit_route, callType=0){
	Data_Change_Submit.submit(char_id, field_id_name, submit_route, callType);
	isChangeCharDataOpen = false;
}

window.abortChanges = function abortChanges(field_id_name){
	if(isChangeCharDataOpen){
		document.getElementById(field_id_name).setAttribute('style', '');
		document.getElementsByClassName('char_item_val_change_container')[0].remove();
	}
	isChangeCharDataOpen = false;
	return;
}

function changeField(char_id, data_change_type, data_url, field_id_name, submit_url){
	if(!isChangeCharDataOpen){
		var dc = new Data_Change(char_id, data_change_type, data_url, field_id_name, submit_url);
		isChangeCharDataOpen = dc.change_data();
	}
}

window.changeClass = function changeClass(char_id){
	changeField(char_id, Data_Change_Type.Types.STRING, '/dataserver/getClassName/' + char_id,
		'character_class', '/character/edit/class/' + char_id);
}

window.changeRace = function changeRace(char_id){
	changeField(char_id, Data_Change_Type.Types.STRING, '/dataserver/getRaceName/' + char_id,
		'character_race', '/character/edit/race/' + char_id);
}

window.changeLevel = function changeLevel(char_id){
	changeField(char_id, Data_Change_Type.Types.NUMBER, '/dataserver/getLevel/' + char_id,
		'character_level', '/character/edit/level/' + char_id);
}

window.changeImage = function changeImage(char_id){
	changeField(char_id, Data_Change_Type.Types.IMAGE, '/dataserver/dummyCall',
		'character_image', '/character/edit/image/' + char_id);
}

window.changeHealth = function changeHealth(char_id){
	changeField(char_id, Data_Change_Type.Types.NUMBER, '/dataserver/getHealth/' + char_id,
		'character_hp', '/character/edit/health/' + char_id);
}

window.changeMaxHealth = function changeMaxHealth(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getMaxHealth/' + char_id,
		'character_max_hp', '/character/edit/maxhealth/' + char_id);
}

window.changeAC = function changeAC(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getAC/' + char_id,
		'character_ac', '/character/edit/ac/' + char_id);
}

window.changeInitiative = function changeInitiative(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getInitiative/' + char_id,
		'character_initiative', '/character/edit/initiative/' + char_id);
}

window.changeAttackBonus = function changeAttackBonus(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getAttackBonus/' + char_id,
		'character_attack_bonus', '/character/edit/attack_bonus/' + char_id);
}

window.changeAlignment = function changeAlignment(char_id){
	changeField(char_id, Data_Change_Type.Types.SELECT,
		'/dataserver/getAlignmentOptions',
		'character_alignment', '/character/edit/alignment/' + char_id);
}

window.changeCurrency = function changeCurrency(char_id){
	changeField(char_id, Data_Change_Type.Types.NUMBER, '/dataserver/getCurrency/' + char_id,
		'character_currency', '/character/edit/currency/' + char_id);
}

window.changeStr = function changeStr(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getStr/' + char_id,
		'character_str', '/character/edit/str/' + char_id);
}

window.changeDex = function changeDex(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getDex/' + char_id,
		'character_dex', '/character/edit/dex/' + char_id);
}

window.changeCon = function changeCon(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getCon/' + char_id,
		'character_con', '/character/edit/con/' + char_id);
}

window.changeInt = function changeInt(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getInt/' + char_id,
		'character_int', '/character/edit/int/' + char_id);
}

window.changeWis = function changeWis(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getWis/' + char_id,
		'character_wis', '/character/edit/wis/' + char_id);
}

window.changeCha = function changeCha(char_id){
	changeField(char_id, Data_Change_Type.Types.NUM_ADDITIONAL, '/dataserver/getCha/' + char_id,
		'character_cha', '/character/edit/cha/' + char_id);
}


function add_item_to_inv(char_id, item_slot){
	var ccd = new ChangeData(char_id, '/dataserver/getItemList/' + item_slot, 'json', '', '');
	ccd.dataCall(inv_item_add_pop_up);
	return; 
}

function show_inv_item_details(char_id, item_id){
	var ccd = new ChangeData(char_id, '/dataserver/inventoryItemDetails/' + char_id + '/' + item_id, 'json', '', '');
	ccd.dataCall(inv_item_details_pop_up);
	return; 
}

var inv_items_save_for_later = '';

function inv_item_details_pop_up(char_id, response, a=null, b=null){
	var inner = document.getElementsByClassName('inv_container')[0].getElementsByClassName('inner_container')[0];
	inv_items_save_for_later = inner.innerHTML;	
	inner.innerHTML += getEquipmentItemDetailsHTML(response, 'close_inv_item_details()');
}

function close_inv_item_details(){
	var inner = document.getElementsByClassName('inv_container')[0].getElementsByClassName('inner_container')[0];
	inner.innerHTML = inv_items_save_for_later;
}

function enable_input(input_name){
	var element = document.getElementsByName(input_name)[0];
	var status = element.getAttribute('disabled');

	if(status == null){
		element.setAttribute('disabled', '');
	} else {
		element.removeAttribute('disabled');
	}

	return;
}

function inv_item_add_pop_up(char_id, response, a=null, b=null){
	var items_html = '';

	response.items.forEach(element => {
		items_html += '\
			<div class="inv_add_item_row_item">\
				<div class="inv_add_item_input">\
					<input type="checkbox" name="' + element.Item_ID + '" onclick="enable_input(\'' + element.Item_ID + '.amount\');">\
					<input type="number" name="' + element.Item_ID + '.amount" min="1" value="1" disabled>\
				</div>\
				<div class="inv_add_item_data">\
					<img src="/imageserver/item/' + element.Item_Picture + '"/>\
					<h2 style="color:' + element.Rarities_Color + ';">' + element.Item_Name + '</h2>\
				</div>\
			</div>\
		'
	});


	var html = '\
		<div class="inv_add_item_container">\
			<div class="inv_add_item_header">\
				<h1>' + response.slot_name + '<h1>\
			</div>\
			' + items_html + '\
			<div class="inv_add_item_buttons">\
				<div class="clickable" onclick="invAddSubmit(' + char_id + ',\'' + response.slot_name + '\');">\
					<h4 style="color: white;">Submit</h4>\
				</div>\
				<div class="clickable" onclick="cancelAddItem();">\
					<h4 style="color: white;">Cancel</h4>\
				</div>\
			</div>\
		</div>\
		';

	document.getElementsByClassName('inv_container')[0].innerHTML += html;
}

function cancelAddItem(){
	document.getElementsByClassName('inv_add_item_container')[0].remove();
	return;
}

function invAddSubmit(char_id, slot_name){
	var rowItems = document.getElementsByClassName('inv_add_item_row_item');

	//document.getElementsByClassName('')[0].getElementsByTagName('input')[0].value;

	var parmStr = '';
	var isFirst = true;

	for(var i = 0; i < rowItems.length; ++i){
		var inputItems = rowItems[i].getElementsByTagName('input');
		var isChecked = false;
		for(var j = 0; j < inputItems.length; ++j){
			if(isChecked){
				parmStr += inputItems[j].value;
			}
			
			if(inputItems[j].type === 'checkbox' && inputItems[j].checked){
				if(!isFirst){
					parmStr += '&';
					
				} else {
					isFirst = false;
				}
				parmStr += inputItems[j].name + '='; 
				isChecked = true;
			} 
			console.log(parmStr);
		}

		/* if(i < rowItems.length - 1 && parmStr.length > 0){
			parmStr += '&';
		} */
	}

	console.log(parmStr);

	submitAddItemData('/character/add/items/' + char_id, parmStr, 'character_weight', char_id, slot_name);


	return;
}

function removeItemDialog(char_id, current_number, field_id_name, submit_route){
	var html_string = '<div class="item_remove_container">';
	
	//html_string += '<input type="number" id="new_value" value="' + current_number.current_value + '">';
	html_string += '<input type="number" id="inv_item_new_value" value="1" min="0" max="' + current_number.current_value + '">';

	var field = document.getElementById(field_id_name);
	if(field == null){
		return;
	}

	isRemoveItemOpen = true;

	html_string += '<button onclick="removeItemSubmit(' + char_id + ',' + current_number.item_id + ',\'' + current_number.slot_name +'\');">Remove</button>\
					<button onclick="abortInvItemsChanges(\'' + field_id_name + '\');">X</button>\
					</div>';

	
	field.parentElement.innerHTML += html_string;
	

	return;
}

var isRemoveItemOpen = false;

function abortInvItemsChanges(field_id_name){
	//document.getElementById(field_id_name).setAttribute('style', '');
	document.getElementsByClassName('item_remove_container')[0].remove();
	isRemoveItemOpen = false;
	return;
}

function removeItem(char_id, item_id){
	if(!isRemoveItemOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getItemAmount/' + char_id + '/' + item_id, 'json',
			'inv_item_' + item_id, '/character/edit/itemAmount/'+ char_id + '/' + item_id);
		ccd.dataCall(removeItemDialog);
	} else {
		console.error('remove item is already open...');
	}
}


function removeItemSubmit(char_id, item_id, slot_name){
	var element = document.getElementById('inv_item_new_value');
	var paramStr = item_id + '=' + element.value;
	console.log('paramStr: ' + paramStr);
	submitAddItemData('/character/remove/items/' + char_id, paramStr, '', char_id, slot_name);
	return;
}

/* 
function submitData(url, params, field_id_name='', is_json=false){
	var http = new XMLHttpRequest();
	http.open('POST', url, true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			if(!is_json && field_id_name != ''){
				document.getElementById(field_id_name).innerHTML = http.responseText;
			} else {
				var data = JSON.parse(http.response);
				for(var k in data){
					console.log(k + ', ' + data[k])
					document.getElementById(k).innerHTML = data[k];
				}
			}
		}
	}
	http.send(params);
} */

function updateInvCategory(callbackFunction = null, char_id, category_name, webpage, keep_open=false){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			if(this.response == null){
				console.error('Response from ' + webpage + ' was null.');
				return;
			}
			if(callbackFunction == null){
				console.log(this.response);
				return this.response;
			}
			
			callbackFunction(char_id, this.response, category_name, keep_open);
			return;
		}
	};
	
	xhttp.open("GET", webpage, true);
	
	xhttp.responseType = 'json'; 

	xhttp.send();

	return;
}

function updateInvCategoryHelper(char_id, response, category_name, keep_open){
	if(keep_open){
		return;
	}
	var parent = document.getElementById('inv_category_' + category_name);
	var lineItems = parent.getElementsByClassName('inv_line_item');
	
	console.log(lineItems.length);
	// because... javascript have to do this in reverse order
	for(var i = lineItems.length - 1; i > -1; --i){
		console.log('removing...');
		lineItems[i].remove();
		console.log('here');
		console.log(i);
	}

	itemString = '';
 
	response.forEach(item => {
		itemString = '';
		console.log(item);
		itemString += '\
			<div class="inv_line_item clickable">\
				<div class="inv_line_inner">\
					<div id="inv_item_' + item.Item_ID + '" class="inv_remove_item_button clickable" onclick="removeItem(' + char_id + ', ' + item['Item_ID'] + ');"></div >\
					<div class="inv_item_text" onclick="show_inv_item_details(' + char_id + ', ' + item.Item_ID + ');">\
						<h2 style="color: ' + item.Rarities_Color + '">' + item.Item_Name + '</h2>';
	
		if(item.Amount > 1){
			itemString += '<h3>x' + item.Amount + '</h3>';
		}

		itemString += '</div>';

		

		if(item.Is_Equiped){
			// TODO: add support for multiple slots
			if(category_name == 'Ring' || category_name == 'Item' || category_name == 'Trinket' || category_name == 'Weapon'){
				itemString += '<div class="inv_equip_unequip_item_button clickable" onclick="unequipItem(' + char_id + ', ' + item.Item_ID + ',\'' + category_name + '\', ' + item.Slots_ID + ', true);"></div >';
			} else {
				itemString += '<div class="inv_unequip_item_button clickable" onclick="unequipItem(' + char_id + ', ' + item.Item_ID + ',\'' + category_name + '\');"></div >';
			}
		}else{
			if(category_name == 'Ring' || category_name == 'Item' || category_name == 'Trinket' || category_name == 'Weapon'){
				itemString += '<div class="inv_equip_unequip_item_button clickable" onclick="equipItem(' + char_id + ', ' + item.Item_ID + ',\'' + category_name + '\', ' + item.Slots_ID + ', true);"></div >';
			} else {
				itemString += '<div class="inv_equip_item_button clickable" onclick="equipItem(' + char_id + ', ' + item.Item_ID + ',\'' + category_name + '\');"></div >';
			}
			//itemString += '<div class="inv_equip_item_button clickable" onclick="equipItem(' + char_id + ', ' + item.Item_ID + ',\'' + category_name +  '\');"></div >';
			//itemString += '<div class="inv_equip_item_button clickable"></div >';
		}

		itemString += '</div>	\
			</div>\
		';

		parent.innerHTML += itemString;	
	});

	var test = document.getElementsByClassName('inv_add_item_container')[0];
	var test2 = document.getElementsByClassName('item_remove_container')[0];


	if(test != null){
		test.remove();
	} else if(test2 != null){
		test2.remove();
	}

	return;
}

function submitAddItemData(url, params, field_id_name='', char_id, slot_name){
	var http = new XMLHttpRequest();
	http.open('POST', url, true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			updateInvCategory(updateInvCategoryHelper, char_id, slot_name, '/dataserver/getItemsInSlot/' + char_id + '/' +  slot_name);
			weight_field = document.getElementById('character_weight');
			weight_field.innerHTML = this.response;
			isRemoveItemOpen = false;
		}
	}
	http.send(params);
}


function unequipItem(char_id, item_id, slot_name, slot_num=0, is_multiple_slots=false, keep_open=false){
	console.log('slot_num: ' + slot_num);
	// TODO: change later
	if(is_multiple_slots){
		// Determine which slot to add the item to
		try {
			//displayMultiSlot(char_id, item_id, slot_name, true);
			displayMultiSlot(char_id, item_id, slot_name, slot_num);
		} catch(e) {
			console.error(e);
		}
	} else {
		equipItemChangeSubmit('/character/item/unequip/', char_id, item_id, slot_name, slot_num, keep_open, true);
	}
}

const multi_slot_name_map = new Map([
	['Trinket', 0],
	['Ring', 1],
	['Item', 2],
	['Weapon', 3]
])

function equipItem(char_id, item_id, slot_name, slot_num=0, is_multiple_slots=false, keep_open=false){
	console.log('slot_num: ' + slot_num + ', slot_name: ' + slot_name);
	// TODO: change later
	if(is_multiple_slots){
		// Determine which slot to add the item to
		try {
			//displayMultiSlot(char_id, item_id, slot_name);
			displayMultiSlot(char_id, item_id, slot_name, slot_num);
		} catch(e) {
			console.error(e);
		}
	} else {
		equipItemChangeSubmit('/character/item/equip/', char_id, item_id, slot_name, slot_num, keep_open, false);
	}
}

function displayMultiSlot(char_id, item_id, slot_name, slot_num=0, is_unequip=false){
	var multi_slot_num = multi_slot_name_map.get(slot_name);

	// I would perfer to use a enum here in the future....
	switch(multi_slot_num){
		case 0: case 1: case 2:
			multipleSlotsInsert(char_id, item_id, 2, slot_num, is_unequip);
			break;
		case 3:
			multipleSlotsInsert(char_id, item_id, 4, slot_num, is_unequip);
			break;
		default:
			throw "Invaild slot name";
	}
}


function multipleSlotsInsert(char_id, item_id, number_of_slots, slot_num, is_unequip=false){
	var parentElement = document.getElementById('inv_item_' + item_id).parentElement;

	if(number_of_slots < 1 || number_of_slots === 3 || number_of_slots > 4){
		throw "Invaild number of slots passed.";
	}

	var ccd = new ChangeData(char_id, '/dataserver/getCurrentEquipedItems/' + char_id + '/' + slot_num, 'json', item_id, '');
	ccd.dataCall(changeNameLater);
}

function changeNameLater(char_id, response, item_id, b=null){
	var items_html = '<div style="display: flex; flex-direction: row;">';

	var i = 0;

	response.items.forEach(element => {
		var img_src_route = '/static/images/items/';
		
		if(element.Item_ID > 0){
			img_src_route = '/imageserver/item/';
		}

		var side = 'left';

		if(i % 4 > 1)	{
			side = 'right';
		}	


		if(i % 2 === 0){
			items_html += '<div class="equipment_side" style="height: auto;">';
		} 
		
		items_html += '\
		<div class="equipment_row" style="display: flex; flex-direction: column; height: auto;">\
			<div id="equipment_multi_' + response.slot_name + (i + 1) + '" class="equipment_' + side + '_item equipment_item">';

		var equipment_item_img_html_temp = '<div class="equipment_' + side + '_img">\
			<img id="equipment_Weapon_image" src="' + img_src_route + element.Item_Picture + '" alt="Weapon" />\
		</div>';

		if(side === 'left'){
			items_html += equipment_item_img_html_temp;
		}
		
		items_html += '<div class="equipment_' + side + '_item_name">\
				<h2  id="equipment_Weapon_text"	style="color: ' + element.Rarities_Color + ';">\
					' + element.Item_Name + '\
				</h2>\
			</div>'

		if(side === 'right'){
			items_html += equipment_item_img_html_temp;
		}
		items_html += '</div>';

		items_html += '<div class="inv_multi_item_equip_container">\
						<div class="inv_multi_item_equip_container_button inv_equip_item_button"\
							onclick="equipItem(' + char_id + ',' + item_id + ',\'' + response.slot_name + '\',' + (i + 1) + ', ' + false + ', ' + true  + ');"\
						></div>\
						<div class="inv_multi_item_equip_container_button inv_unequip_item_button"\
							onclick="unequipItem(' + char_id + ',' + item_id + ',\'' + response.slot_name + '\',' + (i + 1) + ', ' + false + ', ' + true  + ');"\
						></div>\
					</div>';

		items_html += '</div>';


		if(i % 2 == 1){
			items_html += '</div>';
		}	
			/* <div class="inv_add_item_row_item">\
				<div class="inv_add_item_input">\
					<p>asdfasdfasdfasdfasdf</p\
					<input type="checkbox" name="' + element.Item_ID + '" onclick="enable_input(\'' + element.Item_ID + '.amount\');">\
					<input type="number" name="' + element.Item_ID + '.amount" min="1" value="1" disabled>\
				</div>\
				<div class="inv_add_item_data">\
					<img src="/dataserver/imageserver/item/' + element.Item_Picture + '"/>\
					<h2 style="color:' + element.Rarities_Color + ';">' + element.Item_Name + '</h2>\
				</div>\
			</div>\
		'*/
		i++;
	});
	
	items_html += '</div>';

	var html = '\
		<div class="inv_add_item_container">\
			<div class="inv_add_item_header">\
				<h1>' + response.slot_name + '<h1>\
			</div>\
			' + items_html + '\
			<div class="inv_add_item_buttons">\
				<div class="clickable" onclick="cancelAddItem();">\
					<h4 style="color: white;">Cancel</h4>\
				</div>\
			</div>\
		</div>\
		';

	document.getElementsByClassName('inv_container')[0].innerHTML += html;
}


function equipItemChangeSubmit(url_prefix, char_id, item_id, slot_name="", slot_num=0, keep_open=false, unequip=false){
	// Send update to server
	submitEquipChange(url_prefix + char_id + '/' + item_id + '/' + slot_num, char_id, item_id, keep_open, slot_name, slot_num, unequip);
}

function submitEquipChange(url, char_id, item_id, keep_open, slot_name, slot_num, unequip){
	var http = new XMLHttpRequest();
	http.onreadystatechange = function(){ 
		if(http.readyState == 4 && http.status == 200) {
			try {
				if (this.response != null && this.response.error.type !== "None") {
					var error_type = this.response.error.type;
					if (error_type === "equip_error") {
						alert("An error occured: " + this.response.error.message);
						return;
					} else if (error_type === "unequip_error") {
						var prompt_response = confirm(this.response.error.message);
						if (prompt_response) {
							submitEquipChange(url + "/1", char_id, item_id, keep_open, slot_name, slot_num, unequip);
						}
						return;
					}
				}
			} catch (error) {
				console.error(error);
			}
			
			// TODO: error handling
			var _slot_name = this.response.item_data[0].slot_name;
			var _mod_slot_name = this.response.item_data[0].modified_slot_name;

			this.response.item_data.forEach(item_data => {
				// Update item picture and name in equipment
				updateEquipedItemName(item_data);
				updateEquipedItemPicture(item_data);
			});

			// Update stats
			updateCharacterStats(this.response.character_data, this.response.stat_modifiers);

			// Change button to equip button
			updateInvCategory(updateInvCategoryHelper, char_id, _slot_name, '/dataserver/getItemsInSlot/' + char_id + '/' +  _slot_name, keep_open);
			//invertEquipButton(char_id, item_id);

			if(keep_open){
				console.log('slot_num: ' + slot_num + ', slot_name: ' + slot_name);
				updateMultiSlotItem(item_id, slot_name, slot_num, unequip);
			}
		}
	}

	http.open("GET", url, true);
	http.responseType = 'json'; 
	http.send();
	return;
}

function updateEquipedItemPicture(item_data, use_default_image = false){
	var img_element = document.getElementById('equipment_' + item_data.modified_slot_name + '_image');

	var static_item_loc = '/static/images/items/';
	var extention_type = '.png';

	var new_src = static_item_loc + item_data.slot_name + extention_type;

	if(item_data.slot_name === 'Weapon'){
		try{
			var s = String(item_data.modified_slot_name);
			var l = s.length
			var temp = s.substr(l - 1, l);
			var image_name = '';
			if(temp % 2 === 0){
				image_name = 'Off_Hand';
			} else {
				image_name = 'Main_Hand'; 
			}

			new_src = static_item_loc + image_name + extention_type; 
		} catch (e){
			console.error(e);
		}
	}

	/* if(!use_default_image){
		new_src = '/dataserver/imageserver/item/' + response.item_data['picture'];
	} */
	if(item_data.picture != 'null'){
		new_src = '/imageserver/item/' + item_data.picture;
	}
	
	img_element.setAttribute('src', new_src);
}

function updateEquipedItemName(item_data, use_default_data=false){
	var name_element = document.getElementById('equipment_' + item_data.modified_slot_name + '_text');

	var new_name = item_data.slot_name;

	if(item_data.slot_name === 'Weapon'){
		try{
			var s = String(item_data.modified_slot_name);
			var l = s.length
			var temp = s.substr(l - 1, l);
			var end_num = (Math.floor(temp / 3) + 1);
			var slot_name_main_string = '';
			if(temp % 2 === 0){
				slot_name_main_string = 'Off Hand ';
			} else {
				slot_name_main_string = 'Main Hand '; 
			}

			new_name = slot_name_main_string + end_num; 
		} catch (e){
			console.error(e);
		}
	}

	var color = '#606060';

	/* if(!use_default_data){
		new_name = response.item_data['name'];
		color = response.item_data['color'];
	} */
	if(item_data.name != 'null'){
		new_name = item_data.name;
	}

	if (item_data.color != 'null'){
		color = item_data.color;
	}
	
	name_element.innerHTML = new_name;
	name_element.setAttribute('style', 'color: ' + color + ';');
}

function updateCharacterStats(char_data, stat_modifiers){
	var prefix = 'character_';

	var ids = [
		'max_hp', 'ac', 'max_weight',
		'str', 'dex', 'con', 'int', 'wis', 'cha'
	];
/* 	var ids = [
		'max_hp', 'ac', 'initiative', 'attack_bonus', 'max_weight',
		'str', 'dex', 'con', 'int', 'wis', 'cha'
	]; */
	
	var mod_ids = [
		'str_mod', 'dex_mod', 'con_mod', 'int_mod', 'wis_mod', 'cha_mod', 
	];

	ids.forEach(id => {
		var fullId = prefix + id;
		console.log(fullId + ', ' + char_data[id]);
		document.getElementById(fullId).innerHTML = char_data[id];
	});	

	mod_ids.forEach(id => {
		var fullId = prefix + id;
		console.log(fullId + ', ' + char_data[id]);
		document.getElementById(fullId).innerHTML = stat_modifiers[id];
	})
}

function invertEquipButton(char_id, item_id){
	var itemDiv = document.getElementById('inv_item_' + item_id);

	var itemParentDiv = itemDiv.parentElement;

	var unequipClassName = 'inv_unequip_item_button';
	var equipClassName = 'inv_equip_item_button';

	var currentDiv = itemParentDiv.getElementsByClassName(unequipClassName)[0];

	var newClass = '';
	var newFunctionCall = '';

	if(currentDiv != null){
		newClass = equipClassName;
		newFunctionCall = 'equipItem';
	} else {
		currentDiv = itemParentDiv.getElementsByClassName(equipClassName)[0];
		newClass = unequipClassName;
		newFunctionCall = 'unequipItem';
	}

	currentDiv.setAttribute('class', newClass + ' clickable');
	currentDiv.setAttribute('onclick', newFunctionCall + '(' + char_id + ',' + item_id + ');');

}

function updateMultiSlotItem(item_id, category_name, slot_position_number, is_unequiping=false){
	itemDetails(item_id, updateMultiSlotItemHelper, category_name, slot_position_number, is_unequiping);	
}

function itemDetails(item_id, callbackFunction, category_name, slot_position_number, is_unequiping){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			//itemInfo(element, this.responseText);
			callbackFunction(this.response, category_name, slot_position_number, is_unequiping);
			return
		}
	};
	
	const webpage = '/dataserver/itemDetails/' + item_id;
	xhttp.open("GET", webpage, true);
	
	xhttp.responseType = 'json';

	xhttp.send();
}

function updateMultiSlotItemHelper(response, category_name, slot_position_number, is_unequiping){
	var idString = 'equipment_multi_' + category_name + slot_position_number;
	console.log(idString);
	var el = document.getElementById(idString);
	console.log("resonse.name: " + response.name);
	var innerText = response.name;
	var textElement = el.getElementsByTagName('h2')[0];
	var imageElement = el.getElementsByTagName('img')[0];
	textElement.setAttribute('style', 'color: ' + response.color);
	if(is_unequiping){
		var endNum = slot_position_number;
		var prefix = category_name;
		var image_name = category_name + '.png';
		if(category_name === 'Weapon'){
			endNum = Math.ceil(slot_position_number / 2);
			if(slot_position_number % 2 == 0){
				prefix = 'Off Hand';
				image_name = 'Off_Hand.png'
			} else {
				prefix = 'Main Hand';
				image_name = 'Main_Hand.png'
			}
		}
		innerText = prefix + ' ' + endNum;
		textElement.setAttribute('style', 'color: #606060');
		imageElement.src = '/static/images/items/' + image_name;
	} else {
		imageElement.src = '/imageserver/item/' + response.picture;
	}
	console.log("inner_text: " + innerText);
	textElement.innerText = innerText;
	return;
}

function open_character_window(char_id){
	var _window = window.open('/character/' + String(char_id), '_blank');
	_window.focus();
}

function verify_user(user_id){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			//itemInfo(element, this.responseText);
			document.getElementById('user_' + user_id).getElementsByClassName('small_buttons')[0].remove();	
			return
		}
	};
	
	const webpage = '/admin/users/verify/' + user_id;
	xhttp.open("GET", webpage, true);

	xhttp.send();
}

function mark_read(note_id){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			//itemInfo(element, this.responseText);
			document.getElementById('notification_read_' + note_id).remove();	
			return
		}
	};
	
	const webpage = '/admin/notifications/markRead/' + note_id;
	xhttp.open("GET", webpage, true);

	xhttp.send();
}

function remove_note(note_id){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			//itemInfo(element, this.responseText);
			document.getElementById('notification_' + note_id).remove();	
			return
		}
	};
	
	const webpage = '/admin/notifications/remove/' + note_id;
	xhttp.open("GET", webpage, true);

	xhttp.send();
}

function remove_user(user_id, username){
	var un = prompt("Please enter the User's name, " + username + ", to DELETE permanently.", "");
	var params = 'user_id=' + user_id;
	if(un != null && un === username){
		var http = new XMLHttpRequest();
		http.open('POST', '/admin/users/remove', true);

		//Send the proper header information along with the request
		http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

		http.onreadystatechange = function() {
			//Call a function when the state changes.
			if(http.readyState == 4 && http.status == 200) {
				// do something here
				document.getElementById('user_' + user_id).remove();
			}
		}
		http.send(params);
	}
}

function make_user_admin(user_id, username){
	var un = prompt("Please enter the User's name, " + username + ", to promote to admin permanently.", "");
	var params = 'user_id=' + user_id;
	if(un != null && un === username){
		var http = new XMLHttpRequest();
		http.open('POST', '/admin/users/makeAdmin', true);

		//Send the proper header information along with the request
		http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

		http.onreadystatechange = function() {
			//Call a function when the state changes.
			if(http.readyState == 4 && http.status == 200) {
				// do something here
				document.getElementById('make_admin_button_' + username).remove();
			}
		}
		http.send(params);
	}
}
