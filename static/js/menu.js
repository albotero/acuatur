$('nav').hover(function(){
  $('.menu').toggleClass('change');
});

$('li').click(function(){
  $('li').removeClass('selected');
  $(this).addClass('selected');
});

function open_schedule(id) {

}

function duplicate_schedule(id) {

}

function delete_schedule(id) {

}

function new_schedule() {
  location.replace('/schedule');
}
