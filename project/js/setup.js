$(document).ready(function(){
  var colors = ['danger', 'success', 'dark', 'warning'];
  $('.answer').each(function(){
    console.log(Math.floor(Math.random() * colors.length));
    $(this).addClass("btn-" + colors[Math.floor(Math.random() * colors.length)]);
  });
  });
