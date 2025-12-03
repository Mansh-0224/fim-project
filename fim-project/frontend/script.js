// script.js - Frontend logic and API calls

const API_BASE = "http://localhost:5000/api";

/**
 * Initialize Baseline - Send folder path to backend
 */
async function initializeBaseline() {
    const folderPath = document.getElementById("folderPathInit").value.trim();
    const statusDiv = document.getElementById("initStatus");

    // Validate input
    if (!folderPath) {
        showStatus(statusDiv, "Please enter a folder path", "error");
        return;
    }

    // Show loading state
    showStatus(statusDiv, "Initializing baseline...", "loading");

    try {
        const response = await fetch(`${API_BASE}/init-baseline`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ folder: folderPath })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            showStatus(
                statusDiv,
                `✅ ${data.message} Scanned ${data.files_scanned} files.`,
                "success"
            );
            // Pre-fill the check folder path with same path
            document.getElementById("folderPathCheck").value = folderPath;
        } else {
            showStatus(
                statusDiv,
                `❌ ${data.message || "Failed to initialize baseline"}`,
                "error"
            );
        }
    } catch (error) {
        showStatus(statusDiv, `❌ Error: ${error.message}`, "error");
        console.error("Initialize Baseline Error:", error);
    }
}

/**
 * Check Integrity - Compare current state with baseline
 */
async function checkIntegrity() {
    const folderPath = document.getElementById("folderPathCheck").value.trim();
    const statusDiv = document.getElementById("checkStatus");
    const resultsContainer = document.getElementById("resultsContainer");

    // Validate input
    if (!folderPath) {
        showStatus(statusDiv, "Please enter a folder path", "error");
        return;
    }

    // Show loading state
    showStatus(statusDiv, "Checking integrity...", "loading");

    try {
        const response = await fetch(`${API_BASE}/check`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ folder: folderPath })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            showStatus(statusDiv, `✅ Scan completed at ${formatTime(data.timestamp)}`, "success");
            displayResults(data, resultsContainer);
        } else {
            showStatus(
                statusDiv,
                `❌ ${data.message || "Failed to check integrity"}`,
                "error"
            );
            resultsContainer.classList.add("hidden");
        }
    } catch (error) {
        showStatus(statusDiv, `❌ Error: ${error.message}`, "error");
        resultsContainer.classList.add("hidden");
        console.error("Check Integrity Error:", error);
    }
}

/**
 * Display results in the UI
 */
function displayResults(data, container) {
    // Update summary stats
    document.getElementById("totalFiles").textContent = data.total_files;
    document.getElementById("unchangedCount").textContent = data.unchanged_count;
    document.getElementById("modifiedCount").textContent = data.modified.length;
    document.getElementById("addedCount").textContent = data.added.length;
    document.getElementById("deletedCount").textContent = data.deleted.length;

    // Populate modified files list
    const modifiedList = document.getElementById("modifiedList");
    if (data.modified.length > 0) {
        modifiedList.innerHTML = data.modified
            .map(file => `<li>⚠️ ${escapeHtml(file)}</li>`)
            .join("");
    } else {
        modifiedList.innerHTML = '<li class="empty-message">No modified files</li>';
    }

    // Populate added files list
    const addedList = document.getElementById("addedList");
    if (data.added.length > 0) {
        addedList.innerHTML = data.added
            .map(file => `<li>➕ ${escapeHtml(file)}</li>`)
            .join("");
    } else {
        addedList.innerHTML = '<li class="empty-message">No new files</li>';
    }

    // Populate deleted files list
    const deletedList = document.getElementById("deletedList");
    if (data.deleted.length > 0) {
        deletedList.innerHTML = data.deleted
            .map(file => `<li>➖ ${escapeHtml(file)}</li>`)
            .join("");
    } else {
        deletedList.innerHTML = '<li class="empty-message">No deleted files</li>';
    }

    // Show results container
    container.classList.remove("hidden");
}

/**
 * Show status message in UI
 */
function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status-message ${type}`;

    // Auto-clear success messages after 5 seconds
    if (type === "success") {
        setTimeout(() => {
            element.textContent = "";
            element.className = "status-message";
        }, 5000);
    }
}

/**
 * Escape HTML to prevent injection
 */
function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Format ISO timestamp to readable time
 */
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString();
}

/**
 * On page load - check backend connection
 */
document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        if (data.status === "ok") {
            console.log("✅ Backend connected successfully!");
        }
    } catch (error) {
        console.warn("⚠️ Backend not reachable at " + API_BASE);
        console.warn("Make sure to start the Flask server: python app.py");
    }
});

/**
 * Allow pressing Enter in input fields to trigger buttons
 */
document.getElementById("folderPathInit")?.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        initializeBaseline();
    }
});

document.getElementById("folderPathCheck")?.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        checkIntegrity();
    }
});
