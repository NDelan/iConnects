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


// Function to load connections
function loadConnections() {
    const container = document.getElementById("connections-container");
    const mayKnowContainer = document.getElementById("may-know-container");

    // Load your connections
    connections.forEach(connection => {
        createConnectionCard(container, connection, "Schedule");
    });

    // Load people you may know
    peopleYouMayKnow.forEach(person => {
        createConnectionCard(mayKnowContainer, person, "Connect");
    });
}

function createConnectionCard(container, connectionData, buttonText) {
    const card = document.createElement("div");
    card.className = "connection-card";

    // Sample placeholder profile image
    const img = document.createElement("img");
    img.src = "https://via.placeholder.com/80";
    img.alt = `${connectionData.name}'s profile picture`;

    const name = document.createElement("h3");
    name.textContent = connectionData.name;

    const title = document.createElement("p");
    title.textContent = connectionData.title;

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

    container.appendChild(card);
}

// Load connections when the page loads
window.onload = loadConnections;
