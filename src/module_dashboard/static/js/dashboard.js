$(function(){

  const mesActual = new Date().toLocaleString('es-ES', { month: 'long' });
  const {url_servicios_mes, url_tipos_servicios} = window.URLS
  const onError = () => {}

  getSomething(url_servicios_mes, window.CSRF_TOKEN, onError, function(data){

    let serviciosCant = Object.entries(data).map(([clave, valor]) => [parseInt(clave), valor]);
    
    console.log(serviciosCant)


    Highcharts.chart('container-tiempo', {
      title: {
        text: `Servicios atendidos (${mesActual.toUpperCase()})`,
        align: 'left'
      },
      credits: { enabled: false },
      yAxis: {
        title: {
          text: 'Cantidad de servicios'
        },
        allowDecimals: false
      },
      xAxis: {
        tickInterval: 1
      },
      legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
      },
      plotOptions: {
        series: {
          label: { connectorAllowed: false },
        }
      },
      series: [{
        name: 'Servicios atendidos',
        showInLegend: false,
        data: serviciosCant, 
      }],
      responsive: {
        rules: [{
          condition: { maxWidth: 500 },
          chartOptions: {
            legend: {
              layout: 'horizontal',
              align: 'center',
              verticalAlign: 'bottom'
            }
          }
        }]
      }
    });
  })


  getSomething(url_tipos_servicios, window.CSRF_TOKEN, onError, function(data){
    let servicios_tipos = Object.entries(data)
    .map(([name, y]) => ({ name, y }));

    Highcharts.chart('container-servicios', {
      chart: {
        plotShadow: true,
        type: 'pie'
      },
      title: {
        text: `Tipos de servicios atendidos (${mesActual.toUpperCase()})`,
        align: 'left'
      },
      credits: {
        enabled: false
      },
      tooltip: {
        pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
      },
      accessibility: {
        point: {
          valueSuffix: '%'
        }
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: true,
            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
          }
        }
      },
      series: [{
        name: 'Servicios',
        colorByPoint: true,
        data: servicios_tipos 
      }]
    });
  })
})
