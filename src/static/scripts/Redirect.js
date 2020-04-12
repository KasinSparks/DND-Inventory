export class Redirect {
	static redirect(to_location){
		document.location = to_location;
	}

	static redirect_after_time(to_location, milliseconds){
		setTimeout(function(){
			redirect(to_location);
		}, milliseconds);
	}
}
