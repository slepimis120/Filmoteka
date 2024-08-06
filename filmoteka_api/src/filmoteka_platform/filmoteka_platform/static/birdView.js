var lastTransform = d3.zoomIdentity;

$(document).ready(function(){
    bird();
});

function bird(){
    let mainNode = d3.select("#mainView").node();

    let observer = new MutationObserver(observer_callback);

    observer.observe(mainNode, {
        subtree: true,
        attributes: true,
        childList: true,
        characterData: true
    });


    d3.select("#mainView").call(d3.zoom()
    .scaleExtent([0.05, 4])
    .on("zoom", function(event) {
        lastTransform = event.transform;
        d3.select("#mainView").select("g").attr("transform", lastTransform);
        updateViewport(lastTransform);
    }));

    updateViewport(lastTransform);
}

function observer_callback(mutationsList, observer) {
    let main = d3.select("#mainView").html();
    d3.select("#birdView").html(main);

    let mainWidth = d3.select("#mainView").select("g").node().getBBox().width;
    let birdWidth = $("#birdView")[0].clientWidth;

    let mainHeight = d3.select("#mainView").select("g").node().getBBox().height;
    let birdHeight = $("#birdView")[0].clientHeight;

    let scaleWidth = birdWidth / mainWidth;
    let scaleHeight = birdHeight / mainHeight;

    let scale = Math.min(scaleWidth, scaleHeight);

    const thresholdScale = 0.2;

    if (scale < thresholdScale) {
        d3.select("#birdView").selectAll("text").remove();
    }

    let x = d3.select("#birdView").select("g").node().getBBox().x;
    let y = d3.select("#birdView").select("g").node().getBBox().y;
    d3.select("#birdView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");

    updateViewport(lastTransform);
}

function updateViewport(transform) {
    let birdViewSvg = d3.select("#birdView");
    let birdWidth = birdViewSvg.node().clientWidth;
    let birdHeight = birdViewSvg.node().clientHeight;

    transform = transform || lastTransform;

    let mainG = d3.select("#mainView").select("g");
    let mainBBox = mainG.node().getBBox();

    let mainWidth = mainBBox.width;
    let mainHeight = mainBBox.height;

    let visibleWidth = birdWidth / transform.k;
    let visibleHeight = birdHeight / transform.k;

    let visibleX = -transform.x / transform.k;
    let visibleY = -transform.y / transform.k;

    let viewportWidth = Math.min(visibleWidth, mainWidth);
    let viewportHeight = Math.min(visibleHeight, mainHeight);

    let viewportX = (visibleX / mainWidth) * birdWidth;
    let viewportY = (visibleY / mainHeight) * birdHeight;

    let viewport = birdViewSvg.selectAll(".viewport").data([0]);

    viewport.enter()
        .append("rect")
        .attr("class", "viewport")
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 1)
        .merge(viewport)  // Update existing .viewport elements
        .attr("x", -transform.x/20)
        .attr("y", -transform.y/20)
        .attr("width", viewportWidth/20)
        .attr("height", viewportHeight/20);

    // Exit: Remove any .viewport elements that are no longer needed
    viewport.exit().remove();
}
