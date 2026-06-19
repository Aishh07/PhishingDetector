document.addEventListener("DOMContentLoaded", async () => {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    document.getElementById("url").innerText = tab.url;

    document.getElementById("checkBtn").addEventListener("click", async () => {

        const resultDiv = document.getElementById("result");

        resultDiv.innerHTML = `
        <div class="scan-wrapper">
            <div class="shield-container">
                <div class="shield">🛡️</div>
                <div class="radar-ring"></div>
                <div class="radar-ring delay"></div>
            </div>
            <div class="scan-line"></div>
            <div class="ai-engine">
                AI Security Engine Active
            </div>
            <div class="status-text" id="scanStatus">
                Initializing Scan...
            </div>
        </div>
        `;

        const messages = [
            "Extracting URL Features...",
            "Analyzing Domain Structure...",
            "Running ML Model...",
            "Calculating Threat Score...",
            "Generating Prediction..."
        ];

        let index = 0;
        const statusInterval = setInterval(() => {
            const status = document.getElementById("scanStatus");
            if (status) {
                status.innerText = messages[index % messages.length];
            }
            index++;
        }, 700);

        try {

            const response = await fetch(
                "https://phishingdetector-fe2z.onrender.com/predict",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ url: tab.url })
                }
            );

            const data = await response.json();
            clearInterval(statusInterval);

            // ── Fix 1: data.prediction is 0 or 1 (number) ──────
            const isPhishing  = data.prediction === 1;

            // ── Fix 2: confidence is 0.0-1.0, convert to % ─────
            const confPercent = Math.round(data.confidence * 100);

            const color   = isPhishing ? "#ef4444" : "#22c55e";
            const icon    = isPhishing ? "🚨"      : "🟢";
            const cssClass = isPhishing ? "phishing" : "safe";
            const label   = isPhishing ? "PHISHING" : "SAFE";
            const riskMsg = isPhishing
                ? `Risk Level: <b style="color:#ef4444;">${data.risk.toUpperCase()}</b>`
                : `Risk Level: <b style="color:#22c55e;">LOW</b>`;

            resultDiv.innerHTML = `
            <div style="text-align:center;">

                <h3 class="${cssClass}">
                    ${icon} ${label}
                </h3>

                <p style="margin-top:10px;">
                    Confidence: <b>${confPercent}%</b>
                </p>

                <div class="progress">
                    <div
                        class="progress-fill"
                        style="
                            width: ${confPercent}%;
                            background: ${color};
                        ">
                    </div>
                </div>

                <p style="margin-top:8px; font-size:13px;">
                    ${riskMsg}
                </p>

            </div>
            `;

        } catch (error) {

            clearInterval(statusInterval);

            resultDiv.innerHTML = `
            <div style="text-align:center;">
                <h3 style="color:#ef4444;">
                    ❌ API Error
                </h3>
                <p>Unable to connect to server</p>
                <p style="font-size:11px; color:#888;">
                    Check internet or try again
                </p>
            </div>
            `;

            console.error("API Error:", error);
        }

    });

});