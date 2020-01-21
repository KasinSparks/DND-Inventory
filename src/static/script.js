var saveForLater = new Map([["", ""]]);

function test(str){
	var hmtlInner = document.getElementsByClassName('equipment')[0];
	console.debug('here');
	saveForLater[0] = [str, hmtlInner.innerHTML];
	console.debug(saveForLater);
	hmtlInner.innerHTML = '<p>test</p><div style="width: 30%; min-width: 290px; max-width: 302px; height: 100%; background-color: #FFFFFF;" onclick="test2();"><div style="width: 100%; height: 100%;">test asdfsaa</div></div>';
	return;
}


function test3(str){
	var hmtlInner = document.getElementsByClassName('equipment_tab')[0];
	console.debug('here');
	saveForLater[0] = [str, hmtlInner.innerHTML];
	console.debug(saveForLater);
	hmtlInner.innerHTML = hmtlInner.innerHTML.concat('\
	\n<div style="width: 100%; height: 100%; background-color: rgba(0,0,0,0.7);position: relative; top:-100%; left: 0px; z-index: 1;">\
		<div style="display: flex; padding: 20px; width: 80%; margin: 0 auto;">\
			<img style="border: dotted white 2px; margin: auto; width: 64px; height: 64px;" src="../static/Item_img_shoulders.png" alt="Shoulder Item"/>\
			<h1 style="color: white; padding: 0px; margin: auto;">Shoulders<\h1>\
		</div>\
		<div style="overflow-y: scroll; max-height: 70%;">\
			<table style="margin: 0 auto; width: 70%;">\
				<tr>\
					<td><h2>STR:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>DEX:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>CON:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>INT:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>WIS:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>CHA:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>STR:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>DEX:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>CON:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>INT:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>WIS:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>CHA:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>STR:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>DEX:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>CON:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>INT:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>WIS:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>CHA:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>STR:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>DEX:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>CON:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>INT:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
				<tr>\
					<td><h2>WIS:</h2></td>\
					<td><h2>+0</h2></td>\
					<td><h2>CHA:</h2></td>\
					<td><h2>+0</h2></td>\
				</tr>\
			</table>\
		</div>\
		<div onclick="test2();" style="bottom: 0px; position: relative; width: 10%; margin: 4% auto; border: solid white 2px;">\
			<h1 style="color: crimson; text-align: center; padding: 0px; margin: 0px;">X</h1>\
		</div>\
	</div>\
	')
	return;
}

function test2(){
	console.debug("test2()");
	console.debug(saveForLater[0][1]);
	document.getElementsByClassName('equipment_tab')[0].innerHTML = saveForLater[0][1];
	return;
}