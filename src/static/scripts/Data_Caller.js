export class Data_Caller {
	constructor(method_type, url, response_json=true, params=null, logger=null, ignore_response=false){
		this.method_type = method_type;
		this.url = url;
		this.is_json = response_json;
		if (String(method_type).toUpperCase() === "POST" && params === null) {
			// TODO: better error handling	
			logger.error("Tried to do a post request with no data.");
			throw "Tried to do a post request with no data.";
		}
		this.params = params;
		this.logger = logger;
		this.ignore_res = ignore_response;
	}
	
	// use ? for location you want response arg to go
	call(callback, callback_args){
		var xhttp = new XMLHttpRequest();

		xhttp.open(this.method_type, this.url, true);
		//Send the proper header information along with the request
		xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		if (this.is_json) {
			xhttp.responseType = 'json';
		}

		xhttp.onreadystatechange = function(logger=this.logger, ignore_res=this.ignore_res){
			if(this.readyState == 4 && this.status == 200){
				if (ignore_res){
					return;
				}

				if (this.response == null) {
					if (logger !== null){
						logger.error("Response from " + url + " was null.");
					}
					return;
				}
				
				if(!callback_args.includes('?')){
					throw "args list does not have required ? arg";
				}

				var respone_index = callback_args.indexOf('?');
				callback_args[respone_index] = this.response;
				callback.apply(this, callback_args);
				return;
			}
		};
		
		if (this.params !== null){
			xhttp.send(this.params);
		} else {
			xhttp.send();
		}
	}
}
