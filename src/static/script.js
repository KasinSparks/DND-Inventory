var saveForLater = new Map([["", ""]]);

function equipmentItemDetails(charId, equipmentItemStr){
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

function itemDetailsPanel(itemID) {
	var htmlInner = document.getElementsByClassName("sub_inner_panel")[0];
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			htmlInner.innerHTML = htmlInner.innerHTML.concat(
				'<div class="itemfulldetail">' + getEquipmentItemDetailsHTML(this.response, 'closePrev()')
					+ '<div class="item_approved">Approved: ' + (this.response.approved == 1 ? 'True' : 'False') + '</div>\
                        <div class="verify_deny_buttons">\
                            <div class="small_buttons item_notification_button_pass clickable" onclick="item_acceptance(' + itemID + ', true);"></div>\
                            <div class="small_buttons item_notification_button_deny clickable" onclick="item_acceptance(' + itemID + ', false);"></div>\
                        </div>\
					</div>');
			return;
		}
	};
	
	const webpage = '/dataserver/itemFullDetails/' + itemID;
	xhttp.open("GET", webpage, true);
	
	xhttp.responseType = 'json';

	xhttp.send();
}

function closePrev() {
	document.getElementsByClassName("itemfulldetail")[0].remove();
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

function test2(){
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
	var equipmentItemDetailsHTML = '\
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
						<td colspan=2><h2>' + jsonData.item_damage_num_of_dices + ' d ' + jsonData.item_damage_num_of_dice_sides + ' ' + (jsonData.bonus_damage < 0 ? '' : '+') + jsonData.bonus_damage + '</h2></td>\
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
				}

				equipmentItemDetailsHTML += '<tr>\
					<td colspan=2><h2>AC:</h2></td>\
					<td colspan=2><h2>' + jsonData.ac + '</h2></td>\
				</tr>'
				 
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
				</tr>';
	if (jsonData.effect1_name !== "Effect1") {
		equipmentItemDetailsHTML += '<tr>\
				<td colspan=2><h2>' + jsonData.effect1_name + ':</h2></td>\
				<td colspan=2><h2>' + jsonData.effect1_description + '</h2></td>\
			</tr>';
	}
	if (jsonData.effect2_name !== "Effect2") {
		equipmentItemDetailsHTML += '<tr>\
				<td colspan=2><h2>' + jsonData.effect2_name + ':</h2></td>\
				<td colspan=2><h2>' + jsonData.effect2_description + '</h2></td>\
			</tr>';
	}
	
	equipmentItemDetailsHTML += '</table>\
		</div>\
		<div class="item_info_footer" onclick="' + function_call + ';">\
			<h1>X</h1>\
		</div>\
	</div>\
	';
	return equipmentItemDetailsHTML;
}

function accept_tos(){
	document.location = 'tos/accept';
	return;
}

function decline_tos(){
	redirect_after_seconds('../login', 10000);
	// TODO: make a better looking message
	document.getElementsByClassName('login_container')[0].innerHTML = '<p>Terms of Service have been declined.\n\nRedirecting in 10 seconds...</p>';
	return;
}

function redirect(location){
	document.location = location;
}

function redirect_after_seconds(location, milliseconds){
	setTimeout(function(){
		redirect(location);
	}, milliseconds);
}

