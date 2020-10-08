document.getElementById('newmessage').addEventListener("submit", function(e) {
  var content = document.getElementById("sendbox").value;
  if(content == "") {
    console.log("비어있다능");
    e.preventDefault();
  }
})
