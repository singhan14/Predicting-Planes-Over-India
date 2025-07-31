async function fetchPrediction() {
  const date = document.getElementById("date").value;
  const time = document.getElementById("time").value;
  const resultBox = document.getElementById("prediction-result");

  if (!date || !time) {
    alert("⚠️ Please select both a date and a time.");
    return;
  }

  const apiUrl = `https://predicting-planes-over-india-6.onrender.com/predict?date=${date}&time=${time}`;

  try {
    resultBox.style.color = "black";
    resultBox.innerHTML = "⏳ Fetching prediction...";

    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    // Basic validation of expected fields
    if (!data.flight_count || !data.traffic_density) {
      throw new Error("Incomplete data from server");
    }

    resultBox.style.color = "green";
    resultBox.innerHTML = `
      ✅ <b>Predicted Flight Count:</b> ${data.flight_count}<br/>
      🛰️ <b>Traffic Density:</b> ${data.traffic_density}<br/>
    `;
  } catch (error) {
    console.error("❌ Error fetching prediction:", error);
    resultBox.style.color = "red";
    resultBox.innerHTML = `❌ Error: ${error.message}`;
  }
}