function inv_tab(activeClass, activeButtonID){
	inv_inner_area_children = document.getElementsByClassName('inv_container_inner_area')[0].children;

	for(var i = 0; i < inv_inner_area_children.length; ++i){
		if(inv_inner_area_children[i].className === activeClass){
			inv_inner_area_children[i].removeAttribute('style');
			// TODO:
			//if (inv_inner_area_children[i].className === "inv_container_skills_section") {
				// update data, lazy way by coping local modifier data
				// TODO: change to update from server instead of local
			//	_update_skills_data();
			//}
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
	
	return;
}

/* Depercated */
/*
function _update_skills_data(){
	// get the modifier data locally
	var labels = ["str", "dex", "con", "int", "wis", "cha"];

}*/

function category_expand_and_collapse(categoryID, option, line_item_class, button_class){
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

function select_other_button(element_name=[], value){
	console.log(value);
	element_name.forEach(element => {
		if(value === "OTHER"){
			select_button_helper(element, '', 'true');
		} else {
			select_button_helper(element, 'display: none;');
		}
	});
}

function select_standard_button(element_name=[]){
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

class ChangeData{
	constructor(char_id, webpage, responseType, field_id_name, submit_route){
		this.char_id = char_id;
		this.webpage = webpage;
		this.responseType = responseType;
		this.field_id_name = field_id_name;
		this.submit_route = submit_route;
	}

	dataCall(callbackFunction=null, submit_route=this.submit_route, char_id=this.char_id, field_id_name=this.field_id_name){
		console.log(submit_route);
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
				
				callbackFunction(char_id, this.response, field_id_name, submit_route);
				return;
			}
		};
		
		xhttp.open("GET", this.webpage, true);
		
		xhttp.responseType = this.responseType;
	
		xhttp.send();
	
		return;
	}
	
	dropdown(char_id, dropdown_options, field_id_name, submit_route){
		var html_string = '<div class="char_item_val_change_container"><select id="new_value">';
		
		//console.log(submit_route);

		var field = document.getElementById(field_id_name);
		if(field == null){
			return;
		}

		isChangeCharDataOpen = true;

		dropdown_options.opts.forEach(element => {
			html_string += '<option value="' + element.id + '">' + element.name + '</option>';
		});

		html_string += '</select>\
							<button onclick="submitChanges(' + char_id + ',\'' + field_id_name + '\',' + '\'' + submit_route + '\',' + 0 + ');">Y</button>\
							<button onclick="abortChanges(\'' + field_id_name + '\');">X</button>\
							</div>';

		// Put the data in to html and insert it
		
		field.setAttribute('style', 'display: none;');
		field.parentElement.parentElement.innerHTML += html_string;
		

		return;
	}

	number(char_id, current_number, field_id_name, submit_route){
		var html_string = '<div class="char_item_val_change_container">';
		
		html_string += '<input type="number" id="new_value" value="' + current_number.current_value + '">';

		var field = document.getElementById(field_id_name);
		if(field == null){
			return;
		}

		isChangeCharDataOpen = true;

		html_string += '<button onclick="submitChanges(' + char_id + ',\'' + field_id_name + '\',' + '\'' + submit_route + '\',' + 1 + ');">Y</button>\
						<button onclick="abortChanges(\'' + field_id_name + '\');">X</button>\
						</div>';

		
		field.setAttribute('style', 'display: none;');
		field.parentElement.parentElement.innerHTML += html_string;
		

		return;
	}

	number_additional(char_id, current_number, field_id_name, submit_route){
		var html_string = '<div class="char_item_val_change_container">';

		html_string += '<div style="display: flex; width: 100%;">\
							<div class="stat_details"><h4>Base</h4><p>' + current_number.base + '</p></div>\
							<div class="stat_details"><h4>Additional</h4><p>' + current_number.additional + '</p></div>\
						</div>'
		
		html_string += '<input type="number" id="new_value" value="' + current_number.base + '">';

		var field = document.getElementById(field_id_name);
		if(field == null){
			return;
		}

		isChangeCharDataOpen = true;

		html_string += '<button onclick="submitChanges(' + char_id + ',\'' + field_id_name + '\',' + '\'' + submit_route + '\',' + 1 + ');">Y</button>\
						<button onclick="abortChanges(\'' + field_id_name + '\');">X</button>\
						</div>';

		
		field.setAttribute('style', 'display: none;');
		field.parentElement.parentElement.innerHTML += html_string;
		

		return;
	}

	image(char_id, dummy_data, field_id_name, submit_route){
		var html_string = '<div class="char_item_val_change_container">\
						<form method="post" enctype="multipart/form-data" action="' + submit_route + char_id + '">\
						<input name="image" type="file" id="new_value" accept="image/gif, image/jpeg, image/png, image/jpg">';

		var field = document.getElementById(field_id_name);
		if(field == null){
			return;
		}

		isChangeCharDataOpen = true;

		html_string += '<input type="submit", value="Y"/>\
						<button onclick="abortChanges(\'' + field_id_name + '\');">X</button>\
						</form></div>';

		
		field.setAttribute('style', 'display: none;');
		field.parentElement.innerHTML += html_string;
		

		return;
	}
	
	string_value(char_id, current_string, field_id_name, submit_route){
		var html_string = '<div class="char_item_val_change_container">\
		<input type="text" id="new_value" value="' + current_string.current_value + '">';

		var field = document.getElementById(field_id_name);
		if(field == null){
		return;
		}

		isChangeCharDataOpen = true;

		html_string += '<button onclick="submitChanges(' + char_id + ',\'' + field_id_name + '\',' + '\'' + submit_route + '\',' + 1 + ');">Y</button>\
				<button onclick="abortChanges(\'' + field_id_name + '\');">X</button>\
				</div>';


		field.setAttribute('style', 'display: none;');
		field.parentElement.parentElement.innerHTML += html_string;


		return;
	}	
}


var isChangeCharDataOpen = false;

function submitChanges(char_id, field_id_name, submit_route, callType=0){
	var element = document.getElementById('new_value');
	switch(callType){
		case 0:
			submitData(submit_route + char_id,
				'value=' + element.options[element.selectedIndex].value,
				field_id_name);
			break;
		case 1:
			submitData(submit_route + char_id, 'value=' + element.value,
				field_id_name, true);
			break;
		case 2:
			submitImage(submit_route + char_id, 'image=' + element.value,
				field_id_name);
			break;
		default:
			console.log('Value:: ' + element.value);
	}
	abortChanges(field_id_name);
	return
}

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
}

function submitImage(url, params, field_id_name){
	var http = new XMLHttpRequest();
	http.open('POST', url, true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			//console.log(http.responseText);
			//document.getElementById(field_id_name).innerHTML = http.responseText;
		}
	}
	http.send(params);
}

