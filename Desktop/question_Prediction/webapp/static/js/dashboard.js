/* ---------------- Section Switch ---------------- */
function showSection(id) {
    document.querySelectorAll("section")
        .forEach(s => s.classList.add("hidden"));

    document.getElementById(id)
        .classList.remove("hidden");
}


/* ---------------- Prediction Simulation ---------------- */
document.getElementById("simulateBtn").onclick = async () => {
    const btn = document.getElementById("simulateBtn");

    btn.innerText = "Running ML Models...";
    btn.disabled = true;

    try {
        const res = await fetch("/api/predict");
        const data = await res.json();

        btn.innerText = data.status || "Predictions Updated";
    } catch (err) {
        btn.innerText = "Error Running Model";
    }

    btn.disabled = false;

    // Reload table after prediction
    loadPredictions();
};


/* ---------------- Difficulty Trend Chart ---------------- */
async function loadChart() {
    const res = await fetch("/api/chart-data");
    const data = await res.json();

    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart(document.getElementById("trendChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Questions per Subject",
                data: values
            }]
        }
    });
}

loadChart();



/* ---------------- Load Predictions Table ---------------- */
async function loadPredictions() {
    try {
        const res = await fetch("/api/predictions");
        const data = await res.json();

        const tbody = document.getElementById("predictionTable");
        tbody.innerHTML = "";

        data.forEach(r => {
            tbody.innerHTML += `
            <tr class="border-b border-gray-700">
                <td class="p-2">${r.Subject || ""}</td>
                <td class="p-2">${r.Topic || ""}</td>
                <td class="p-2">${r.Predicted_Probability || ""}</td>
            </tr>`;
        });

    } catch (err) {
        console.log("Prediction load error:", err);
    }
}

// Load on start
loadPredictions();


/* ---------------- Rank Booster Cards ---------------- */
const chapters = [
    ["Electrostatics", 90],
    ["Calculus", 85],
    ["Organic Chemistry", 80]
];

const container = document.getElementById("rankCards");

if (container) {
    chapters.forEach(([name, val]) => {
        container.innerHTML += `
        <div class="bg-slate-900 p-4 rounded shadow">
            <h3 class="mb-2 font-semibold">${name}</h3>

            <div class="bg-gray-700 h-3 rounded">
                <div class="bg-green-500 h-3 rounded"
                     style="width:${val}%"></div>
            </div>

            <p class="text-sm mt-2 text-gray-400">
                High Yield Probability
            </p>
        </div>`;
    });
}
