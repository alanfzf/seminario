$(function(){
  $('#tabla').DataTable({})
  $('.delete-user').click(function(){
    const answer = confirm("¿De verdad deseas eliminar a este usuario?")
    if(!answer){return}

    const url = $(this).data('url')
    const csrf = window.CSRF_TOKEN

    const onDone = (_data) => { 
      window.location.reload() 
    }
    const onError = (errors) => {
      $('#alert-area').removeClass('d-none')
      $('#alert-content').html(errors)
    }
    deleteSomething(url, csrf, onError, onDone)
  })
})
