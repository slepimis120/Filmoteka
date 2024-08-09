document.addEventListener('DOMContentLoaded', function() {
    // Existing functionality from index.js
    const fileInput = document.querySelector('input[placeholder="File:"]');
    const searchInput = document.querySelector('input[placeholder="Search:"]');
    const attributeSelect = document.getElementById('attribute-select');
    const operatorSelect = document.getElementById('operator-select');
    const filterValueInput = document.getElementById('filter-value');
    const suggestionsBox = document.createElement('div');
    suggestionsBox.classList.add('suggestions-box');
    searchInput.parentNode.appendChild(suggestionsBox);

    let typingTimer;
    const typingDelay = 2000;

    searchInput.addEventListener('input', function() {
        clearTimeout(typingTimer);
        toggleInputs('search');
        if (searchInput.value.trim()) {
            typingTimer = setTimeout(fetchMovieSuggestions, typingDelay);
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

    fileInput.addEventListener('input', function() {
        toggleInputs('file');
    });

    filterValueInput.addEventListener('input', function() {
        toggleInputs('filter');
    });

    function toggleInputs(activeInput) {
        if (activeInput === 'search') {
            fileInput.disabled = true;
            filterValueInput.disabled = true;
            fileInput.style.backgroundColor = '#d3d3d3'; // grey out
            filterValueInput.style.backgroundColor = '#d3d3d3'; // grey out
        } else if (activeInput === 'file') {
            searchInput.disabled = true;
            filterValueInput.disabled = true;
            searchInput.style.backgroundColor = '#d3d3d3'; // grey out
            filterValueInput.style.backgroundColor = '#d3d3d3'; // grey out
        } else if (activeInput === 'filter') {
            searchInput.disabled = true;
            fileInput.disabled = true;
            searchInput.style.backgroundColor = '#d3d3d3'; // grey out
            fileInput.style.backgroundColor = '#d3d3d3'; // grey out
        }

        if (!searchInput.value.trim() && !fileInput.value.trim() && !filterValueInput.value.trim()) {
            searchInput.disabled = false;
            fileInput.disabled = false;
            filterValueInput.disabled = false;
            searchInput.style.backgroundColor = '';
            fileInput.style.backgroundColor = '';
            filterValueInput.style.backgroundColor = '';
        }
    }

    function fetchMovieSuggestions() {
        const query = searchInput.value.trim();
        if (!query) return;

        fetch(`/tmdb_search?query=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            displaySuggestions(data.results);
        })
        .catch(error => console.error('Fetch error:', error));
    }

    function displaySuggestions(movies) {
        suggestionsBox.innerHTML = '';
        movies.forEach(movie => {
            const suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.textContent = movie.title;
            suggestionItem.addEventListener('click', function() {
                searchInput.value = movie.title;
                suggestionsBox.innerHTML = '';
            });
            suggestionsBox.appendChild(suggestionItem);
        });
    }

    fileInput.addEventListener('input', function() {
        searchInput.disabled = fileInput.value.trim() !== "";
    });

    searchInput.addEventListener('input', function() {
        fileInput.disabled = searchInput.value.trim() !== "";
    });

    document.querySelector('button[type="submit"]').addEventListener('click', function(event) {
        event.preventDefault();

        if (filterValueInput.value.trim() && !searchInput.value.trim() && !fileInput.value.trim()) {
            const attribute = attributeSelect.value;
            const operator = operatorSelect.value;
            const value = filterValueInput.value.trim();

            fetch('/add_filter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ attribute, operator, value })
            })
            .then(response => response.text())
            .then(data => {
                document.open();
                document.write(data);
                document.close();

                initializeTreeView();
                fetchAndDisplayFilters();
            })
            .catch(error => console.error('Fetch error:', error)); // Handle fetch errors
        } else if (searchInput.value.trim() && !fileInput.value.trim() && !filterValueInput.value.trim()) {
            fetch('/generate_and_visualize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ search: searchInput.value.trim() })
            })
            .then(response => response.text())
            .then(data => {
                document.open();
                document.write(data);
                document.close();

                fetchAndDisplayFilters();
                initializeTreeView();
            })
            .catch(error => console.error('Fetch error:', error)); // Handle fetch errors
        } else if (fileInput.value.trim() && !searchInput.value.trim() && !filterValueInput.value.trim()) {
            fetch('/parse_and_visualize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ file_path: fileInput.value.trim() })
            })
            .then(response => response.text())
            .then(data => {
                document.open();
                document.write(data);
                document.close();

                fetchAndDisplayFilters();
                initializeTreeView();
            })
            .catch(error => console.error('Fetch error:', error)); // Handle fetch errors
        } else {
            console.error('Invalid input: please provide valid input.');
        }
    });

    fetch('/get_graph_attributes', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(attributes => {
        populateAttributeDropdown(attributes);
    })
    .catch(error => console.error('Error fetching attributes:', error));

    function populateAttributeDropdown(attributes) {
        attributeSelect.innerHTML = '';

        if (Object.keys(attributes).length === 0) {
            // Handle the case when no attributes are returned
            const option = document.createElement('option');
            option.textContent = 'No attributes available';
            attributeSelect.appendChild(option);
            updateOperatorDropdown(null); // No type available
            return;
        }

        for (const [attrName, attrType] of Object.entries(attributes)) {
            const option = document.createElement('option');
            option.value = attrName;
            option.textContent = attrName;
            option.dataset.type = attrType;
            attributeSelect.appendChild(option);
        }

        // Select the first option if available and update operator dropdown
        if (attributeSelect.options.length > 0) {
            updateOperatorDropdown(attributeSelect.options[0].dataset.type);
        }
    }

    attributeSelect.addEventListener('change', function() {
        const selectedOption = attributeSelect.options[attributeSelect.selectedIndex];
        updateOperatorDropdown(selectedOption.dataset.type);
    });

    function updateOperatorDropdown(type) {
        operatorSelect.innerHTML = '';

        let operators;
        if (type === null) {
            const option = document.createElement('option');
            option.textContent = 'No operators available';
            operatorSelect.appendChild(option);
            return;
        }

        if (type === 'float' || type === 'int') {
            operators = ['==', '>', '>=', '<', '<=', '!=', 'contains'];
        } else if (type === 'str') {
            operators = ['==', 'contains'];
        } else {
            console.error('Unknown attribute type:', type);
            return;
        }

        operators.forEach(op => {
            const option = document.createElement('option');
            option.value = op;
            option.textContent = op;
            operatorSelect.appendChild(option);
        });
    }

    function initializeTreeView() {
        console.log('Initializing TreeView');
        fetch('/get_graph_data/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(graph => {
            console.log('Graph data fetched:', graph);
            let treeViewManager = createTreeViewManager();
            console.log("TreeView Manager created:", treeViewManager);

            treeViewManager.setTreeViewData({
                nodes: graph.vertices.reduce((obj, vertex) => {
                    obj[vertex.id] = vertex.attributes;
                    return obj;
                }, {}),
                links: graph.edges.map(edge => ({
                    source: edge.start_vertex,
                    target: edge.end_vertex
                })),
                directed: true
            });

            if (graph.root_id) {
                console.log('Root ID:', graph.root_id);
                treeViewManager.setTreeView(graph.root_id);
            } else {
                console.error('Root ID is not provided or graph data is empty.');
            }
        })
        .catch(error => console.error('Error fetching graph data:', error));
    }

    // Added functionality from filter.js
    function fetchAndDisplayFilters() {
        fetch('/get_graph_filters/')
            .then(response => response.json())
            .then(filters => {
                const appliedQueriesDiv = document.querySelector('.applied-queries');
                appliedQueriesDiv.innerHTML = ''; // Clear previous filters

                filters.forEach((filter, index) => {
                    // Generate a unique ID based on the filter's attributes
                    const filterId = `filter-${index}-${filter.parameter_name}-${filter.comparator}-${filter.value}`;

                    const filterDiv = document.createElement('div');
                    filterDiv.className = 'filter-item';
                    filterDiv.innerHTML = `${filter.parameter_name} ${filter.comparator} ${filter.value} <button class="remove-filter" data-filter-id="${filterId}">x</button>`;

                    appliedQueriesDiv.appendChild(filterDiv);
                });

                // Add event listeners to remove filter buttons
                document.querySelectorAll('.remove-filter').forEach(button => {
                    button.addEventListener('click', function() {
                        const filterId = this.getAttribute('data-filter-id');
                        removeFilter(filterId);
                    });
                });
            })
            .catch(error => console.error('Error fetching filters:', error));
    }

    function removeFilter(filterId) {
        const parts = filterId.split('-');
        const parameter_name = parts[2];
        const comparator = parts[3];
        const value = parts[4];

        const filterData = JSON.stringify({
            attribute: parameter_name,
            operator: comparator,
            value: value
        });

        fetch('/remove_filter/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: filterData
        })
        .then(response => response.text())
        .then(data => {
            document.open();
            document.write(data);
            document.close();

            fetchAndDisplayFilters();
            initializeTreeView();
        })
        .catch(error => console.error('Error removing filter:', error));
    }

    fetchAndDisplayFilters(); // Initial call to populate filters on page load

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
