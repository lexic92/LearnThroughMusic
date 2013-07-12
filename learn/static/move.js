function move2(userID) {
	$("#Lists").html(userID + "");
}

function deletesong(userId, songId) {
	var string1 = '/learn/delete/' + userId + '/' + songId;
	$.ajax({
		url: string1,
		success: function(data){
			$("#Lists").html(data);
		}
	});
}

function movesong(userID, songID, fromList, toList) {
	if(toList == "")
	{
		//Do nothing
		return;
	}
	else if(fromList == toList)
	{
		//Do nothing to make it save time and not reload
		return;
	}
	else
	{
		var string1 = '/learn/move/' + userID + '/' + songID + '/' + fromList + '/' + toList;
		$.ajax({
		    url: string1,
		    success: function(data){
			$("#Lists").html(data);
		    }
		   
		});
	}
}


function getMoveDropDownListValue(listID){
    var selectBoxID = 'moveDropDownList' + listID;
    return document.getElementById(selectBoxID).value;
}  


function deletesong(userId, songId) {
	var string1 = '/learn/delete/' + userId + '/' + songId;
	$.ajax({
		url: "http://www.something.com",
		success: function(data){
			$("#list").html(data);
		}
	});
}






