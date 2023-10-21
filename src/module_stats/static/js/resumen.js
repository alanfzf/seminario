$(function(){

 $('#btn-print').click(function(event) {
    event.preventDefault();
    const report_ids = $('#tabla tbody tr').map(function() { return $(this).find('th').text(); }).get();
    const append_url = `report_ids=${report_ids.join(",")}`
    const url = $(this).attr('href')
    window.location.href = `${url}?${append_url}`;
  });


})
