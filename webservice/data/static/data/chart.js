

/*s = new Object();

var values = new Array();
for(var i = 0; i<1000; i+=2){
    obj = new Object();
    obj.x = i;
    obj.y = 10;
    values.push(obj);
}

s.values= values;
s.key = "Overview";
s.color = "#2ca02c";

data2 = new Array();
data2.push(s);

s = new Object();

var values = new Array();
for(var i = 0; i<500; i++){
    obj = new Object();
    obj.x = i;
    obj.y = (i*i) - 100*i;
    values.push(obj);
}

for(var i = 500; i<1000; i++){
    obj = new Object();
    obj.x = i;
    obj.y = 0;
    values.push(obj);
}

s.values= values;
s.key = "Stream";
s.color = "#2ca02c";

data = new Array();
data.push(s);*/

dataExtent = [ 50, 70];
var data, data2;
var chart;

d3.json('/rest/gateways/2/sensors/1/measurements.json?type=1&start=2015-01-01&end=2020-01-01', function(error, incoming_data) {
    if(error){
        throw error;
    }

    var values = incoming_data.measurements;

    values.forEach(function(d) {
        date = new Date(d[0]);
        console.log(date.getTime());
        d.x = date.getTime();
        d.y = +d[1];
    });

    values.sort(function(a, b){
        return a.x - b.x;
    });

    var stream = new Object();
    stream.values= values;
    stream.key = "Measurements";
    stream.color = "#2ca02c";

    data = new Array();
    data[0] = stream;

    data2 = data;

    initializeGraph();
});

function initializeGraph(){
     nv.addGraph(function() {
        chart = nv.models.lineWithFocusChart();

        chart.brushExtent([50,70]);

        chart.xAxis.tickFormat(
            function(d){
                return d3.time.format('%Y-%m-%d')(new Date(d));
            }
        );

        chart.x2Axis.tickFormat(
            function(d){
                return d3.time.format('%Y-%m-%d')(new Date(d));
            }
        );
        chart.yAxis.tickFormat(d3.format(',.2f'));
        chart.y2Axis.tickFormat(d3.format(',.2f'));
        chart.useInteractiveGuideline(true);

        // Set initial range.
        chart.brushExtent([start.valueOf(), end.valueOf()])

        d3.select('#chart-1 svg')
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}

function refresh() {
    var tempDataValues;
    var tempDataValuesOverview;
    d3.json('/rest/gateways/2/sensors/1/measurements.json?type=1&start=2015-01-01&end=2020-01-01', function(error, incoming_data) {
        if(error){
            throw error;
        }

        var values = incoming_data.measurements;

        values.forEach(function(d) {
            date = new Date(d[0]);
            console.log(date.getTime());
            d.x = date.getTime();
            d.y = +d[1];
        });

        values.sort(function(a, b){
            return a.x - b.x;
        });

        tempDataValues = values;
        tempDataValuesOverview = values;

         data[0].values = tempDataValues;
        data2[0].values = tempDataValuesOverview ;
        chart.update();
     });
}

//Update data AJAX
//http://stackoverflow.com/questions/24689157/nvd3-how-to-refresh-the-data-function-to-product-new-data-on-click