function abortChanges(field_id_name){
	if(isChangeCharDataOpen){
		document.getElementById(field_id_name).setAttribute('style', '');
		document.getElementsByClassName('char_item_val_change_container')[0].remove();
	}
	isChangeCharDataOpen = false;
	return;
}


function changeClass(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getClassName/' + char_id,
			'json', 'character_class', '/character/edit/class/');
		ccd.dataCall(ccd.string_value);
	}
}

function changeRace(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getRaceName/' + char_id,
			'json', 'character_race', '/character/edit/race/');
		ccd.dataCall(ccd.string_value);
	}
}

function changeLevel(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getLevel/' + char_id, 'json',
			'character_level', '/character/edit/level/');
		ccd.dataCall(ccd.number);
	}
}

function changeImage(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/dummyCall', 'json',
			'character_image', '/character/edit/image/');
		ccd.dataCall(ccd.image);
	}
}

function changeHealth(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getHealth/' + char_id, 'json',
			'character_hp', '/character/edit/health/')
		ccd.dataCall(ccd.number);
	}
}

function changeMaxHealth(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getMaxHealth/' + char_id, 'json',
			'character_max_hp', '/character/edit/maxhealth/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeAC(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getAC/' + char_id, 'json',
			'character_ac', '/character/edit/ac/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeInitiative(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getInitiative/' + char_id, 'json',
			'character_initiative', '/character/edit/initiative/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeAttackBonus(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getAttackBonus/' + char_id, 'json',
			'character_attack_bonus', '/character/edit/attackBonus/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeAlignment(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getAlignmentOptions',
			'json', 'character_alignment', '/character/edit/alignment/');
		ccd.dataCall(ccd.dropdown);
	}
}

function changeCurrency(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getCurrency/' + char_id, 'json',
			'character_currency', '/character/edit/currency/')
		ccd.dataCall(ccd.number);
	}
}

function changeStr(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getStr/' + char_id, 'json',
			'character_str', '/character/edit/str/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeDex(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getDex/' + char_id, 'json',
			'character_dex', '/character/edit/dex/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeCon(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getCon/' + char_id, 'json',
			'character_con', '/character/edit/con/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeInt(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getInt/' + char_id, 'json',
			'character_int', '/character/edit/int/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeWis(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getWis/' + char_id, 'json',
			'character_wis', '/character/edit/wis/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeCha(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeData(char_id, '/dataserver/getCha/' + char_id, 'json',
			'character_cha', '/character/edit/cha/')
		ccd.dataCall(ccd.number_additional);
	}
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

