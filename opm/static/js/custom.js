function reveal_password(chkbx){
  var password_field = document.getElementById("password_field");
  var show_password = document.getElementById("show_password");
  if(true){
    password_field.innerHTML = "{{ profile.password }}"
  } else {
    password_field.data = "****"
  }
}
