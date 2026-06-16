document.addEventListener("DOMContentLoaded", async () => {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    document.getElementById("url").innerText = tab.url;

    document.getElementById("checkBtn").addEventListener("click", async () => {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        url: tab.url
                    })
                }
            );

            const data = await response.json();

            let color = "green";
let icon = "🟢";

if (data.prediction === "PHISHING") {
    color = "red";
    icon = "🔴";
}

document.getElementById("result").innerHTML =
`
<h3 style="color:${color}">
    ${icon} ${data.prediction}
</h3>

<p>
    Confidence: ${data.confidence}%
</p>
`;

        }
        catch(error) {

            document.getElementById("result").innerHTML =
                "API Error";

            console.log(error);
        }

    });

});