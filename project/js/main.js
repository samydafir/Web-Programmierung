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


function nextQuestion(answer){
  /*Load new question*/
  var next = questions[questionNumber]["incorrect_answers"];
  next.push(questions[questionNumber]["correct_answer"])
  next.sort(function() {
      return 0.5 - Math.random();
  });

  $(".answer").each(function(){
      $(this).html(next.pop());
  });

  $(".question").html(questions[questionNumber]["question"]);

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

  progress();
  for(i = 0; i < answers.length; i++) {
    if(answers[i] === questions[i]["correct_answer"])
      points += 1;
  }
  $("#score").html(points);
  $("#max-points").html(questions.length);
  $("#result-overlay").show();
  $("main").css("filter", "blur(11px)");
}
