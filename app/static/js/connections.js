// Array of  connections data
const connections = [
    { name: "Alex Johnson", title: "Software Engineer at TechCorp" },
    { name: "Emily Davis", title: "Graphic Designer at Creatives Inc." },
    { name: "Michael Lee", title: "Marketing Manager at Marketify" }
];


// Array of  connections data
const peopleYouMayKnow = [
    { name: "Alex Johnson", title: "Software Engineer at TechCorp" },
    { name: "Emily Davis", title: "Graphic Designer at Creatives Inc." },
    { name: "Michael Lee", title: "Marketing Manager at Marketify" }
];


// Function to create connection card
function createConnectionCard(connection, buttonText) {
    const card = document.createElement("div");
    card.className = "connection-card";

    // Sample placeholder profile image
    const img = document.createElement("img");
    img.src = "https://via.placeholder.com/80";
    img.alt = `${connection.name}'s profile picture`;

    const name = document.createElement("h3");
    name.textContent = connection.name;

    const title = document.createElement("p");
    title.textContent = connection.title;

    const buttonContainer = document.createElement("div");
    buttonContainer.className = "button-container";

    const messageBtn = document.createElement("button");
    messageBtn.className = "message-btn";
    messageBtn.textContent = "Message";

    const actionBtn = document.createElement("button");
    actionBtn.className = buttonText === "Schedule" ? "schedule-btn" : "connect-btn";
    actionBtn.textContent = buttonText;

    const profileBtn = document.createElement("button");
    profileBtn.className = "profile-btn";
    profileBtn.textContent = "Profile";

    buttonContainer.appendChild(messageBtn);
    buttonContainer.appendChild(actionBtn);
    buttonContainer.appendChild(profileBtn);

    card.appendChild(img);
    card.appendChild(name);
    card.appendChild(title);
    card.appendChild(buttonContainer);

    return card;
}

// Function to load connections
function loadConnections() {
    const connectionsContainer = document.getElementById("connections-container");
    const mayKnowContainer = document.getElementById("may-know-container");

    // Clear existing content
    connectionsContainer.innerHTML = "";
    mayKnowContainer.innerHTML = "";

    // Load your connections
    connections.forEach(connection => {
        const card = createConnectionCard(connection, "Schedule");
        connectionsContainer.appendChild(card);
    });

    // Load people you may know
    peopleYouMayKnow.forEach(person => {
        const card = createConnectionCard(person, "Connect");
        mayKnowContainer.appendChild(card);
    });

    // Add search functionality
    setupSearch("connections-search", connectionsContainer, connections, "Schedule");
    setupSearch("may-know-search", mayKnowContainer, peopleYouMayKnow, "Connect");
}

// Function to setup search functionality
function setupSearch(searchInputId, container, dataArray, buttonText) {
    const searchInput = document.getElementById(searchInputId);
    
    searchInput.addEventListener("input", function() {
        // Get the search term and convert to lowercase
        const searchTerm = this.value.toLowerCase().trim();
        
        // Clear the current container
        container.innerHTML = "";
        
        // Filter the connections based on the search term
        const filteredConnections = dataArray.filter(connection => 
            connection.name.toLowerCase().includes(searchTerm) || 
            connection.title.toLowerCase().includes(searchTerm)
        );
        
        // Recreate connection cards for filtered results
        filteredConnections.forEach(connection => {
            const card = createConnectionCard(connection, buttonText);
            container.appendChild(card);
        });
        
        // If no results, show a message
        if (filteredConnections.length === 0) {
            const noResultsMessage = document.createElement("p");
            noResultsMessage.textContent = "No connections found.";
            noResultsMessage.classList.add("no-results");
            container.appendChild(noResultsMessage);
        }
    });
}

// Load connections when the page loads
window.onload = loadConnections;
