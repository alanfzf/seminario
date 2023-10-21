function deleteSomething(url_target, csrf, callback_error, callback_done){
  $.ajax({
    headers: {'X-CSRFToken': csrf},
    url: url_target,
    type: 'DELETE',
    dataType: 'json',
    processData: false,
    contentType: false,
  })
    .done(function(data){
      callback_done(data);
    })
    .fail(function(xhr, err_status, error){
      const {status, responseJSON} = xhr
      let {errors} = responseJSON || {}

      if (!errors){
        errval = (status === 403 ? `No tienes permiso de realizar esto` 
          : `${err_status}, ${error}`)
        errors = `${status}: ${errval}`
      }
      callback_error(errors);
    })
    .always(function(_data){})
}

function getSomething(url_target, csrf, callback_error, callback_done){
  $.ajax({
    headers: {'X-CSRFToken': csrf},
    url: url_target,
    type: 'GET',
    dataType: 'json',
    processData: false,
    contentType: false,
  })
  .done(function(data){
      callback_done(data)
    })
  .fail(function(_xhr, _status, _error){
      callback_error(_error)
    })
  .always(function(_data){})
}
