import { Data_Caller } from "../Data_Caller.js"
import { Logger } from "../Logger.js"

export class Item_Overlay {
	// must supply either equipmentItemStr or itemID
	constructor(element_name, url){
		this.el_name = element_name;
		this.url = url;
		// TODO : move logger out
		this.logger = new Logger(true);
	}

	create(){
		var html_inner = document.getElementsByClassName(this.el_name)[0];
		
		var dc = new Data_Caller("GET", url, true);
		dc.call_async(
	}

	itemInfo(element, jsonData){
		// Quick verify data sent back
		if(jsonData != null && (jsonData.name != '' && jsonData.name != 'null')){
			element.innerHTML += get_item_details_html(jsonData);
		} else {
			this.logger.error("JSON data was null");
		}
	}
}
