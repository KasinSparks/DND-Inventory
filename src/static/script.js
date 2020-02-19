var saveForLater = new Map([["", ""]]);

function test(str){
	var hmtlInner = document.getElementsByClassName('equipment')[0];
	console.debug('here');
	saveForLater[0] = [str, hmtlInner.innerHTML];
	console.debug(saveForLater);
	hmtlInner.innerHTML = '<p>test</p><div style="width: 30%; min-width: 290px; max-width: 302px; height: 100%; background-color: #FFFFFF;" onclick="test2();"><div style="width: 100%; height: 100%;">test asdfsaa</div></div>';
	return;
}



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

function getEquipmentItemDetailsHTML(jsonData){
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
				</tr>\
				<tr>\
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
					<td></td>\
					<td><h2 class="weight">Weight:</h2></td>\
					<td><h2 class="weight">' + jsonData.weight + '</h2></td>\
					<td></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2>' + jsonData.effect1_name + ':</h2></td>\
					<td colspan=2><h2>' + jsonData.effect1_description + '</h2></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2>' + jsonData.effect2_name + ':</h2></td>\
					<td colspan=2><h2>' + jsonData.effect2_description + '</h2></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2>Number of Damage Dices:</h2></td>\
					<td colspan=2><h2>' + jsonData.item_damage_num_of_dices + '</h2></td>\
				</tr>\
				<tr>\
					<td colspan=2><h2>Number of Damage Dice Sides:</h2></td>\
					<td colspan=2><h2>' + jsonData.item_damage_num_of_dice_sides + '</h2></td>\
				</tr>\
			</table>\
		</div>\
		<div class="item_info_footer" onclick="test2();">\
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

function category_expand_and_collapse(categoryID, option){
	inv_cat = document.getElementById(categoryID); 

	inv_line_items = inv_cat.getElementsByClassName('inv_line_item');

	inv_category_button = inv_cat.getElementsByClassName('inv_category_button')[0];

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

function select_other_button(element_name){
	select_button_helper(element_name, '');
}

function select_standard_button(element_name){
	select_button_helper(element_name, 'display: none;');
}

function select_button_helper(element_name, style_attribute){
	document.getElementsByName(element_name)[0].setAttribute('style', style_attribute);
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

		dropdown_options.classes.forEach(element => {
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
		<input type="number" id="new_value" value="' + current_number.level + '">';

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
		var ccd = new ChangeData(char_id, '/dataserver/getClassOptions',
			'json', 'character_class', '/character/edit/class/');
		ccd.dataCall(ccd.dropdown);
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
					<img src="/dataserver/imageserver/item/' + element.Item_Picture + '"/>\
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

function updateInvCategory(callbackFunction = null, char_id, category_name, webpage){
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
			
			callbackFunction(char_id, this.response, category_name);
			return;
		}
	};
	
	xhttp.open("GET", webpage, true);
	
	xhttp.responseType = 'json'; 

	xhttp.send();

	return;
}

function updateInvCategoryHelper(char_id, response, category_name){
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
					<div class="inv_item_text">\
						<h2 style="color: ' + item.Rarities_Color + '">' + item.Item_Name + '</h2>';
	
		if(item.Amount > 1){
			itemString += '<h3>x' + item.Amount + '</h3>';
		}

		itemString += '</div>';

		if(item.Is_Equiped){
			itemString += '<div class="inv_unequip_item_button clickable" onclick="unequipItem(' + char_id + ', ' + item.Item_ID + ',' + category_name + ');"></div >';
		}else{
			itemString += '<div class="inv_equip_item_button clickable" onclick="equipItem(' + char_id + ', ' + item.Item_ID + ',' + category_name +  ');"></div >';
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
			document.getElementById('character_weight').innerHTML = this.response;
			isRemoveItemOpen = false;
		}
	}
	http.send(params);
}

function unequipItem(char_id, item_id){
	// Send update to server
	submitUnequipChange('/character/test', '', '');
}

function equipItem(char_id, item_id, slot_name){
	slot_num = 0;
	if(is_multiple_slots){
		// Determine which slot to add the item to
	} else {
		equipItemChangeSubmit('/character/item/equip/', char_id, item_id);
	}
}

function multipleSlotsInsert(url_prefix, char_id, item_id, slot_num){

}

function equipItemChangeSubmit(url_prefix, char_id, item_id, slot_num=0){
	// Send update to server
	submitEquipChange(url_prefix + char_id + '/' + item_id + '/' + slot_num, char_id, item_id);
}

function submitEquipChange(url, char_id, item_id){
	var http = new XMLHttpRequest();
	http.onreadystatechange = function(){ 
		if(http.readyState == 4 && http.status == 200) {
			// Update item picture and name in equipment
			updateEquipedItemName(this.response);
			updateEquipedItemPicture(this.response);

			// Update stats
			updateCharacterStats(this.response);

			console.log(this.response.slot_name);

			// Change button to equip button
			updateInvCategory(updateInvCategoryHelper, char_id, this.response.slot_name, '/dataserver/getItemsInSlot/' + char_id + '/' +  this.response.slot_name);
			//invertEquipButton(char_id, item_id);
		}
	}

	http.open("GET", url, true);
	
	http.responseType = 'json'; 

	http.send();

	return;
}

function updateEquipedItemPicture(response, use_default_image = false){
	var img_element = document.getElementById('equipment_' + response.slot_name + '_image');

	var new_src = '/static/images/no_image.png';

	if(!use_default_image){
		new_src = '/dataserver/imageserver/item/' + response.item_data['picture'];
	}
	
	img_element.setAttribute('src', new_src);
}

function updateEquipedItemName(response, use_default_data=false){
	var name_element = document.getElementById('equipment_' + response.slot_name + '_text');

	var new_name = response.slot_name;
	var color = '#606060';

	if(!use_default_data){
		new_name = response.item_data['name'];
		color = response.item_data['color'];
	}
	
	name_element.innerHTML = new_name;
	name_element.setAttribute('style', 'color: ' + color + ';');
}

function updateCharacterStats(response){
	var prefix = 'character_';
	var ids = [
		'max_hp', 'ac', 'initiative', 'attack_bonus', 'max_weight',
		'str', 'dex', 'con', 'int', 'wis', 'cha'
	];
	
	var mod_ids = [
		'str_mod', 'dex_mod', 'con_mod', 'int_mod', 'wis_mod', 'cha_mod', 
	];

	ids.forEach(id => {
		var fullId = prefix + id;
		console.log(fullId + ', ' + response.character_data[id]);
		document.getElementById(fullId).innerHTML = response.character_data[id];
	});	
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

