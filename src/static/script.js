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
	if(jsonData != null){
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