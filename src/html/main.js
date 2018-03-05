var API_ENDPOINT = "http://localhost:8080"

// From https://code-maven.com/ajax-request-for-json-data

function ajax_get(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            console.log('responseText:' + xmlhttp.responseText);
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch(err) {
                console.log(err.message + " in " + xmlhttp.responseText);
                return;
            }
            callback(data);
        }

    };

    xmlhttp.open("GET", url, true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send();

}

ajax_get(API_ENDPOINT + '/diary', function(data) {
	if (data.status) {
		var members = data.result;	
        var output = "<table>";
        for (var i = 0; i < members.length; i++) {
		output += "<form>";
		output += "<tr><td><b>ID</b></td><td>"+members[i]['id']+"</td></tr>";
            	output += "<tr><td><b>Title</b></td><td>"+members[i]['title']+"</td></tr>";
		output += "<tr><td><b>Author</b></td><td>"+members[i]['author']+"</td></tr>";
		output += "<tr><td><b>Date</b></td><td>"+members[i]['publish_date']+"</td></tr>";
		output += "<tr><td><b>Text</b></td><td>"+members[i]['text']+"</td></tr>";
		output += "<tr><td><b>Privacy </b></td><td>Public</td></tr>"; // Must be public entry
		output += "<tr><td><br></td><td><br></td></tr>"; // empty row to separate entries 
		output += "</form>";
        }
        output += "</table>";
		document.getElementById("listpublicentries").innerHTML = output;
	}
	else {
		document.getElementById("listpublicentries").innerHTML = "Failed to obtained public entry";
	}

});

$('#registerform').on('submit', function(event){

   var obj = $('#registerform').serializeJSON();

   $.ajax({
      url: "http://localhost:8080/users/register",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
	   document.getElementById("register_results").innerHTML = "Registration successful, please login!";
           document.getElementById("registerform").reset();
         }
         else {
           var output = data.error;
	   document.getElementById("register_results").innerHTML = "<font color='red'>Error: " + output + "</font>";
         }
      }
   });

   return false;

});

$('#loginform').on('submit', function(event){

   var obj = $('#loginform').serializeJSON();

   $.ajax({
      url: "http://localhost:8080/users/authenticate",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
	   document.getElementById("login_results").innerHTML = "Login successful! Redirecting...";
           document.cookie = "token=" + data.result['token'];
           setTimeout("window.location = 'users/'", 2000);
         }
         else {
	   document.getElementById("login_results").innerHTML = "<font color='red'>Login failed!</font>";
         }
      }
   });

   return false;

});