function item_acceptance(item_id, status){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			//itemInfo(element, this.responseText);
			//document.getElementById('notification_' + note_id).remove();
			var s = 'Approved: ' + (status == 1 ? 'True' : 'False');
			console.log("yse");
			document.getElementsByClassName('item_approved')[0].innerHTML = s;
			return
		}
	};
	
	int_status = 0;
	if (status) {
		int_status = 1;
	}
	const webpage = '/admin/items/approveItem/' + item_id + '/' + int_status;
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

/* Depercated */
/*
function modify_skill(char_id, amount, skill_name, field_id_name){
	var params = 'char_id=' + char_id + '&skill_name=' + skill_name + '&amount=' + amount;
	var http = new XMLHttpRequest();
	http.open('POST', '/character/skills/edit', true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			document.getElementById(field_id_name).getElementsByTagName("h2")[0].innerHTML = this.response;
		}
	}
	http.send(params);
}*/
var ability_header_old = "";
function add_ability(char_id){
	var ability_test = null;
	try{
		var ability_test = [
			document.getElementsByClassName("new_ability_input"),
			document.getElementsByClassName("edit_ability_input")
		];
	} catch (error) {
		// an edit or create is NOT already open
		// ignore and go on
	}

	for(var i = 0; i < ability_test.length; ++i){
		if (ability_test[i] !== null && ability_test[i].length > 0) {
			console.error("Ability modification window is already open. Please close existing ability modification window before continuing.");
			
			alert("Ability modification window is already open. Please close existing ability modification window before continuing.");

			return;
		}
	}

	var ability_header = document.getElementById("ability_header");
	ability_header_old = ability_header.innerHTML;
	var new_html = '<div class="new_ability_input">\
			<label for"ability_name">Ability Name: </label>\
			<input id="ability_name" name="ability_name" type="text" value="" maxlength="63" onkeyup="valid_char(event, \'ability_name\');">\
			<br>\
			<label for"ability_description">Ability Description: </label>\
			<textarea id="ability_description" name="ability_description" rows="5" columns="100" maxlength="500"></textarea>\
			<br>\
			<label for"ability_damage">Ability Damage: </label>\
			<input id="ability_damage" name="ability_damage" type="text", value="" maxlength="63">\
			<br>\
			<label for"ability_type">Ability Type: </label>\
			<input id="ability_type" name="ability_type" type="text", value="" maxlength="63">\
			<br>\
			<button onclick="submit_ability(' + char_id + ', \'/character/abilities/add\')">Submit</button>\
			<button onclick="cancel_add_ability()">Cancel</button>\
		</div>';
	ability_header.innerHTML = new_html;
}

var skill_header_old = "";
function add_skill(char_id){
	var skill_test = null;
	try{
		var skill_test = [
			document.getElementsByClassName("new_skill_input"),
			document.getElementsByClassName("edit_skill_input")
		];
	} catch (error) {
		// an edit or create is NOT already open
		// ignore and go on
	}

	for(var i = 0; i < skill_test.length; ++i){
		if (skill_test[i] !== null && skill_test[i].length > 0) {
			console.error("Misc. modification window is already open. Please close existing misc. modification window before continuing.");
			
			alert("Misc. modification window is already open. Please close existing misc. modification window before continuing.");

			return;
		}
	}

	var skill_header = document.getElementById("skills_header");
	skill_header_old = skill_header.innerHTML;
	var new_html = '<div class="new_skill_input">\
			<label for"skill_name">Name: </label>\
			<input id="skill_name" name="skill_name" type="text" value="" maxlength="63" onkeyup="valid_char(event, \'skill_name\');">\
			<br>\
			<label for"skill_description">Description: </label>\
			<textarea id="skill_description" name="skill_description" rows="5" columns="100" maxlength="500"></textarea>\
			<br>\
			<button onclick="submit_skill(' + char_id + ', \'/character/skill/add\')">Submit</button>\
			<button onclick="cancel_add_skill()">Cancel</button>\
		</div>';
	skill_header.innerHTML = new_html;
}

