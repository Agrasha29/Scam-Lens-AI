
const API_BASE_URL = "http://127.0.0.1:8000";

async function analyzeMessage(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed.");
        }

        return data;

    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}


async function analyzeURL(url) {
    const response = await fetch(`${API_BASE_URL}/analyze-url`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "URL analysis failed.");
    }

    return data;
}



async function analyzeScreenshot(file) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_BASE_URL}/analyze-image`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Screenshot analysis failed."
        );
    }

    return data;
}

