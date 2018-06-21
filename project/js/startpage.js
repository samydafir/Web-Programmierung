
$(document).ready(function check_login() {
  var cookie = document.cookie;
  if (cookie.indexOf("session_id") != -1  && cookie.indexOf("username") != -1) {
    $("#login-button").text("Logout");
    $("#login-button").attr("onclick", "logout(event)");
  }
});

function show_dialog(event, dialog) {
  $("#" + dialog).show();
  $("main, nav, header").css("filter", "blur(11px)");
}

function hide_dialog(event, dialog) {
  event.preventDefault();
  $("#" + dialog).hide();
  $("main, nav, header").css("filter", "");
  $("#login-message, #reg-message").html("");
}

function login(event) {
  event.preventDefault();
  user = $("#login_user").val();
  pw = $("#login_pw").val();

  $.ajax({
    url: "login.cgi",
    type: "POST",
    data: {username: user, password: pw},
    success: function(response){
      if(response == "True\n") {
        $("#login-button").text("Logout");
        $("#login-button").attr("onclick", "logout(event)");
        hide_dialog(event, "login");

      } else {
        $("#login-message").html("Something went wrong. Please try again.");
      }
    },
    error: function(response){
      $("#reg-message").html("Something went wrong. Please try again.");
    }
  });
}

function register (event) {
  event.preventDefault();
  user = $("#reg_user").val();
  pw = $("#reg_pw").val();
  pw_rep = $("#reg_pw_rep").val();
  $.ajax({
    url: "register.cgi",
    type: "POST",
    data: {username: user, password: pw, password_repeat: pw_rep},
    success: function(response){
      if(response == "True\n") {
        hide_dialog(event, "register");
      } else {
        $("#reg-message").html("Something went wrong. Please try again.");
      }
    },
    error: function(response){
      $("#reg-message").html("Something went wrong. Please try again.");
    }
  });
}

function logout(event) {
  $.ajax({
    url: "logout.cgi",
    type: "POST",
    success: function(response){
      $("#login-button").text("Login");
      $("#login-button").attr("onclick", "show_dialog(event, 'login')");
    },
    error: function(response){

    }
  });
}