function submit_ability(char_id, url, old_ability_name=null, ability_name=null, ability_description=null, ability_damage=null, ability_type=null){
	if(ability_name === null){
		var ability_name = document.getElementById("ability_name").value;
	}
	if(ability_description === null){
		var ability_description = document.getElementById("ability_description").value;
	}
	if(ability_damage === null){
		var ability_damage = document.getElementById("ability_damage").value;
	}
	if(ability_type === null){
		var ability_type = document.getElementById("ability_type").value;
	}
	
	var params = 'char_id=' + char_id + '&ability_name=' + ability_name + '&ability_description=' + ability_description + '&old_ability_name=' + old_ability_name + '&ability_damage=' + ability_damage + '&ability_type=' + ability_type;
	var http = new XMLHttpRequest();
	http.open('POST', url, true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			// TODO
			//document.getElementById(field_id_name).getElementsByTagName("h2")[0].innerHTML = this.response;
			if(this.response.substring(0, 5) === "ERROR"){
				console.error(this.response);
				alert(this.response);
				return;
			}
			
					
			var json_data = JSON.parse(this.response);
			var char_id = json_data.char_id;
			var old_name = json_data.old_name;

			if(old_name !== 'null'){
				// edit ability
				cancel_edit_ability(old_name);
				var line_item = document.getElementById("abilities_" + old_name);
				line_item.setAttribute("id", line_item.getAttribute("id").replace(old_name, json_data.Ability_Name));
				line_item.getElementsByClassName("ability_name")[0].innerHTML = json_data.Ability_Name;
				var _old_des_el = document.getElementById("ability_" + old_name + "_description")
				_old_des_el.innerHTML = json_data.Ability_Description;
				_old_des_el.setAttribute("id", _old_des_el.getAttribute("id").replace(old_name, json_data.Ability_Name));
				
				var _old_damage_el = document.getElementById("ability_" + old_name + "_damage")
				_old_damage_el.innerHTML = json_data.Ability_Damage;
				_old_damage_el.setAttribute("id", _old_damage_el.getAttribute("id").replace(old_name, json_data.Ability_Name));

				var _old_type_el = document.getElementById("ability_" + old_name + "_type")
				_old_type_el.innerHTML = json_data.Ability_Type;
				_old_type_el.setAttribute("id", _old_type_el.getAttribute("id").replace(old_name, json_data.Ability_Name));

				var _edit_button = line_item.getElementsByClassName("ability_edit_button")[0];
				_edit_button.setAttribute("onclick", _edit_button.getAttribute("onclick").replace(old_name, json_data.Ability_Name));
				var _remove_button = line_item.getElementsByClassName("ability_remove_button")[0];
				_remove_button.setAttribute("onclick", _remove_button.getAttribute("onclick").replace(old_name, json_data.Ability_Name));
				var _expand_button = line_item.getElementsByClassName("inv_category_button")[0];
				_expand_button.setAttribute("onclick", _expand_button.getAttribute("onclick").replace(old_name, json_data.Ability_Name));
			} else {
				// new ability
				var i_html = document.getElementsByClassName("inv_container_abilities_section")[0];

				i_html.innerHTML += add_ability_html(char_id, json_data.Ability_Name, json_data.Ability_Description, json_data.Ability_Damage, json_data.Ability_Type);
				console.log(this.response);	
				cancel_add_ability();
			}

		}
	}
	http.send(params);
}

