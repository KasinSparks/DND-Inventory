export class Logger {
	constructor(enabled=true){
		this.enabled = enabled;
	}

	log(message){
		console.log(message);
	}

	error(message){
		console.error(message);
	}
}
