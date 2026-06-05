(function(){

    const currentScript=document.currentScript;

    const baseUrl=new URL(
        currentScript.src
    ).origin;

    const css=document.createElement("link");

    css.rel="stylesheet";

    css.href=baseUrl+"/static/widget/widget.css";

document.head.appendChild(css);
    const widget=`

        <div id="botforge-widget-btn">
            💬
        </div>

        <div id="botforge-chat-window">

            <div id="botforge-chat-header">
                BotForge Assistant
            </div>

            <div id="botforge-chat-body">

                <div>
                    Hello! How can I help you today?
                </div>

            </div>

            <div id="botforge-chat-footer">

                <input
                    type="text"
                    placeholder="Type message..."
                >

                <button>
                    Send
                </button>

            </div>

        </div>

    `;

    document.body.insertAdjacentHTML(
        "beforeend",
        widget
    );

    const btn=document.getElementById(
        "botforge-widget-btn"
    );

    const windowBox=document.getElementById(
        "botforge-chat-window"
    );

    btn.addEventListener(
        "click",
        function(){

            if(
                windowBox.style.display==="block"
            ){

                windowBox.style.display="none";

            }else{

                windowBox.style.display="block";

            }

        }
    );

})();