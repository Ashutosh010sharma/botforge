(async function(){
    let sessionId=localStorage.getItem("botforge_session");
   
    if(!sessionId){
        sessionId=crypto.randomUUID();
        localStorage.setItem("botforge_session",sessionId);
    }

    const currentScript = document.currentScript;
    const baseUrl = new URL(currentScript.src).origin;

    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = baseUrl + "/static/widget/widget.css";
    document.head.appendChild(css);

    const widgetKey = currentScript.getAttribute("data-widget-key");

    const apiUrl = baseUrl + "/bots/widget/chat/" + widgetKey + "/";
    const configUrl = baseUrl + "/bots/widget/config/" + widgetKey + "/";

    let botConfig = null;

    async function loadConfig(){
        const response = await fetch(configUrl);
        botConfig = await response.json();
    }

    await loadConfig();

    // Injects the dynamic branding color from backend configuration data
    document.documentElement.style.setProperty(
        "--bf-primary",
        botConfig.color
    );

   const widget = `
    <!-- Floating Chat Trigger Button -->
    <div id="botforge-widget-btn">
        <svg id="bf-icon-chat" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <svg id="bf-icon-close" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </div>

    <!-- Chat Box Window -->
    <div id="botforge-chat-window">

        <!-- Header -->
        <div id="botforge-chat-header">
            <div class="bf-header-profile">
                <span class="bf-online-dot"></span>
                <div class="bf-header-text">
                    <span class="bf-bot-name">${botConfig.name}</span>
                    <span class="bf-bot-status">Online</span>
                </div>
            </div>
        </div>

        <!-- Scrollable Chat Body Area -->
        <div id="botforge-chat-body">
            <div class="bf-row bf-row-bot">
                <div class="bf-msg bf-msg-bot">
                    ${botConfig.welcome_message}
                </div>
            </div>
        </div>

        <!-- Interactive Footer with Inputs and Branding -->
        <div id="botforge-chat-footer" style="display: flex; flex-direction: column; gap: 8px;">
            
            <!-- Input Row -->
            <div style="display: flex; align-items: center; width: 100%; gap: 8px;">
                <input type="text" id="botforge-message" placeholder="Type your message here..." style="flex-grow: 1;">
                <button type="button" id="botforge-send">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
            </div>

            <!-- Integrated Minimal Brand Link -->
            <div style="text-center: center; width: 100%; text-align: center; margin-top: 2px;">
                <small style="font-size: 11px; color: #64748b; display: inline-flex; align-items: center; gap: 3px; font-family: system-ui, sans-serif;">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="#eab308" stroke="#eab308" style="vertical-align: middle;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                    by 
                    <a href="${baseUrl}" target="_blank" style="color: var(--bf-primary, #20c997); font-weight: 600; text-decoration: none; transition: opacity 0.15s ease;">
                        BotForge
                    </a>
                </small>
            </div>

        </div>

    </div>`;

    document.body.insertAdjacentHTML("beforeend", widget);

    const btn = document.getElementById("botforge-widget-btn");
    const windowBox = document.getElementById("botforge-chat-window");

    // Left alignment handling override
    if(botConfig.position==="bottom-left"){

    btn.style.left="20px";
    btn.style.right="auto";

    windowBox.style.left="20px";
    windowBox.style.right="auto";

}else{

    btn.style.right="20px";
    btn.style.left="auto";

    windowBox.style.right="20px";
    windowBox.style.left="auto";
}

    const chatIcon = document.getElementById("bf-icon-chat");
    const closeIcon = document.getElementById("bf-icon-close");

    btn.addEventListener("click", function(){
        if(windowBox.style.display === "flex"){
            windowBox.style.display = "none";
            chatIcon.style.display = "block";
            closeIcon.style.display = "none";
        } else {
            windowBox.style.display = "flex";
            chatIcon.style.display = "none";
            closeIcon.style.display = "block";
        }
    });

    const sendBtn = document.getElementById("botforge-send");
    const input = document.getElementById("botforge-message");
    const chatBody = document.getElementById("botforge-chat-body");

    async function sendMessage(){
        const message = input.value.trim();
        if(!message) return;

        // Render user message bubble
        chatBody.innerHTML += `
        <div class="bf-row bf-row-user">
            <div class="bf-msg bf-msg-user">${message}</div>
        </div>`;

        chatBody.scrollTop = chatBody.scrollHeight;
        input.value = "";

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message,
                    session_id:sessionId
                })
            });

            const data = await response.json();

            // Render chatbot response bubble
            chatBody.innerHTML += `
            <div class="bf-row bf-row-bot">
                <div class="bf-msg bf-msg-bot">${data.response}</div>
            </div>`;

        } catch(error) {
            console.error(error);

            // Render clean error block message
            chatBody.innerHTML += `
            <div class="bf-row bf-row-bot">
                <div class="bf-msg bf-msg-bot" style="color: #dc3545; border-color: rgba(220, 53, 69, 0.2);">
                    Something went wrong. Please try again.
                </div>
            </div>`;
        }

        chatBody.scrollTop = chatBody.scrollHeight;
    }

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keypress", function(e){
        if(e.key === "Enter") sendMessage();
    });

})();