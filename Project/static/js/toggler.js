$(document).ready(function(){
 $('.toggle').click(function(){
  $(this).children('.toggle__arrow-down').toggle();
  $(this).children('.toggle__arrow-up').toggle();
  $(this).parent().children('div.spoiler_body').toggle('normal');
  return false;
 });
});