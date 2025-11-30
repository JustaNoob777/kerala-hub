// ===============================
// GLOBAL SEARCH SCRIPT (SAFE)
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("service-search");
    const suggestions = document.getElementById("suggestions");
    const searchBtn = document.getElementById("search-btn");
    const resultsGrid = document.getElementById("results-grid");
    const resultsCount = document.getElementById("results-count");

    // If search is not present on page, stop script
    if (!input || !suggestions || !searchBtn) return;

    // Force container alignment for dropdown
    const wrapper = input.closest(".search-wrapper");
    if (wrapper) wrapper.style.position = "relative";

    // ------------------------------------------
    // MAIN SEARCH REQUEST (for full search page)
    // ------------------------------------------
    async function performSearch() {
        const query = input.value.trim();
        if (!query) return;

        try {
            const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
            const results = await response.json();

            if (resultsGrid) {
                resultsGrid.innerHTML = "";
            }

            if (resultsCount) {
                resultsCount.textContent = `${results.length} results found`;
            }

            results.forEach(item => {
                if (!resultsGrid) return;

                const card = document.createElement("div");
                card.className = "card";
                
                card.innerHTML = `
                    <div class="card-icon">${item.icon || "📘"}</div>
                    <div class="card-title">${item.name}</div>
                `;

                card.onclick = () => {
                    window.location.href =
                        item.type === "service"
                        ? `/service/${item.id}/`
                        : `/office/${item.id}/`;
                };

                resultsGrid.appendChild(card);
            });

        } catch (err) {
            console.error("Search error:", err);
        }
    }

    // ------------------------------------------
    // Auto-suggestions
    // ------------------------------------------
    input.addEventListener("input", async () => {
        const q = input.value.trim();

        if (!q) {
            suggestions.style.display = "none";
            return;
        }

        try {
            const response = await fetch(`/search/?q=${encodeURIComponent(q)}`);
            const matches = await response.json();

            suggestions.innerHTML = "";

            matches.slice(0, 5).forEach(item => {
                const li = document.createElement("li");
                li.innerHTML = item.type === "service"
                    ? `📘 ${item.name}`
                    : `🏢 ${item.name}`;

                li.onclick = () => {
                    window.location.href =
                        item.type === "service"
                        ? `/service/${item.id}/`
                        : `/office/${item.id}/`;
                };

                suggestions.appendChild(li);
            });

            suggestions.style.display = matches.length ? "block" : "none";

        } catch (err) {
            console.error("Suggestion error:", err);
        }
    });

    // ------------------------------------------
    // Search button click
    // ------------------------------------------
    searchBtn.addEventListener("click", performSearch);

    // ------------------------------------------
    // Enter key triggers full search
    // ------------------------------------------
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            performSearch();
        }
    });

    // ------------------------------------------
    // Clicking outside hides suggestions
    // ------------------------------------------
    document.addEventListener("click", (e) => {
        if (!wrapper.contains(e.target)) {
            suggestions.style.display = "none";
        }
    });

});


// ==============================
// DARK MODE
// ==============================
document.addEventListener("DOMContentLoaded", function () {
    const themeBtn = document.getElementById("theme-toggle");
    const root = document.documentElement;

    // Apply previously saved theme
    const saved = localStorage.getItem("theme");

    if (saved === "dark") {
        root.classList.add("dark-mode");
        if (themeBtn) themeBtn.textContent = "☀️";
    } else {
        root.classList.remove("dark-mode");
        if (themeBtn) themeBtn.textContent = "🌙";
    }

    // Only attach toggle if button exists (homepage only)
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            root.classList.toggle("dark-mode");

            if (root.classList.contains("dark-mode")) {
                localStorage.setItem("theme", "dark");
                themeBtn.textContent = "☀️";
            } else {
                localStorage.setItem("theme", "light");
                themeBtn.textContent = "🌙";
            }
        });
    }
});