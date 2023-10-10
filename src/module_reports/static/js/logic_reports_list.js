$(function(){
  $('#tabla').DataTable({})
  $('.delete-report').click(function(){
    const onDone = (_data) => { 
      window.location.reload() 
    }
    const onError = (errors) => {
      $('#alert-area').removeClass('d-none')
      $('#alert-content').html(errors)
    }

    const borrar = confirm('¿De verdad deseas eliminar este item?')
    if(!borrar){ return }

    const url = $(this).data('url')
    const csrf = window.CSRF_TOKEN
    deleteSomething(url, csrf, onError, onDone)
  })
})
