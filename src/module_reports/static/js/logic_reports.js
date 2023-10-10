$(function(){
  $('.select2').select2({
    theme: 'bootstrap-5'
  })


  $("#report_submit").click(function(){
    $(".accordion-collapse").collapse("show");
  })



  $("#report_submit").submit(function(e) {
    // Prevent the form from submitting
    e.preventDefault();

    // Expand all accordions
    // $(".accordion-collapse").collapse("show");

    // Submit the form
    // $(this).submit();
  });


})
