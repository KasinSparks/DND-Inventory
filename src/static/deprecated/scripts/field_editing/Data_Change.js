import { Data_Change_Options } from "./Data_Change_Options.js"
import { Data_Change_Type } from "./Data_Change_Type.js"
import { Data_Caller } from "../Data_Caller.js"
import { Logger } from "../Logger.js"

export class Data_Change {
	constructor(char_id, data_change_type, data_url, field_id_name, submit_url){
		this.char_id = char_id;
		this.data_change_type = data_change_type;
		this.data_url = data_url;
		this.field_id_name = field_id_name;
		this.submit_url = submit_url;
		this.logger = new Logger(true);	//TODO: move logger out of class
	}

	change_data(){
		var is_res_json = true;	// is response json
		var callback_function = null;
		switch(this.data_change_type){
			case Data_Change_Type.Types.IMAGE:
				callback_function = Data_Change_Options.image;
				break;
			case Data_Change_Type.Types.NUMBER:
				callback_function = Data_Change_Options.number;
				break;
			case Data_Change_Type.Types.NUM_ADDITIONAL:
				callback_function = Data_Change_Options.number_additional;
				break;
			case Data_Change_Type.Types.STRING:
				callback_function = Data_Change_Options.string_value;
				break;
			case Data_Change_Type.Types.SELECT:
				callback_function = Data_Change_Options.dropdown;
				break;
			default:
				// TODO: better error handling
				var err_msg = "Unknown type to change in Data_Change::change_data";
				this.logger.error(err_msg);
				//throw "Unknown type to change in Data_Change::change_data";
				return false;
		}
		var data_caller = new Data_Caller("GET", this.data_url, is_res_json, null, this.logger);
		data_caller.call_async(callback_function, 
			[this.char_id, '?', this.field_id_name, this.submit_url]); 

		return true;
	}
}
