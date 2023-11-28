function plotScatterChart() {

    // Set the dimensions and margins of the graph
    const margin = {top: 10, right: 30, bottom: 30, left: 60},
            width = 500 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

    // Append the svg object to the body of the page
    const svg = d3.select("#svg_scatter_chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                    `translate(${margin.left}, ${margin.top})`)


    // Read the data
    d3.csv("static/data/data_pca.csv")
            .then(function (pca_data) {

                // Add X axis
                const x = d3.scaleLinear()
                        .domain([-0.4, 1.4]) //marked
                        .range([0, width]);
                svg.append("g")
                        .attr("transform", `translate(0, ${height})`)
                        .call(d3.axisBottom(x));

                // Add Y axis
                const y = d3.scaleLinear()
                        .domain([-0.6, 0.8]) //marked
                        .range([height, 0]);
                svg.append("g")
                        .call(d3.axisLeft(y));

                // Create a tooltip
                const tooltip = d3.select("#svg_scatter_chart")
                        .append("div")
                        .attr("class", "tooltip")
                        .classed("tooltip", true)

                // Three function that update view when user hover / move / leave a cell
                const mouseover = function (event, d) {

                    tooltip.style("opacity", 0.8)

                    // Highlight the corresponding dot
                    d3.select(this)
                            .classed("highlighted", true)

                    //Highlight the correponding row in the heatmap
                    trait = d3.select("#svg_scatter_chart")
                            .attr("Trait")
                    d3.select("#svg_heat_map")
                            .selectAll("rect")
                            .filter((rd, i) => rd === trait)
                            .classed("highlighted", true)

                    //Highlight the corresponding cell in the heatmap
                    d3.select("#svg_heat_map")
                            .selectAll("rect")
                            .filter((rd, i) => rd.Trait === trait && rd.Song === d.Song)
                            .classed("highlighted", true)
                }

                const mousemove = function (event, d) {
                    // Show the tooltip
                    tooltip.html(`The selected song is: ${d.Song}`)
                            .style("left", (event.x + 20) + "px")
                            .style("top", (event.y + 20) + "px")
                }


                const mouseleave = function (event, d) {
                    // Hide the tooltip
                    tooltip.style("opacity", 0)


                    // Remove the dot highlight
                    d3.select(this)
                            .classed("highlighted", false)

                    // Remove the row highlight in the heatmap
                    trait = d3.select("#svg_scatter_chart")
                            .attr("Trait")
                    d3.select("#svg_heat_map")
                            .selectAll("rect")
                            .filter((rd, i) => rd === trait)
                            .classed("highlighted", false)

                    // Remove the cell highlight in the heatmap
                    d3.select("#svg_heat_map")
                            .selectAll("rect").filter((rd, i) => rd.Trait === trait && rd.Song === d.Song)
                            .classed("highlighted", false)
                }

                // Add dots
                svg.selectAll()
                        .data(pca_data)
                        .enter()
                        .append("circle")
                        .attr("cx", function (d) {
                            return x(d.Pc1);
                        })
                        .attr("cy", function (d) {
                            return y(d.Pc2);
                        })
                        .attr("r", 7)
                        .style("fill", "grey")
                        .style("opacity", 0.8)
                        .classed("highlightable", true)
                        .on("mouseover", mouseover)
                        .on("mousemove", mousemove)
                        .on("mouseleave", mouseleave)
            })

}