function drawGraph(data, chart_id, typeName) {
    bisectDate = d3.bisector(function(d) {
        return d.timestamp;
    }).left,
    formatValue = d3.format(",.2f"),
    formatUnit = function(d) {
        return formatValue(d) + "pF";
    };

    var len = data.length;
    console.log(data)
    graph = new SimpleGraph(chart_id,
        data,
        {
            "xmax": data[len-1][0], "xmin": data[0][0],
            "ymax": data[len-1][1], "ymin": data[0][1],
            "title": typeName + " measurements",
            "xlabel": "Time",
            "ylabel": "Value"
        }
    );

    graph2 = new SimpleGraph(chart_id +"-overview",
        data,
        {
            "xmax": data[len-1][0], "xmin": data[0][0],
            "ymax": data[len-1][1], "ymin": data[0][1],
            "title": typeName + " measurements",
            "xlabel": "Time",
            "ylabel": "Value"
        }
    );
}

function loadGraph(type, typeName, id) {
    var url = '/rest/gateways/{{ gateway_id }}/sensors/' + id + '/measurements.json?type=' + type + '&start=2015-01-01&end=2020-01-01';
    var chart_id = 'measurement_chart-' + type + '-' + id;

    var margin = {
        top: 20,
        right: 50,
        bottom: 30,
        left: 50
    };
    var width = 960 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S").parse;

    d3.json(url, function(error, incoming_data) {
        if(error){
            throw error;
        }

        var data = incoming_data.measurements;

        data.forEach(function(d) {
            d.timestamp = parseDate(d[0]);
            d.value = +d[1];
        });

        data.sort(function(a, b) {
            return a.timestamp - b.timestamp;
        });

        drawGraph(data, chart_id, typeName);
    });
}

$(document).ready(function(){
    $(".nav-pills a").click(function(){
        $(this).tab('show');
    });

    $('.nav-pills a').on('shown.bs.tab', function(event){
        var pillName = $(event.target).text(); // Sensor x
        var id = pillName.slice(-1); // x
    });

    $('.graphDataTabs a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        console.log(e.target.dataset.measurementType); // newly activated tab
        loadGraph(e.target.dataset.measurementType, e.target.dataset.measurementTypeName, e.target.dataset.sensor);
    })
});