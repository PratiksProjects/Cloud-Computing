$(document).ready(function () {
    $('#container').hide();
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
});

function makeChart() {
        statType = $("#statType").val();
        valueType = $("#dataType").val();
        $('#container').show();
        Highcharts.chart('container', {
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {
                    //making query

                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = makeRequest(statType.toLowerCase(), valueType.toLowerCase()).responseJSON.aggregations.the_avg.value;
                        series.addPoint([x, y], true, true);
                    },5000); //updates every 5 seconds
                }
            }
        },
        title: {
            text: 'Live ' + statType + ' ' + valueType + ' Data' 
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 160
        },
        yAxis: {
            title: {
                text: 'Value'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'Random data',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;
                /*data.push({
                    x:time,
                    y: makeRequest(statType.toLowerCase(), valueType.toLowerCase()).responseJSON.aggregations.the_avg.value
                })*/
                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.random()
                    });
                }
                return data;
            }())
        }]
    });
}

function makeRequest(statType, valueType)
{
    
    //query object construction
    var q = {};
    q = {};
    q.query = {};
    q.query.bool = {};
    q.query.bool.filter = {};
    q.query.bool.filter.range = {};
    q.query.bool.filter.range.timestampNum = {};
    q.query.bool.filter.range.timestampNum.gt = "now-5s"; //get previous 30 second data
    q.aggs = {};
    q.aggs.the_avg = {};
    
    //query based on inputs
    if(statType == 'average') {
        q.aggs.the_avg.avg = {};
        q.aggs.the_avg.avg.field = valueType;
    } else if(statType = 'maximum') {
        q.aggs.the_avg.max = {};
        q.aggs.the_avg.max.field = valueType;
    } else {
        q.aggs.the_avg.min = {};
        q.aggs.the_avg.min.field = valueType;
    }
    
    var str = JSON.stringify(q);
    
    //console.log(str);
    url = "https://search-esdomain-kpidoc4kzpilk24sijrxcmp5ge.us-east-1.es.amazonaws.com/sensordata/_search?pretty"; 
    
    var graphData;
    return $.ajax({
      cache: false,
      type: "POST",
      url: url,
      data: str,
      dataType: 'json',
      contentType: 'json',
      async: false
    });
}
