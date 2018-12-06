
// global variable
var img = undefined

function callWebService() 
{
    if (img !== undefined){
      // Sending and receiving data in JSON format using POST mothod
      document.getElementById("result").innerHTML = "In treatment!"
      var xhr = new XMLHttpRequest();
      var url = "http://132.203.114.102:8080/detectArucoMarker";
      xhr.open("POST", url, true);
      xhr.setRequestHeader("Content-type", "application/json");
      xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
              var json = JSON.parse(xhr.responseText);
              var result = json.result
              document.getElementById("result").innerHTML = result;
          }
      };
      var data = JSON.stringify({"data":img});
      xhr.send(data);
    }
    else
    {
      document.getElementById("result").innerHTML = "No image loaded!"
    }
}

function getSingleFile(path) 
{
  if (!path.target.files[0])
  {
    document.getElementById("result").innerHTML = "Not a file!"
    img = undefined
  }
  else
  {
    var file = path.target.files[0];
    var reader = new FileReader();
    reader.onload = function(e) { 
      img = e.target.result;
      document.getElementById('uplImg').src = img;
    };
    reader.readAsDataURL(file);
    document.getElementById("result").innerHTML = "Ready to send!"
  }
}

document.getElementById('file-input').addEventListener('change', getSingleFile, false);
/*
function loadDefault()
{
  document.getElementById('uplImg').src = img;
}

window.onload = loadDefault
*/

var myString = "something format_abc";
var myRegexp = /(?:^|\s)format_(.*?)(?:\s|$)/g;
var match = myRegexp.exec(myString);