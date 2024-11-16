$(document).ready(function () {


    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },


    });
});

// Siri configuration
// Function to initialize SiriWave with responsive dimensions
function initializeSiriWave() {
    // Get the container's dimensions
    const container = document.getElementById("siri-container");
    
    // Set width and height relative to the viewport size
    const width = Math.min(window.innerWidth * 0.9, 800); // 90% of the screen width, max 800px
    const height = Math.min(window.innerHeight * 0.2, 200); // 20% of the screen height, max 200px

    // Clear previous wave if any
    container.innerHTML = "";

    // Initialize the SiriWave
    new SiriWave({
        container: container,
        width: width,
        height: height,
        style: "ios9",
        amplitude: 1,
        speed: 0.3,
        autostart: true
    });
}

// Initialize on page load
initializeSiriWave();

// Reinitialize on window resize for responsiveness
window.addEventListener("resize", initializeSiriWave);

// Siri message animation
$('.siri-message').textillate({
    loop: true,
    sync: true,
    in: {
        effect: "fadeInUp",
        sync: true,
    },
    out: {
        effect: "fadeOutUp",
        sync: true,
    },

});

// mic button click event

$("#MicBtn").click(function () { 
    eel.playAssistantSound()
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    
});
