$(function(){
  $('.select2').select2({
    theme: 'bootstrap-5',
    width: '100%'
  })

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation');
  function scrollToInvalid(form) {
    const invalidInputs = Array.from(form.querySelectorAll(':invalid'));    // set up so you can use any custom invalid classes you're adding to your elements, as well
    invalidInputs.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);                      // sort inputs by offset from top of viewport (handles issues with multi-column layouts, where the first element in the markup isn't necessarily the highest on the page)
    invalidInputs[0].scrollIntoView({ block: 'center', behavior: 'smooth' });                                         // scroll first (top) input into center of view, using smooth animation
  }

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();

        scrollToInvalid(form)
      }

      form.classList.add('was-validated');
    }, false);
  });

})
