ids = ["answer1", "answer2", "answer3", "answer4"];

$("#answer1, #answer2, #answer3, #answer4").click(function( event ){
  var answer = $(this);
  answers.push(($(answer).text().trim()));

  /*enlarge selected answer*/
  $(answer).css("width", "98%");
  $(answer).css("height", "100px");
  $(answer).prop("disabled", true);

  /*hide other buttons*/
  $(ids).each(function(){
    if ($("#" + this).attr("id") !== $(answer).attr("id"))
      $("#" + this).hide();
  });

  questionNumber += 1;
  /* Load new question after time */
  setTimeout(function(){
    if(questionNumber < questions.length){
      nextQuestion(answer)
    } else {
      results();
    }
  }, 2000);
});

/**
 * Loads next question from the questions-array using the
 * incremented question-counter
 */
function nextQuestion(answer){
  /*Load new question*/
  var next = questions[questionNumber][1];

  $(".answer").each(function(){
      $(this).html(next.pop());
  });

  $(".question").html(questions[questionNumber][0]);

  formatNext(answer);
}

function formatNext(answer){

  progress();
  random_colors();

  /* reset css to default */
  $(answer).css("width", "");
  $(answer).css("height", "");
  $(answer).prop("disabled", "");

  $(ids).each(function(){
    if ($("#" + this).attr("id") !== $(answer).attr("id"))
      $("#" + this).show();
  });
}

function progress() {
  var progress = Math.floor(questionNumber / questions.length * 100);
  $(".progress-bar").first().prop("aria-valuenow", progress);
  $(".progress-bar").first().css("width", progress + "%");
}


function results(){
  var i;
  var points = 0;
  var cookie = document.cookie

  progress();

  if (cookie.indexOf("session_id") != -1  && cookie.indexOf("username") != -1) {
    $.ajax({
      url: "post_results.cgi",
      type: "POST",
      data: {answers: answers},
      success: function(response){
        console.log(response);
        var result = response.split(",");
        $("#score").html(result[1]);
        $("#max-points").html(result[0]);
      }
    });

  } else {
    for(i = 0; i < answers.length; i++) {
      if(answers[i] === correct[i])
        points += 1;
    }
    $("#score").html(points);
    $("#max-points").html(questions.length);
  }

  $("#result-overlay").show();
  $("main").css("filter", "blur(11px)");
}
