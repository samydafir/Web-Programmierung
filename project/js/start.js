/*---- Variables ----*/
var questionNumber = 0;
var answers = [];

function random_colors(){
  var colors = ['danger', 'success', 'dark', 'warning'];
  $('.answer').each(function(){
    $(this).addClass("btn-" + colors[Math.floor(Math.random() * colors.length)]);
  });
}

$(document).ready(random_colors);
