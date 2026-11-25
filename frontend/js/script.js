
// ==========================================
// ScamLens - Frontend Functionality
// ==========================================

// HTML Elements
const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".input-panel");

const messageInput = document.getElementById("message-input");
const urlInput = document.getElementById("url-input");
const imageInput = document.getElementById("image-input");

const charCount = document.getElementById("char-count");
const fileName = document.getElementById("file-name");

const analyzeBtn = document.getElementById("analyze-btn");
const statusMessage = document.getElementById("status-message");
const analysisResult = document.getElementById("analysis-result");

let currentMode = "text";


// ==========================================
// 1. Switch Between Analyzer Modes
// ==========================================

tabs.forEach(tab => {

    tab.addEventListener("click", () => {

        tabs.forEach(item => item.classList.remove("active"));
        panels.forEach(panel => panel.classList.remove("active"));

        tab.classList.add("active");

        currentMode = tab.dataset.mode;

        document.getElementById(`${currentMode}-panel`)
            .classList.add("active");

        statusMessage.classList.remove("show");
        analysisResult.hidden = true;

    });

});


// ==========================================
// 2. Character Counter
// ==========================================

messageInput.addEventListener("input", () => {

    charCount.textContent =
        `${messageInput.value.length} / 10000`;

});


// ==========================================
// 3. Image Upload Validation
// ==========================================

imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) return;

    const allowedTypes = ["image/jpeg", "image/png"];

    if (!allowedTypes.includes(file.type)) {

        showStatus("Please upload a JPG or PNG image.");

        imageInput.value = "";
        fileName.textContent = "";

        return;
    }

    if (file.size > 5 * 1024 * 1024) {

        showStatus("Image size must be less than 5 MB.");

        imageInput.value = "";
        fileName.textContent = "";

        return;
    }

    fileName.textContent = `Selected: ${file.name}`;

    statusMessage.classList.remove("show");

});


// ==========================================
// 4. Analyze Button
// ==========================================

