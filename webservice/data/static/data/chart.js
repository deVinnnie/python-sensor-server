/**
 * Wrapper code for loading chart.
 */

/**
* currentRange.start and currentRange.end specify date
* range of values currently in data set.
*/
var currentRange;

var data, data2;
var chart;

/**
 * Convenience method : returns a url with range specifiers based upon a base url.
 */
function makeURL(base_url, start, end){
    var url = base_url + '&start=' + start.format("YYYY-MM-DD") + '&end=' + end.format("YYYY-MM-DD");
    return url;
}

/**
 * @param {int} sensor = id of sensor
 * @param {int} type = id of measurementType
 *
 */
function loadGraph(sensor, type){
    console.log("Load Chart");
    var common_url = base_url + 'sensors/' + sensor + '/measurements.json?type=' + type;
    var url = makeURL(common_url, start, end);

    d3.json(url , function(error, incoming_data){
        // Fetch data for main chart
        console.log(start.format("YYYY-MM-DD") + " " + end.format("YYYY-MM-DD"));
        if(error){
            throw error;
        }

        var values = incoming_data.measurements;

        values.forEach(function(d) {
            date = new Date(d[0]);
            d.x = date.getTime();
            d.y = +d[1];
        });

        values.sort(function(a, b){
            return a.x - b.x;
        });

        var stream = new Object();
        stream.values= values;
        stream.key = "Measurements";
        stream.color = mtypes[type].color;

        data = new Array();
        data[0] = stream;


        // Load data for viewfinder.

        overview_url = base_url + 'sensors/' + sensor + "/measurements/overview.json/?type=" + type + "&step=5";
        d3.json(overview_url , function(error, incoming_data) {
            console.log("Load Viewfinder Chart");
            if(error){
                throw error;
            }

            var values = incoming_data.measurements;

            values.forEach(function(d) {
                date = new Date(d[0]);
                d.x = date.getTime();
                d.y = +d[1];
            });

            values.sort(function(a, b){
                return a.x - b.x;
            });

            var stream = new Object();
            stream.values= values;
            stream.key = "Overview";
            stream.color = mtypes[type].color;

            data2 = new Array();
            data2[0] = stream;

            initializeGraph(sensor, type, common_url);
        });
    });
}

function initializeGraph(sensor, type, updateURL){
     console.log("Init Graph");
     nv.addGraph(function() {
        chart = nv.models.lineWithFocusChart();

        chart.xAxis.tickFormat(
            function(d){
                return d3.time.format('%Y-%m-%d %H:%M')(new Date(d));
            }
        );

        chart.x2Axis.tickFormat(
            function(d){
                return d3.time.format('%Y-%m-%d')(new Date(d));
            }
        );
        chart.yAxis.tickFormat(
            function(d){
                return d3.format(',.2f')(d) + mtypes[type].unit;
            }
        );
        chart.y2Axis.tickFormat(d3.format(',.2f'));

        chart.margin({left: 80});

        chart.useInteractiveGuideline(true);
        chart.forceY(0);

        chart.updateURL = updateURL;

        // Set initial range.
        earliestMeasurementAvailable = moment(data2[0].values[0].x); //Array is already sorted!
        viewFinderStart = earliestMeasurementAvailable.isAfter(start) ? earliestMeasurementAvailable : start;
        chart.brushExtent([viewFinderStart.valueOf(), end.valueOf()]);

        currentRange = {
            "start" : viewFinderStart,
            "end" : end
        };

        chartID = '#chart-sensor-' + sensor + '-type-' + type;
        d3.select(chartID + ' svg')
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}


//Update data AJAX
//http://stackoverflow.com/questions/24689157/nvd3-how-to-refresh-the-data-function-to-product-new-data-on-click