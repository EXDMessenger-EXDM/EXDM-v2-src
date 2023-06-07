let content = document.getElementById('content');

function general_info() {
    content.innerHTML = `
    <h1>General Info</h1>
    <p>Here you can see the main information about the application</p>
    <input type="text" placeholder="Application name">
    <p>Auth token (AppID encoded to Base64).(Random letters and numbers encoded to Base64 and hashed with SHA256).(Random letters and numbers):</p>`;
}

function access() {
    content.innerHTML = `
    <h1>Access</h1>
    <p>Here you can configure API access</p>
    <input type="checkbox" id="accessGuilds"/><label for="accessGuilds">Access to servers (channels, roles)</label><br><br>
    <input type="checkbox" id="accessUsers"/><label for="accessUsers">Access to users (avatar, bio, etc)</label><br><br>
    <input type="checkbox" id="accessMessages"/><label for="accessMessages">Access to messages (message content)</label><br><br>
    <input type="checkbox" id="accessAi"/><label for="accessAi">Access to AI features (Text completion, DALL-E, etc)</label><br><br>
    `;
}