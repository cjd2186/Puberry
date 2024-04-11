// Function to display popular items
function displayLobbies() {
    // Get the container where popular items will be displayed
    const ul= $("#LobbyList")
    console.log(lobbies)
    $.each(lobbies, function(index, item) {
        const li = $("<li>");
        const button = $("<button>").addClass("lobby-button")
        button.text("Lobby " + index + ": "+ item[1] + "/" + item[3] + " players");
        button.data("lobby-id", item[0]);
        li.append(button);
        ul.append(li);
    });

    
    //TODO: get route to lobby correct
    $("#LobbyList").on("click", ".lobby-button", function() {
        var lobbyId = $(this).data("lobby-id");
        var lobbyUrl = "/lobby/" + lobbyId;
        window.location.href = lobbyUrl;
    });
    
}

$(document).ready(function(){
    console.log("ues")
    // Generate a UUID (v4)
    const clientId = uuid.v4();
    // Store the generated UUID in localStorage
    localStorage.setItem('clientId', clientId);


    // Establish WebSocket connection with the server and send the clientId
    const socket = io.connect('http://localhost:5000', {
    query: { clientId },
    });
    displayLobbies()
});