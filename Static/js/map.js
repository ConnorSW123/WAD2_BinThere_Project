function initializeMap(binData) {
    console.log("Initializing map with data:", binData);

    var map = L.map('map').setView([55.8723, -4.2882], 18);  // Default view: University of Glasgow

    // OpenStreetMap Tile Layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Custom bin icon
    var greenBinIcon = L.icon({
        iconUrl: "/static/Images/green_bin.png",
        iconSize: [25, 25],
        iconAnchor: [12.5, 25],
        popupAnchor: [0, -25]
    });

    // Add bin markers
    binData.forEach(function(bin) {
        var marker = L.marker([bin.latitude, bin.longitude], { icon: greenBinIcon }).addTo(map);
        marker.bindPopup(createPopupContent(bin));
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

// Handle bin upvotes and downvotes
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
            // Update vote count visually
            upvoteButton.innerText = `Upvote (${data.upvotes})`;
            downvoteButton.innerText = `Downvote (${data.downvotes})`;
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

// Get CSRF token from meta tag
function getCSRFToken() {
    return document.querySelector("meta[name='csrf-token']").getAttribute("content");
}
