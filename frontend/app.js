const API_URL = "https://ai-3rdpartyriskcopilot.onrender.com";

async function generateAssessment() {

    const vendorName =
        document.getElementById("vendorName").value;

    const payload = {
        vendorName: vendorName,
        businessCritical:
            document.getElementById("critical").value === "Yes",

        pii:
            document.getElementById("pii").value === "Yes",

        paymentData:
            document.getElementById("payment").value === "Yes",

        systemAccess:
            document.getElementById("access").value === "Yes",

        cloudHosted:
            document.getElementById("cloud").value === "Yes"
    };

    try {

        const response = await fetch(
            `${API_URL}/analyze-risk`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const result = await response.json();

        let cssClass = "low";

        if (result.risk_rating === "Medium")
            cssClass = "medium";

        if (result.risk_rating === "High")
            cssClass = "high";

        if (result.risk_rating === "Critical")
            cssClass = "critical";

        document.getElementById("riskSummary").innerHTML =
        `
        <div class="risk-box ${cssClass}">
            Risk Score:
            ${result.risk_score}/100
            |
            ${result.risk_rating}
        </div>
        `;

        document.getElementById("assessmentResult").innerText =
`
Vendor: ${result.vendor}

Risk Rating: ${result.risk_rating}

Risk Score: ${result.risk_score}

Recommendation:
${result.recommendation}
`;

    } catch (error) {

        document.getElementById(
            "assessmentResult"
        ).innerText =
        "Unable to connect to API.";
    }
}
