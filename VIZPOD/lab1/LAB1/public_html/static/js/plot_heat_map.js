function plotHeatMap() {
    // Set the dimensions and margins of the graph
    const margin = {top: 100, right: 100, bottom: 170, left: 100},
            width = 900 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;
    // Append the svg object to the body of the page
    const svg = d3.select("#svg_heat_map")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);
    // Read the data
    d3.csv("static/data/data_color_final.csv")
            .then(function (data) {

                // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
                const myGroups = Array.from(new Set(data.map(d => d.Song)))
                const myVars = Array.from(new Set(data.map(d => d.Trait)))

                // Build X scales and axis:
                const x = d3.scaleBand()
                        .range([0, width])
                        .domain(myGroups)
                        .padding(0.05);
                svg.append("g")
                        .style("font-size", 12)
                        .attr("transform", `translate(0, ${height})`)
                        .call(d3.axisBottom(x).tickSize(0))
                        .selectAll("text").attr("transform", "rotate(65)")
                        .style("text-anchor", "start")
                        .select(".domain").remove()

                // Build Y scales and axis:
                const y = d3.scaleBand()
                        .range([height, 0])
                        .domain(myVars)
                        .padding(0.05);
                svg.append("g")
                        .style("font-size", 12)
                        .call(d3.axisLeft(y).tickSize(0))
                        .select(".domain").remove()

                // Build color scale
                const myColor = d3.scaleSequential()
                        .interpolator(d3.interpolateInferno) // choosing colors
                        //d3.interpolateInferno //best, RdGy
                        //d3.interpolatePlasma
                        //d3.interpolateMagma
                        //d3.interpolateCividis
                        //d3.interpolateViridis
                        .domain([0, 1]) //adjust for my data

                // Create a tooltip
                const tooltip = d3.select("#svg_heat_map")
                        .append("div")
                        .attr("class", "tooltip")
                        .classed("tooltip", true)

                // Three function that update view when user hover / move / leave a cell
                const mouseover = function (event, d) {
                    tooltip.style("opacity", 0.8)

                    // Select the corresponding dot in the scatterplot
                    d3.select("#svg_scatter_chart")
                            .selectAll("circle")
                            .filter((cd, i) => cd.Song === d.Song)
                            .classed("highlighted", true)

                    // Save the selected trait
                    d3.select("#svg_scatter_chart")
                            .attr("Trait", d.Trait)

                    // Update dot colors in the scatterplot
                    d3.select("#svg_scatter_chart")
                            .selectAll("circle")
                            .style("fill", function (cd) {
                                color = data.filter(function (id) {
                                    return id.Song === cd.Song && id.Trait === d.Trait
                                })
                                return myColor(color[0].Color)
                            })

                    // Update dot colors in the scatterplot by changing color attribute!!!
//                    pca_data_new = d3.select("#svg_scatter_chart")
//                            .selectAll("circle")
//                            .data()
//                            .map(x => x)
//
//                    pca_data_new.map(function (cd) {
//                        color = data.filter(function (id) {
//                            return id.Song === cd.Song && id.Trait === d.Trait
//                        })
//                        cd.Color = color[0].Color
//                        return cd
//                    })
//
//                    d3.select("#svg_scatter_chart")
//                            .selectAll("circle")
//                            .data(pca_data_new, d => d.Song)
//                            .join(
//                                    enter => enter.append("circle"),
//                                    update => update.style("fill", (d, i) => myColor(d.Color)),
//                                    exit => exit.remove()
//                            )


                    // Highlight the corresponding column and row
                    svg.selectAll("rect")
                            .filter((rd, i) => rd === d.Song || rd === d.Trait)
                            .classed("highlighted", true)
                }

                const mousemove = function (event, d) {
                    // Show the tooltip
                    tooltip.html(`The "${d.Trait}" in ${d.Song} is: ${d.value}`)
                            .style("left", (event.x + 20) + "px")
                            .style("top", (event.y + 20) + "px")

                }

                const mouseleave = function (event, d) {
                    // Hide the tooltip
                    tooltip.style("opacity", 0)

                    // Unselect the selected dot in the scatterplot
                    d3.select("#svg_scatter_chart")
                            .selectAll("circle")
                            .filter((cd, i) => cd.Song === d.Song)
                            .classed("highlighted", false)

                    // Remove the column and row highlight
                    svg.selectAll("rect")
                            .filter((rd, i) => rd === d.Song || rd === d.Trait)
                            .classed("highlighted", false)
                }

                // Add the squares
                svg.selectAll()
                        .data(data)
                        .enter()
                        .append("rect")
                        .attr("x", function (d) {
                            return x(d.Song)
                        })
                        .attr("y", function (d) {
                            return y(d.Trait)
                        })
                        .attr("width", x.bandwidth())
                        .attr("height", y.bandwidth())
                        .style("fill", function (d) {
                            return myColor(d.Color)
                        })
                        .style("opacity", 0.8)
                        .classed("highlightable", true)
                        .on("mouseover", mouseover)
                        .on("mousemove", mousemove)
                        .on("mouseleave", mouseleave)

                // Prepare (add) column highlights
                svg.selectAll()
                        .data(myGroups)
                        .enter()
                        .append("rect")
                        .attr("x", function (d) {
                            return x(d)
                        })
                        .attr("y", 0)
                        .attr("width", x.bandwidth())
                        .attr("height", height)
                        .style("fill", "none")
                        .attr("opacity", 1)
                        .classed("highlightable", true)

                // Prepare (add) row highlights
                svg.selectAll()
                        .data(myVars)
                        .enter()
                        .append("rect")
                        .attr("x", 0)
                        .attr("y", function (d) {
                            return y(d)
                        })
                        .attr("width", width)
                        .attr("height", y.bandwidth())
                        .style("fill", "none")
                        .attr("opacity", 1)
                        .classed("highlightable", true)
            })
}