function submit_skill(char_id, url, old_skill_name=null, skill_name=null, skill_description=null){
	if(skill_name === null){
		var skill_name = document.getElementById("skill_name").value;
	}
	if(skill_description === null){
		var skill_description = document.getElementById("skill_description").value;
	}
	
	var params = 'char_id=' + char_id + '&skill_name=' + skill_name + '&skill_description=' + skill_description + '&old_skill_name=' + old_skill_name; 
	var http = new XMLHttpRequest();
	http.open('POST', url, true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			// TODO
			//document.getElementById(field_id_name).getElementsByTagName("h2")[0].innerHTML = this.response;
			if(this.response.substring(0, 5) === "ERROR"){
				console.error(this.response);
				alert(this.response);
				return;
			}
			
					
			var json_data = JSON.parse(this.response);
			var char_id = json_data.char_id;
			var old_name = json_data.old_name;

			if(old_name !== 'null'){
				// edit skill
				cancel_edit_skill(old_name);
				var line_item = document.getElementById("skills_" + old_name);
				line_item.setAttribute("id", line_item.getAttribute("id").replace(old_name, json_data.Skill_Name));
				line_item.getElementsByClassName("skill_name")[0].innerHTML = json_data.Skill_Name;
				var _old_des_el = document.getElementById("skill_" + old_name + "_description")
				_old_des_el.innerHTML = json_data.Skill_Description;
				_old_des_el.setAttribute("id", _old_des_el.getAttribute("id").replace(old_name, json_data.Skill_Name));
				
				var _edit_button = line_item.getElementsByClassName("skill_edit_button")[0];
				_edit_button.setAttribute("onclick", _edit_button.getAttribute("onclick").replace(old_name, json_data.Skill_Name));
				var _remove_button = line_item.getElementsByClassName("skill_remove_button")[0];
				_remove_button.setAttribute("onclick", _remove_button.getAttribute("onclick").replace(old_name, json_data.Skill_Name));
				var _expand_button = line_item.getElementsByClassName("inv_category_button")[0];
				_expand_button.setAttribute("onclick", _expand_button.getAttribute("onclick").replace(old_name, json_data.Skill_Name));
			} else {
				// new skill
				var i_html = document.getElementsByClassName("inv_container_skills_section")[0];

				i_html.innerHTML += add_skill_html(char_id, json_data.Skill_Name, json_data.Skill_Description);
				console.log(this.response);	
				cancel_add_skill();
			}

		}
	}
	http.send(params);
}

function delete_ability(char_id, ability_name){
	var params = 'char_id=' + char_id + '&ability_name=' + ability_name;
	var http = new XMLHttpRequest();
	http.open('POST', 'abilities/delete', true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			if (this.response !== "200") {
				alert("Ability could not be deleted");
				return;
			}
			document.getElementById("abilities_" + ability_name).remove();
		}
	}
	http.send(params);
}

function delete_skill(char_id, skill_name){
	var params = 'char_id=' + char_id + '&skill_name=' + skill_name;
	var http = new XMLHttpRequest();
	http.open('POST', 'skill/delete', true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			if (this.response !== "200") {
				alert("Skill could not be deleted");
				return;
			}
			document.getElementById("skills_" + skill_name).remove();
		}
	}
	http.send(params);
}

function add_ability_html(char_id, ability_name, ability_description, ability_damage, ability_type){
	var html = '<div id="abilities_' + ability_name + '" class="inv_category">\
		<div class="inv_category_line">\
			<div class="inv_line_inner">\
				<div class="ability_remove_button clickable" onclick="delete_ability(' + char_id + ', \'' + ability_name + '\');"></div>\
				<h2 class="ability_name">' + ability_name + '</h2>\
				<div class="skills_mod_buttons">\
					<div class="ability_edit_button clickable" onclick="edit_ability(' + char_id + ', \'' + ability_name + '\');"></div>\
					<div style="width: 8px;"></div>\
					<div class="inv_category_expand_button inv_category_button clickable" onclick="category_expand_and_collapse(\'abilities_' + ability_name + '\', \'expand\', \'inv_line_item\', \'inv_category_button\');"></div >\
				</div>\
			</div>\
		</div>\
		<div class="inv_line_item" style="display: none;">\
			<div class="inv_line_inner">\
				<div class="ability_description">\
					<h2 class="ability_info_field">Description: </h2>\
					<h2 id="ability_' + ability_name + '_description">' + ability_description + '</h2>\
				</div>\
			</div>\
		</div>\
		<div class="inv_line_item" style="display: none;">\
			<div class="inv_line_inner">\
				<div class="ability_description">\
					<h2 class="ability_info_field">Damage: </h2>\
					<h2 id="ability_' + ability_name + '_damage">' + ability_damage + '</h2>\
				</div>\
			</div>\
		</div>\
		<div class="inv_line_item" style="display: none;">\
			<div class="inv_line_inner">\
				<div class="ability_description">\
					<h2 class="ability_info_field">Type: </h2>\
					<h2 id="ability_' + ability_name + '_type">' + ability_type + '</h2>\
				</div>\
			</div>\
		</div>\
	</div>'
	return html;
}

