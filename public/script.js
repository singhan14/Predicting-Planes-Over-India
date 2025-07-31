document.getElementById("predictForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const date = document.getElementById("dateInput").value;
  const time = document.getElementById("timeInput").value;

  const response = await fetch("https://predicting-planes-over-india-6.onrender.com", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ date, time })
  });

  const data = await response.json();
  document.getElementById("results").hidden = false;
  document.getElementById("count").textContent = data.predicted_count;

  // Chart.js - example 24 hour prediction dummy chart
  const timeline = data.timeline || Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    count: Math.round(Math.random() * 100)  // replace with actual timeline data if available
  }));

  const ctx = document.getElementById("timelineChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: timeline.map(d => `${d.hour}:00`),
      datasets: [{
        label: "Flight Count",
        data: timeline.map(d => d.count),
        borderColor: "blue",
        tension: 0.3,
        fill: false
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  });
});
