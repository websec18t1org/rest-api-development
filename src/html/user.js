
function delete_diary(id)
{
	var cook = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
	var cookietext = '{ "token" : "' + cook + '", "id" : "'+ id+'"}';
	var obj = JSON.parse(cookietext);

   $.ajax({
      url: "http://localhost:8080/diary/delete",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
           alert('Success!');
	   getowndiaryfunction(); // refresh 
         }
         else {
           alert('Error! Status = ' + xhr.status + ' Message = ' + data + send);
         }
      }
   });

   return false;

}

function update_diary(id, publicvalue)
{
	var cook = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        if (publicvalue) {
	   var cookietext = '{ "token" : "' + cook + '", "id" : "' + id + '", "public" : true }';
        }
        else {
	   var cookietext = '{ "token" : "' + cook + '", "id" : "' + id + '", "public" : false }';
        }
	var obj = JSON.parse(cookietext);

   $.ajax({
      url: "http://localhost:8080/diary/permission",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
          alert('Success!');
	  getowndiaryfunction(); // refresh 
         }
         else {
           alert('Error! Status = ' + xhr.status + ' Message = ' + data + send);
         }
      }
   });

   return false;

}

$(document).ready(function() {

   var cook = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
   var cookietext = '{ "token" : "' + cook + '" }';
   var obj = JSON.parse(cookietext);

   $.ajax({
      url: "http://localhost:8080/users",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
	   document.getElementById("authenticate_results").innerHTML = "Status: Authentication successful<br> You are logged in as <b>" + data.result['username'] + "</b> (" + data.result['fullname'] + ", " + data.result['age'] + " years old)<br>";
         }
         else {
           var output = data.error;
	   document.getElementById("authenticate_results").innerHTML = "<font color='red'>Status: Error<br>" + output + "</font>";
         }
      }
   });

   return false;

});

$('#logoutform').on('submit', function(event){

   var cook = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
   var cookietext = '{ "token" : "' + cook + '" }';
   var obj = JSON.parse(cookietext);

   $.ajax({
      url: "http://localhost:8080/users/expire",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
	   document.getElementById("logout_results").innerHTML = "Logout successful! Redirecting...";
           setTimeout("window.location = 'http://localhost/'", 2000);
         }
         else {
	   document.getElementById("logout_results").innerHTML = "<font color='red'>Error</font>";
         }
      }
   });

   return false;

});

function getowndiaryfunction()
{

   var cook = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
   var cookietext = '{ "token" : "' + cook + '" }';
   var obj = JSON.parse(cookietext);

   $.ajax({
      url: "http://localhost:8080/diary",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(obj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
           var members = data.result;
           
		   if(members.length == 0)
		   {
			  document.getElementById("viewdiary_results").innerHTML = 'You have not created any diary entry.' ;
		   }
		   else
		   {
			   var output = "<table>";
			   for (var i = 0; i < members.length; i++) {
						output += '<tr><td><div id="entry_'+members[i]['id']+'"><table>'

						output += "<form>"
						output += "<tr><td><b>ID</b></td><td>"+members[i]['id']+"</td></tr>"
						output += "<tr><td><b>Title</b></td><td>"+members[i]['title']+"</td></tr>"
						output += "<tr><td><b>Author</b></td><td>"+members[i]['author']+"</td></tr>"
						output += "<tr><td><b>Date</b></td><td>"+members[i]['publish_date']+"</td></tr>"
						output += "<tr><td><b>Text</b></td><td>"+members[i]['text']+"</td></tr>"
						output += "<tr>"
						if (members[i]['public'])
						{	output += "<td><b>Privacy</b></td><td>Public <button style='width: 50%' id='2' onclick=update_diary("+members[i]['id']+",0)>Set Private</button></td>";}
						else
						{	output += "<td><b>Privacy</b></td><td>Private <button style='width: 50%' id='2' onclick=update_diary("+members[i]['id']+",1)>Set Public</button></td>";}
	
							output += "</tr></form><form><tr>";
							output += "<td colspan='2'><button id='1' onclick=delete_diary("+members[i]['id']+")>Delete Post</button></td>";
							output += "</tr></form>";

							output += "</table></div></td></tr>"
          }
          output += "</table>";
                  document.getElementById("viewdiary_results").innerHTML = output;
		   }
           
         }
         else {
	   var output = data.error;
	   document.getElementById("viewdiary_results").innerHTML = "<font color='red'>Status: Error<br>" + output + "</font>";
         }
      }
   });

   return false;

}

$('#viewdiaryform').on('submit', getowndiaryfunction());

$('#creatediaryform').on('submit', function(event){

   var cook = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
   var cookietext = '{ "token" : "' + cook + '" }';
   var obj = JSON.parse(cookietext);

   var obj2 = $('#creatediaryform').serializeJSON();

   var finalobj = {};

   finalobj['token'] = obj['token'];
   finalobj['title'] = obj2['title'];
   if (obj2['public'] == "on")
      finalobj['public'] = true;
   else
      finalobj['public'] = false;
   finalobj['text'] = obj2['text'];

   $.ajax({
      url: "http://localhost:8080/diary/create",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(finalobj),
      contentType: 'application/json',
      error: function(xhr, error) {
            alert('Error! Status = ' + xhr.status + ' Message = ' + error + send);
      },
      success: function(data) {
         if (data.status) {
	   document.getElementById("creatediary_results").innerHTML = "Create post with ID " + data.result['id'] + " successful!<br>Refreshing diary...";
	   setTimeout("getowndiaryfunction();document.getElementById('creatediary_results').innerHTML=''", 5000);
           document.getElementById("creatediaryform").reset();
         }
         else {
	   var output = data.error;
	   document.getElementById("creatediary_results").innerHTML = "<font color='red'>Status: Error<br>" + output + "</font>";
         }
      }
   });

   return false;

});