var edit_ability_header_old = "";
function edit_ability(char_id, old_ability_name){
	var ability_test = null;
	try{
		var ability_test = [
			document.getElementsByClassName("new_ability_input"),
			document.getElementsByClassName("edit_ability_input")
		];
	} catch (error) {
		// an edit or create is NOT already open
		// ignore and go on
	}

	for(var i = 0; i < ability_test.length; ++i){
		if (ability_test[i] !== null && ability_test[i].length > 0) {
			console.error("Ability modification window is already open. Please close existing ability modification window before continuing.");
			
			alert("Ability modification window is already open. Please close existing ability modification window before continuing.");

			return;
		}
	}

	var ability_header = document.getElementById("abilities_" + old_ability_name);
	var old_ability_description = document.getElementById("ability_" + old_ability_name + "_description").innerHTML;
	var old_ability_type = document.getElementById("ability_" + old_ability_name + "_type").innerHTML; 
	var old_ability_damage = document.getElementById("ability_" + old_ability_name + "_damage").innerHTML; 
	edit_ability_header_old = ability_header.innerHTML;
	var new_html = '<div class="edit_ability_input">\
			<label for"ability_name">Ability Name: </label>\
			<input id="ability_name" name="ability_name" type="text" value="' + old_ability_name + '" maxlength="63" onkeyup="valid_char(event, \'ability_name\');">\
			<br>\
			<label for"ability_description">Ability Description: </label>\
			<textarea id="ability_description" name="ability_description" rows="5" columns="100" maxlength="500">' + old_ability_description + '</textarea>\
			<br>\
			<label for="ability_damge">Ability Damage: </label>\
			<input id="ability_damage" name="ability_damage" type="text", value="' + old_ability_damage + '" maxlength="63">\
			<br>\
			<label for="ability_type">Ability Type: </label>\
			<input id="ability_type" name="ability_type" type="text", value="' + old_ability_type + '" maxlength="63">\
			<br>\
			<button onclick="submit_ability(' + char_id + ', \'/character/abilities/edit\', \'' + old_ability_name + '\')">Submit</button>\
			<button onclick="cancel_edit_ability(\'' + old_ability_name + '\')">Cancel</button>\
		</div>';
	ability_header.innerHTML = new_html;
}

function cancel_add_ability(){
	_cancel_mod_ability("ability_header", ability_header_old);
	ability_header_old = "";
}

function cancel_edit_ability(name){
	_cancel_mod_ability("abilities_" + name, edit_ability_header_old);
	edit_ability_header_old = "";
}

function _cancel_mod_ability(parent_div, old_html){
	var ability_header = document.getElementById(parent_div);
	ability_header.innerHTML = old_html;
}

function add_skill_html(char_id, skill_name, skill_description){
	var html = '<div id="skills_' + skill_name + '" class="inv_category">\
		<div class="inv_category_line">\
			<div class="inv_line_inner">\
				<div class="skill_remove_button clickable" onclick="delete_skill(' + char_id + ', \'' + skill_name + '\');"></div>\
				<h2 class="skill_name">' + skill_name + '</h2>\
				<div class="skills_mod_buttons">\
					<div class="skill_edit_button clickable" onclick="edit_skill(' + char_id + ', \'' + skill_name + '\');"></div>\
					<div style="width: 8px;"></div>\
					<div class="inv_category_expand_button inv_category_button clickable" onclick="category_expand_and_collapse(\'skills_' + skill_name + '\', \'expand\', \'inv_line_item\', \'inv_category_button\');"></div >\
				</div>\
			</div>\
		</div>\
		<div class="inv_line_item" style="display: none;">\
			<div class="inv_line_inner">\
				<div class="skill_description">\
					<h2 class="skill_info_field">Description: </h2>\
					<h2 id="skill_' + skill_name + '_description">' + skill_description + '</h2>\
				</div>\
			</div>\
		</div>\
	</div>'
	return html;
}