analyzeBtn.addEventListener("click", async () => {

    statusMessage.classList.remove("show");
    analysisResult.hidden = true;

    // TEXT ANALYSIS
    if (currentMode === "text") {

        const message = messageInput.value.trim();

        if (!message) {
            showStatus("Please enter a message to analyze.");
            return;
        }

        if (message.length < 5) {
            showStatus("Please enter a longer message.");
            return;
        }

        await analyzeTextMessage(message);

    }

    // IMAGE VALIDATION
    else if (currentMode === "image") {

const file = imageInput.files[0];

    if (!file) {
        showStatus("Please upload a screenshot first.");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    analysisResult.hidden = false;
    analysisResult.textContent = "Extracting text from screenshot...";

    try {
        const result = await analyzeScreenshot(file);

        displayAnalysisResult(result);

    } catch (error) {
        console.error("Screenshot Analysis Error:", error);

        analysisResult.hidden = true;

        showStatus(
            error.message || "Unable to analyze screenshot."
        );

    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "<span>🔍</span> Analyze Now";
    }
    }

    // URL VALIDATION
    else if (currentMode === "url") {
        

        const url = urlInput.value.trim();

    if (!url) {
        showStatus("Please enter a URL to analyze.");
        return;
    }

    try {
        const parsedURL = new URL(
            /^[a-z][a-z0-9+.-]*:\/\//i.test(url)
                ? url
                : `https://${url}`
        );

        if (!["http:", "https:"].includes(parsedURL.protocol) ||
            !parsedURL.hostname ||
            !parsedURL.hostname.includes(".")) {
            throw new Error("Invalid URL");
        }

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";

        analysisResult.hidden = false;
        analysisResult.textContent = "Analyzing URL...";

        const result = await analyzeURL(url);
        displayAnalysisResult(result);

    } catch (error) {
        console.error("URL Analysis Error:", error);

        analysisResult.hidden = true;
        showStatus(
            error.message || "Unable to analyze this URL."
        );

    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "<span>🔍</span> Analyze Now";
    }

    }

});


// ==========================================
// 5. Connect Frontend to Backend
// ==========================================

async function analyzeTextMessage(message) {

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    analysisResult.hidden = false;
    analysisResult.textContent = "Analyzing your message...";

    try {

        // Send message to FastAPI backend
        const result = await analyzeMessage(message);

        // Display backend response
        displayAnalysisResult(result);

    } catch (error) {

        console.error("Analysis Error:", error);

        analysisResult.textContent =
            "Unable to analyze the message. Please check whether the backend is running.";

    } finally {

        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = "<span>🔍</span> Analyze Now";

    }

}


// ==========================================
// 6. Display Analysis Results
// ==========================================

function displayAnalysisResult(result) {

    analysisResult.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = "ScamLens Analysis Results";

    const risk = document.createElement("p");

    risk.textContent =
        `Risk Level: ${result.risk_level} (${result.risk_score}/100)`;

// ==========================================
// AI/ML Analysis Display
// ==========================================

let mlSection = null;

if (
    result.ml_prediction &&
    result.ml_spam_probability !== undefined
) {
    const probability = Math.max(
        0,
        Math.min(100, Number(result.ml_spam_probability))
    );

    mlSection = document.createElement("div");
    mlSection.className = "ml-analysis";

    mlSection.style.cssText = `
        margin: 20px 0;
        padding: 18px;
        border: 1px solid #64748b;
        border-radius: 12px;
        background: rgba(100, 116, 139, 0.08);
    `;

    const mlHeading = document.createElement("h4");
    mlHeading.textContent = "🤖 AI/ML Analysis";

    const prediction = document.createElement("p");

    const predictionLabel = document.createElement("strong");
    predictionLabel.textContent = "ML Prediction: ";

    const predictionValue = document.createElement("span");
    predictionValue.textContent =
        result.ml_prediction.toUpperCase();

    predictionValue.style.cssText = `
        font-weight: bold;
        color: ${result.ml_prediction === "spam" ? "#dc2626" : "#16a34a"};
    `;

    prediction.append(predictionLabel, predictionValue);

    const probabilityText = document.createElement("p");
    probabilityText.textContent =
        `Spam Probability: ${probability.toFixed(2)}%`;

    const progressBar = document.createElement("div");

    progressBar.style.cssText = `
        width: 100%;
        height: 12px;
        background: #d1d5db;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 10px;
    `;

    const progress = document.createElement("div");

    progress.style.cssText = `
        width: ${probability}%;
        height: 100%;
        background: #dc5555;
        border-radius: 10px;
        transition: width 0.4s ease;
    `;

    progressBar.appendChild(progress);

    const note = document.createElement("small");
    note.textContent =
        "Prediction generated by the trained ScamLens Machine Learning model.";

    mlSection.append(
        mlHeading,
        prediction,
        probabilityText,
        progressBar,
        note
    );
}

    const indicatorsHeading = document.createElement("h4");
    indicatorsHeading.textContent = "Detected Indicators";

    const indicatorsList = document.createElement("ul");

    result.detected_indicators.forEach(item => {

        const li = document.createElement("li");

        li.textContent =
            `${item.keyword}: ${item.reason}`;

        indicatorsList.appendChild(li);

    });

    if (result.detected_indicators.length === 0) {

        const li = document.createElement("li");

        li.textContent = "No suspicious indicators detected.";

        indicatorsList.appendChild(li);

    }

    const recommendationsHeading = document.createElement("h4");
    recommendationsHeading.textContent = "Safety Recommendations";

    const recommendationsList = document.createElement("ul");

    result.recommendations.forEach(item => {

        const li = document.createElement("li");

        li.textContent = item;

        recommendationsList.appendChild(li);

    });

    if (result.extracted_text) {
    const extractedHeading = document.createElement("h4");
    extractedHeading.textContent = "Extracted Text";

    const extractedContent = document.createElement("p");
    extractedContent.textContent = result.extracted_text;

    analysisResult.append(
        extractedHeading,
        extractedContent
    );
}

    analysisResult.append(
    heading,
    risk
);

// Display ML results when available
if (mlSection) {
    analysisResult.appendChild(mlSection);
}

analysisResult.append(
    indicatorsHeading,
    indicatorsList,
    recommendationsHeading,
    recommendationsList
);

}


// ==========================================
// 7. Display Status Messages
// ==========================================

function showStatus(message) {

    statusMessage.textContent = message;

    statusMessage.classList.add("show");

}
