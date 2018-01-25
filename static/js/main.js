//function that continuosuly checks for download cookie
var checkDownloadCookie = function() {
	//check if cookie delivered from views has been set true
	if (Cookies.get("downloadFinished") == "true") {
		//if yes, hide the gif
		$('#loading').css('display', 'none');
	} else {
		//if not,re-run this function in 1 second.
		setTimeout(checkDownloadCookie, 1000);
	};
};

//loading spinner
$(document).ready(function(){
	//check whether link to download was clicked
	$(".downloadLink").click(function(){
		Cookies.set("downloadFinished","false");
		//switch the loader image from hidden to shown
		$("#loading").css("display","inline");
		//check every second whether cookie download works
		setTimeout(checkDownloadCookie, 1000);
	});
});