var edit_skill_header_old = "";
function edit_skill(char_id, old_skill_name){
	var skill_test = null;
	try{
		var skill_test = [
			document.getElementsByClassName("new_skill_input"),
			document.getElementsByClassName("edit_skill_input")
		];
	} catch (error) {
		// an edit or create is NOT already open
		// ignore and go on
	}

	for(var i = 0; i < skill_test.length; ++i){
		if (skill_test[i] !== null && skill_test[i].length > 0) {
			console.error("Misc. modification window is already open. Please close existing misc modification window before continuing.");
			
			alert("Misc. modification window is already open. Please close existing misc modification window before continuing.");

			return;
		}
	}

	var skill_header = document.getElementById("skills_" + old_skill_name);
	var old_skill_description = document.getElementById("skill_" + old_skill_name + "_description").innerHTML;

	edit_skill_header_old = skill_header.innerHTML;
	var new_html = '<div class="edit_skill_input">\
			<label for"skill_name">Name: </label>\
			<input id="skill_name" name="skill_name" type="text" value="' + old_skill_name + '" maxlength="63" onkeyup="valid_char(event, \'skill_name\');">\
			<br>\
			<label for"skill_description">Description: </label>\
			<textarea id="skill_description" name="skill_description" rows="5" columns="100" maxlength="500">' + old_skill_description + '</textarea>\
			<br>\
			<button onclick="submit_skill(' + char_id + ', \'/character/skill/edit\', \'' + old_skill_name + '\')">Submit</button>\
			<button onclick="cancel_edit_skill(\'' + old_skill_name + '\')">Cancel</button>\
		</div>';
	skill_header.innerHTML = new_html;
}

function cancel_add_skill(){
	_cancel_mod_ability("skills_header", skill_header_old);
	skill_header_old = "";
}

function cancel_edit_skill(name){
	_cancel_mod_ability("skills_" + name, edit_skill_header_old);
	edit_skill_header_old = "";
}

function item_create_slot_change(slot_name=null){
	var sel_val = "";
	if (slot_name === null) {
		selector = document.getElementsByName("slot")[0];
		sel_val = selector.value.toLowerCase();
	} else {
		sel_val = slot_name.toLowerCase();
	}
	var wield_req_div = document.getElementById("wield_req");

	var wield_new_style = "display: none;";

	if (sel_val === "weapon") {
		// show wield requirements
		wield_new_style = wield_req_div.getAttribute("style").replace("display: none;", "");
		_set_element_style(wield_req_div, wield_new_style);
	} else {
		_set_element_style_to_display_none(wield_req_div);
	}
}

function _element_style_has_display_none(element){
	return element.getAttribute("style").includes("display: none;");
}

function _set_element_style_to_display_none(element){
	if (_element_style_has_display_none(element)) { return; }
	_set_element_style(element, element.getAttribute("style") + " display: none;");
}

function _set_element_style(element, new_style){
	element.setAttribute("style", new_style);
}

function detect_item_type(slot_name){
	item_create_slot_change(slot_name);
}

function is_allowed_string(str_val){
    _banned_chars = ['\'', '\"', '?', ',', '*', ';'];
	_str = String(str_val);

	for (var i = 0; i < _str.length; ++i) {
		for (var j = 0; j < _banned_chars.length; ++j) {
			if (_str[i] === _banned_chars[j]) {
				return false;
			}
		}
	}

	return true;
}

function valid_char(event, name){
	var key_pressed = event.key;
	if (!is_allowed_string(key_pressed)){
		alert("Invalid character: " + key_pressed);
		var _input = document.getElementsByName(name)[0];
		_input.value = replace_all(String(key_pressed), _input.value); 
	}
}

function replace_all(replace_char, from_string){
	var _new_str = "";
	for (var i = 0; i < from_string.length; ++i) {
		if (from_string[i] !== replace_char) {
			_new_str += from_string[i];	
		}
	}
	return _new_str;
}
