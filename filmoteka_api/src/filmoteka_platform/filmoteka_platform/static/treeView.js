function createTreeViewManager() {
    let nodes, links, directed;
    let treeViewContainer = d3.select("#treeView"); // Select the correct element

    function clearTreeView(){
        treeViewContainer.html(''); // Clear the tree view
    }

    function setTreeView(id) {
        clearTreeView();

        let parentElement = treeViewContainer.append('li');
        let toggler = parentElement.append('span').attr('class', 'caret').text(id);
        toggler.on('click', () => {
            if (toggler.classed('caret-down')) {
                toggler.classed('caret-down', false);
                parentElement.select('ul').remove();
            } else {
                toggler.classed('caret-down', true);
                generateSubTreeView(parentElement, id);
            }
        });
    }

    function generateSubTreeView(parent, id) {
    let nodeContent = parent.append('ul');
    for (let name in nodes[id]) {
        console.log("Adding attribute:", name, "with value:", nodes[id][name]);
        nodeContent.append('li').text(name + ": " + nodes[id][name]);
    }

    const nodeLinks = links.filter((link) => link.source == id);
    if(!directed){
        for(let l of links.filter(link => link.target == id)){
            nodeLinks.push({source: l.target, target: l.source});
        }
    }

    for (let child of nodeLinks) {
        let childId = child.target;
        console.log("Adding child node:", childId);
        let childNode = nodeContent.append('li');
        let togglerChildNode = childNode.append('span').attr('class', 'caret').text(childId);
        togglerChildNode.on('click', () => {
            if (togglerChildNode.classed('caret-down')) {
                togglerChildNode.classed('caret-down', false);
                childNode.select('ul').remove();
            } else {
                togglerChildNode.classed('caret-down', true);
                generateSubTreeView(childNode, childId);
            }
        });
    }
}


    function setTreeViewData(graph) {
        clearTreeView();
        nodes = graph.nodes;
        links = graph.links;
        directed = graph.directed;
    }

    return {
        setTreeView,
        setTreeViewData,
        clearTreeView
    };
}
