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

class ChangeCharacterData{
	constructor(char_id, webpage, responseType, field_id_name, submit_route){
		this.char_id = char_id;
		this.webpage = webpage;
		this.responseType = responseType;
		this.field_id_name = field_id_name;
		this.submit_route = submit_route;
	}

	dataCall(callbackFunction, submit_route=this.submit_route, char_id=this.char_id, field_id_name=this.field_id_name){
		console.log(submit_route);
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function(){
			if(this.readyState == 4 && this.status == 200){
				if(this.response == null){
					console.error('Response from ' + webpage + ' was null.');
					return;
				}
				callbackFunction(char_id, this.response, field_id_name, submit_route);
				return
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
				field_id_name);
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

function submitData(url, params, field_id_name){
	var http = new XMLHttpRequest();
	http.open('POST', url, true);

	//Send the proper header information along with the request
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			// do something here
			document.getElementById(field_id_name).innerHTML = http.responseText;
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
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getClassOptions',
			'json', 'character_class', '/character/edit/class/');
		ccd.dataCall(ccd.dropdown);
	}
}

function changeLevel(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getLevel/' + char_id, 'json',
			'character_level', '/character/edit/level/');
		ccd.dataCall(ccd.number);
	}
}

function changeImage(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/dummyCall', 'json',
			'character_image', '/character/edit/image/');
		ccd.dataCall(ccd.image);
	}
}

function changeHealth(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getHealth/' + char_id, 'json',
			'character_hp', '/character/edit/health/')
		ccd.dataCall(ccd.number);
	}
}

function changeMaxHealth(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getMaxHealth/' + char_id, 'json',
			'character_max_hp', '/character/edit/maxhealth/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeAC(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getAC/' + char_id, 'json',
			'character_ac', '/character/edit/ac/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeInitiative(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getInitiative/' + char_id, 'json',
			'character_initiative', '/character/edit/initiative/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeAttackBonus(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getAttackBonus/' + char_id, 'json',
			'character_attack_bonus', '/character/edit/attackBonus/')
		ccd.dataCall(ccd.number_additional);
	}
}

function changeAlignment(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getAlignmentOptions',
			'json', 'character_alignment', '/character/edit/alignment/');
		ccd.dataCall(ccd.dropdown);
	}
}

function changeCurrency(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getCurrency/' + char_id, 'json',
			'character_currency', '/character/edit/currency/')
		ccd.dataCall(ccd.number);
	}
}

function changeStrBonus(char_id){
	if(!isChangeCharDataOpen){
		var ccd = new ChangeCharacterData(char_id, '/dataserver/getStr/' + char_id, 'json',
			'character_str_bonus', '/character/edit/str/')
		ccd.dataCall(ccd.number_additional);
	}
}