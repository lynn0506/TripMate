function doOpenCheck(gender){
  var option = document.getElementsByName("gender");
  console.log("check gender")
  for(var i=0; i<option.length; i++){
      if(option[i] != gender){
          option[i].checked = false;
          option[i].required = false;
      } else {
          option[i].required = true;
      }
  }
}
