// Variable to see current mode
var isWideMode = true;

// Listen click event of button 
document.getElementById("modeButton").addEventListener("click", function() {
    var iframe = document.getElementById("myIframe");
    var button = document.getElementById("modeButton");

    if (isWideMode) {
        // Switch to centered mode
        iframe.src = "https://inspo-chatbot-mobile-v1.streamlit.app/?embed=true"; // URL centered mode
        button.innerText = "Centered mode";
    } else {
        // Swith to wide mode
        iframe.src = "https://inspo-chatbot-v1.streamlit.app/?embed=true"; // URL wide mode
        button.innerText = "Wide mode";
    }

    // Switch mode
    isWideMode = !isWideMode;
});