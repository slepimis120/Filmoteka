document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[placeholder="File:"]');
    const searchInput = document.querySelector('input[placeholder="Search:"]');

    const suggestionsBox = document.createElement('div');
    suggestionsBox.classList.add('suggestions-box');
    searchInput.parentNode.appendChild(suggestionsBox);

    let typingTimer;
    const typingDelay = 2000;

    searchInput.addEventListener('input', function() {
        clearTimeout(typingTimer);
        if (searchInput.value.trim()) {
            typingTimer = setTimeout(fetchMovieSuggestions, typingDelay);
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

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

        if (searchInput.value.trim() && !fileInput.value.trim()) {
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

                initializeTreeView();
            })
            .catch(error => console.error('Fetch error:', error)); // Handle fetch errors
        } else if (fileInput.value.trim() && !searchInput.value.trim()) {
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

                initializeTreeView();
            })
            .catch(error => console.error('Fetch error:', error)); // Handle fetch errors
        } else {
            console.error('Invalid input: please provide either a file or a search query.');
        }
    });

function initializeTreeView() {
    fetch('/get_graph_data/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(graph => {
        let treeViewManager = createTreeViewManager();

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
            treeViewManager.setTreeView(graph.root_id);
        } else {
            console.error('Root ID is not provided or graph data is empty.');
        }
    })
    .catch(error => console.error('Error fetching graph data:', error));
}

});

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
