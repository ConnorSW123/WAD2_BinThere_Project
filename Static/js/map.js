let markers = [];  // This will store all the markers globally

// Initialize the map and place markers based on bin data
function initializeMap(binData) {
    var map = L.map('map').setView([55.8723, -4.2882], 18);  // Default view: University of Glasgow

    // OpenStreetMap Tile Layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Custom bin icon
    var greenBinIcon = L.icon({
        iconUrl: "/static/Images/green_bin.png",  // Your custom icon URL
        iconSize: [25, 25],  // Icon size
        iconAnchor: [12.5, 25],  // Point of the icon which will correspond to marker's location
        popupAnchor: [0, -25]  // Point where the popup will appear
    });

    // Add bin markers
    binData.forEach(function(bin) {
        var marker = L.marker([bin.latitude, bin.longitude], { icon: greenBinIcon }).addTo(map);

        // Store the marker globally for future reference (for updates)
        markers.push(marker);  // Save the marker

        marker.binId = bin.id;  // Attach the bin ID to the marker for easy reference
        marker.binData = bin;  // Attach the bin data to the marker so we can access it later
        marker.binData.user_vote = null; // Initialize user vote as null (no vote)

        marker.bindPopup(createPopupContent(bin));  // Bind the popup to the marker
    });
}

// Create popup content for each bin
function createPopupContent(bin) {
    return `
        <div style="font-family: 'Yomogi', sans-serif;">
            <h5>${bin.location_name}</h5>
            <p><strong>Bin Types:</strong> ${bin.bin_types.join(', ')}</p>
            <div class="vote-buttons">
                <button id="upvote-button-${bin.id}" onclick="vote(${bin.id}, 1)">Upvote (${bin.upvotes})</button>
                <button id="downvote-button-${bin.id}" onclick="vote(${bin.id}, 0)">Downvote (${bin.downvotes})</button>
            </div>
        </div>
    `;
}

function vote(binId, voteType) {
    console.log(`Voting on bin ${binId}, Type: ${voteType}`);

    const upvoteButton = document.getElementById(`upvote-button-${binId}`);
    const downvoteButton = document.getElementById(`downvote-button-${binId}`);

    // Disable buttons during request
    upvoteButton.disabled = true;
    downvoteButton.disabled = true;

    fetch(`vote/${binId}/${voteType}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // Get CSRF token from meta tag
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Update the vote counts visually
            upvoteButton.innerText = `Upvote (${data.upvotes})`;
            downvoteButton.innerText = `Downvote (${data.downvotes})`;

            // Update the vote state in the marker data
            updateVoteButtonStyles(binId, data.user_vote);  // Use the user_vote from the response

            // Re-render the map with updated bin data (only update the specific bin)
            updateBinMarker(binId, data.upvotes, data.downvotes, data.user_vote);
        }
    })
    .catch(error => {
        console.error("Error voting:", error);
        alert("An error occurred while voting. Please Sign In to Vote!");
    })
    .finally(() => {
        upvoteButton.disabled = false;
        downvoteButton.disabled = false;
    });
}

// Function to update the marker on the map with new vote counts
function updateBinMarker(binId, upvotes, downvotes, user_vote) {
    // Find the marker for the bin by its id
    const marker = markers.find(marker => marker.binId === binId); // 'markers' is the array holding your map markers
    if (marker) {
        // Update the marker data
        marker.binData.upvotes = upvotes;
        marker.binData.downvotes = downvotes;
        marker.binData.user_vote = user_vote;  // Store the user's vote status

        // Update the popup content with new vote counts
        marker.setPopupContent(createPopupContent(marker.binData));

        // Update the displayed upvote and downvote buttons in the popup
        const upvoteButton = document.getElementById(`upvote-button-${binId}`);
        const downvoteButton = document.getElementById(`downvote-button-${binId}`);
        upvoteButton.innerText = `Upvote (${upvotes})`;
        downvoteButton.innerText = `Downvote (${downvotes})`;

        // Reapply button styles based on current vote state (upvoted or downvoted)
        updateVoteButtonStyles(binId, user_vote);
    }
}

function updateVoteButtonStyles(binId, user_vote) {
    const upvoteButton = document.getElementById(`upvote-button-${binId}`);
    const downvoteButton = document.getElementById(`downvote-button-${binId}`);

    // Reset all buttons to default
    upvoteButton.classList.remove('upvoted', 'default');
    downvoteButton.classList.remove('downvoted', 'default');

    // Check and apply the user's current vote status
    if (user_vote === 1) {
        upvoteButton.classList.add('upvoted');
    } else if (user_vote === 0) {
        downvoteButton.classList.add('downvoted');
    } else {
        upvoteButton.classList.add('default'); // Add default for no vote
        downvoteButton.classList.add('default'); // Add default for no vote
    }
}


// Get CSRF token from meta tag
function getCSRFToken() {
    return document.querySelector("meta[name='csrf-token']").getAttribute("content");
}
