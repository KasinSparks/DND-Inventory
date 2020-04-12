import { Data_Caller } from "./Data_Caller.js"
import { Logger } from "./Logger.js"
import { Data_Change_Type } from "./Data_Change_Type.js"

export class Data_Change_Submit{
	static submit(char_id, field_id_name, submit_route, call_type=0){
		var logger = new Logger(true);
		var element = document.getElementById('new_value');
		switch(call_type){
			case Data_Change_Type.Types.SELECT:
				var d = new Data_Caller("POST", submit_route, false, "value=" +
					element.options[element.selectedIndex].value, logger);
				d.call(Data_Change_Submit._submit_result_handler,
					[false, call_type, field_id_name, '?']);
				break;
			case Data_Change_Type.Types.NUMBER:
				// allow falldown for number to string because handling of number and
				// string is the same
			case Data_Change_Type.Types.STRING:
				var d = new Data_Caller("POST", submit_route, true, "value=" +
					element.value, logger);
				d.call(Data_Change_Submit._submit_result_handler,
					[true, call_type, field_id_name, '?']);
				break;
			case Data_Change_Type.Types.IMAGE:
				var d = new Data_Caller("POST", submit_route, false, "image=" +
					element.value, logger, true);
				d.call(Data_Change_Submit._submit_result_handler,
					[false, call_type, field_id_name, '?']);
				break;
			default:
				// TODO: better error handling
				logger.error("Unknown type of data: " + element.value);
		}
		Data_Change_Submit._abortChanges(field_id_name);
		return
	}

	static _submit_result_handler(is_json, call_type, field_id_name, response){
		if (call_type === Data_Change_Type.Types.IMAGE) {
			// do nothing
		} else if(!is_json && field_id_name != ''){
			document.getElementById(field_id_name).innerHTML = response;
		} else {
			var data = response;
			for(var k in data){
				document.getElementById(k).innerHTML = data[k];
			}
		}
		return;
	}

	static _abortChanges(field_id_name, isChangeCharDataOpen=true){
		if(isChangeCharDataOpen){
			document.getElementById(field_id_name).setAttribute('style', '');
			document.getElementsByClassName('char_item_val_change_container')[0].remove();
		}
		//isChangeCharDataOpen = false;
		return;
	}
}
