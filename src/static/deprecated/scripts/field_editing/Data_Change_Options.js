import { Data_Caller } from "../Data_Caller.js"
import { Data_Change_Type } from "./Data_Change_Type.js"

export class Data_Change_Options {
	static _check_for_field(field_id_name){
		return document.getElementById(field_id_name);
	}

	static _option(data, char_id, field_id_name, submit_route, type){
		var field = Data_Change_Options._check_for_field(field_id_name);
		if (field === null) {
			return false;
		}

		var html_string = '<div class="char_item_val_change_container">';

		html_string += data;
		
		if (type !== Data_Change_Type.Types.IMAGE) {
			html_string += '<button onclick="submitChanges(' + char_id + ',\'' +
				field_id_name + '\',' + '\'' + submit_route + '\',' + type +
				');">Y</button><button onclick="abortChanges(\'' + field_id_name +
				'\');">X</button></div>';
			field.parentElement.parentElement.innerHTML += html_string;
		} else {
			field.parentElement.innerHTML += html_string;
		}
		
		field.setAttribute('style', 'display: none;');

		return true;

	}

	static dropdown(char_id, dropdown_options, field_id_name, submit_route){
		var html_string = '<select id="new_value">';
		dropdown_options.opts.forEach(element => {
			html_string += '<option value="' + element.id + '">' + element.name + '</option>';
		});

		html_string += '</select><button onclick="submitChanges(' + char_id +
			',\'' + field_id_name + '\',' + '\'' + submit_route + '\',' + 0 +
			');">Y</button><button onclick="abortChanges(\'' + field_id_name +
			'\');">X</button></div>';

		return Data_Change_Options._option(html_string, char_id, field_id_name, submit_route,
			Data_Change_Type.Types.SELECT);
	}
	
	static number(char_id, current_number, field_id_name, submit_route){
		var html_string = '<input type="number" id="new_value" value="' +
			current_number.current_value + '">';
		console.log(current_number.current_value);
		
		return Data_Change_Options._option(html_string, char_id, field_id_name, submit_route,
			Data_Change_Type.Types.NUMBER);
	}

	static number_additional(char_id, current_number, field_id_name, submit_route){
		var html_string = '<div style="display: flex; width: 100%;">\
			<div class="stat_details"><h4>Base</h4><p>' + current_number.base +
			'</p></div><div class="stat_details"><h4>Additional</h4><p>' +
			current_number.additional + '</p></div></div>';
		
		html_string += '<input type="number" id="new_value" value="' +
			current_number.base + '">';

		return Data_Change_Options._option(html_string, char_id, field_id_name, submit_route,
			Data_Change_Type.Types.NUMBER);
	}

	static image(char_id, dummy_data, field_id_name, submit_route){
		var html_string = '<form method="post" enctype="multipart/form-data" action="' +
			submit_route + '"><input name="image" type="file"\
			id="new_value" accept="image/gif, image/jpeg, image/png, image/jpg">\
			<input type="submit", value="Y"/><button onclick="abortChanges(\'' +
			field_id_name + '\');">X</button></form></div>';

		return Data_Change_Options._option(html_string, char_id, field_id_name, submit_route,
			Data_Change_Type.Types.IMAGE);
	}
	
	static string_value(char_id, current_string, field_id_name, submit_route){
		var html_string = '<input type="text" id="new_value" value="' +
			current_string.current_value + '">';

		return Data_Change_Options._option(html_string, char_id, field_id_name, submit_route,
			Data_Change_Type.Types.STRING);
	}	
}
