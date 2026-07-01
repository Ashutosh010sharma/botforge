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
    const mobileOffset = parseInt(currentScript.getAttribute("data-bottom-offset") ?? "24", 10);

    // Apply only on mobile
    const bottomOffset = window.innerWidth <= 768 ? mobileOffset : 24;

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

    function getTime(){
        return new Date().toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"});
    }

    // Escapes user-provided / bot-provided text so markup can never break bubble layout
    function escapeHtml(str){
        const div = document.createElement("div");
        div.textContent = String(str ?? "");
        return div.innerHTML;
    }

   const widget = `
    <!-- Floating Chat Trigger Button (only ever shows the chat icon;
         it hides itself while the chat window is open) -->
    <div id="botforge-widget-btn">

    <svg id="bf-icon-chat"
         width="22"
         height="22"
         viewBox="0 0 24 24"
         fill="none"
         stroke="currentColor"
         stroke-width="2"
         stroke-linecap="round"
         stroke-linejoin="round">

        <path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/>

        <path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/>

        <path d="M5 15l.6 1.4L7 17l-1.4.6L5 19l-.6-1.4L3 17l1.4-.6L5 15z"/>

    </svg>

</div>

    <!-- Chat Box Window -->
    <div id="botforge-chat-window">

        <!-- Header -->
        <div id="botforge-chat-header">
            <div class="bf-header-profile">
                <div class="bf-avatar">
                   <svg width="17"
         height="17"
         viewBox="0 0 24 24"
         fill="none"
         stroke="currentColor"
         stroke-width="2"
         stroke-linecap="round"
         stroke-linejoin="round">

        <path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/>

        <path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/>

        <path d="M5 15l.6 1.4L7 17l-1.4.6L5 19l-.6-1.4L3 17l1.4-.6L5 15z"/>

    </svg>
                </div>
                <div class="bf-header-text">
                    <span class="bf-bot-name">${botConfig.name}</span>
                    <span class="bf-bot-status">
                        <span class="bf-online-dot"></span>
                        Online · Ready to help
                    </span>
                </div>
            </div>

            <!-- Header Close Button -->
            <button type="button" id="botforge-header-close" aria-label="Close chat">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        </div>

        <!-- Scrollable Chat Body Area -->
        <div id="botforge-chat-body">
            <div class="bf-row bf-row-bot">
                <div class="bf-msg-wrap">
                    <div class="bf-msg bf-msg-bot">${botConfig.welcome_message}</div>
                    <span class="bf-time">${getTime()}</span>
                </div>
            </div>
        </div>

        <!-- Interactive Footer with Inputs and Branding -->
        <div id="botforge-chat-footer">
            
            <!-- Input Row -->
            <div>
                <input type="text" id="botforge-message" placeholder="Type a message…">
                <button type="button" id="botforge-send">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
            </div>

            <!-- Integrated Minimal Brand Link -->
            <div>
                <small>
                    <svg width="9" height="9" viewBox="0 0 24 24" fill="#eab308" stroke="#eab308" style="vertical-align:middle;flex-shrink:0;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                    Powered by&nbsp;<a href="${baseUrl}" target="_blank">BotForge</a>
                </small>
            </div>

        </div>

    </div>`;

    document.body.insertAdjacentHTML("beforeend", widget);

    const btn = document.getElementById("botforge-widget-btn");
    const windowBox = document.getElementById("botforge-chat-window");
    const headerCloseBtn = document.getElementById("botforge-header-close");

    // Position handling
   if (botConfig.position === "bottom-left") {

        btn.style.left = "24px";
        btn.style.right = "auto";
        btn.style.bottom = bottomOffset + "px";

        windowBox.style.left = "24px";
        windowBox.style.right = "auto";
        windowBox.style.bottom = (bottomOffset + 20) + "px";

    } else {

        btn.style.right = "24px";
        btn.style.left = "auto";
        btn.style.bottom = bottomOffset + "px";

        windowBox.style.right = "24px";
        windowBox.style.left = "auto";
        windowBox.style.bottom = (bottomOffset + 20) + "px";

    }

    function openChat(){
        windowBox.style.display = "flex";
        // The launcher button hides while the chat window is open —
        // the window sits in the same corner, so showing both is redundant.
        btn.style.display = "none";
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function closeChat(){
        windowBox.style.display = "none";
        // Bring the launcher button back so the chat can be reopened.
        btn.style.display = "flex";
    }

    // Launcher button only opens the chat (it's hidden whenever the chat is open)
    btn.addEventListener("click", openChat);

    // Cross button inside the header is the only way to close the chat window
    headerCloseBtn.addEventListener("click", closeChat);

    const sendBtn = document.getElementById("botforge-send");
    const input = document.getElementById("botforge-message");
    const chatBody = document.getElementById("botforge-chat-body");

    function appendRow(side, html, timeText){
        const row = document.createElement("div");
        row.className = "bf-row bf-row-" + side;

        const wrap = document.createElement("div");
        wrap.className = "bf-msg-wrap";

        const msg = document.createElement("div");
        msg.className = "bf-msg bf-msg-" + side;
        msg.innerHTML = html;
        wrap.appendChild(msg);

        if(timeText){
            const time = document.createElement("span");
            time.className = "bf-time";
            time.textContent = timeText;
            wrap.appendChild(time);
        }

        row.appendChild(wrap);
        chatBody.appendChild(row);
        return row;
    }

    async function sendMessage(){
        const message = input.value.trim();
        if(!message) return;

        const t = getTime();

        // User bubble (escaped so long / short / special-character text never breaks layout)
        appendRow("user", escapeHtml(message), t);

        chatBody.scrollTop = chatBody.scrollHeight;
        input.value = "";

        // Typing indicator
        const typingRow = document.createElement("div");
        typingRow.className = "bf-row bf-row-bot";
        typingRow.innerHTML = `
            <div class="bf-typing-indicator">
                <span></span><span></span><span></span>
            </div>`;
        chatBody.appendChild(typingRow);
        chatBody.scrollTop = chatBody.scrollHeight;

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message, session_id: sessionId })
            });

            const data = await response.json();

            typingRow.remove();

            appendRow("bot", escapeHtml(data.response), getTime());

        } catch(error) {
            console.error(error);
            typingRow.remove();

            appendRow(
                "bot",
                `<span style="color:#dc3545;">Something went wrong. Please try again.</span>`,
                getTime()
            );
        }

        chatBody.scrollTop = chatBody.scrollHeight;
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", function(e){
        if(e.key === "Enter") sendMessage();
    });

})();