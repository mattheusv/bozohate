function shortMonthTickFormat(date) {
    return d3.timeFormat(d3.timeYear(date) < date ? '%b' : '%Y')(date);
}

function parseDate(item, index) {
    item.date_used = d3.timeParse("%Y-%m-%d")(item.date_used)
}

// set the dimensions and margins of the graph
var margin = { top: 20, right: 30, bottom: 30, left: 80 },
    width = (1060 - margin.left - margin.right),
    height = (500 - margin.top - margin.bottom),
    barPadding = .3;

// append the svg object to the body of the page
var svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

$.ajax({
    type: "GET",
    dataType: "json",
    url: "api/tweet/computed",
    success: function (data) {

        // Add X axis
        var x = d3.scaleBand()
            .domain(data.map(function(d) { return d.date_used; }))
            .range([0, width])
            .padding(barPadding);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickSize(0));

        // Add Y left axis
        var yLeft = d3.scaleLinear()
            .domain([0, d3.max(data, function (d) { return d.total_data; })])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(yLeft));

        var subgroups = ["total_data", "negative_percent"];

        var xSubgroup = d3.scaleBand()
            .domain(subgroups)
            .range([0, x.bandwidth()])
            .padding([0.05]);

        //bar
        svg.append("g")
            .selectAll("g")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", function(d) { return x(d.date_used); })
                .attr("y", function(d) { return yLeft(d.negative_value); })
                .attr("width", xSubgroup.bandwidth())
                .attr("height", function(d) {
                    return height - yLeft(d.negative_value); 
                })
            .attr("fill", "steelblue");

        svg.append("g").selectAll("g")
            .data(data)
            .enter()
            .append("rect")
            .attr("transform", "translate(93, 0)")
            .attr("x", function(d) { return x(d.date_used); })
                .attr("y", function(d) { return yLeft(d.total_data); })
                .attr("width", xSubgroup.bandwidth())
                .attr("height", function(d) {
                    return height - yLeft(d.total_data); 
                })
            .attr("fill", "red");

        var legend = svg.append("text")
            .attr("x", (margin.left + width / 2))
            .attr("y", height + margin.top + 7)
            .attr("text-anchor", "middle");
        legend.append("tspan")
            .attr("fill", "steelblue")
            .text("\u2B24");
        legend.append("tspan")
            .attr("dx", "0.3em")
            .text("negatives tweets");
        legend.append("tspan")
            .attr("fill", "red")
            .attr("dx", "0.9em")
            .text("\u2B24");
        legend.append("tspan")
            .attr("dx", "0.3em")
            .text("total tweets");

    }
});
