async function fetchPrediction() {
  const date = document.getElementById("date").value;
  const time = document.getElementById("time").value;

  if (!date || !time) {
    alert("Please select both date and time.");
    return;
  }

  const apiUrl = "https://predicting-planes-over-india-6.onrender.com/predict";

  try {
    document.getElementById("prediction-result").innerHTML = "⏳ Loading...";

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date, time }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const data = await response.json();

    document.getElementById("prediction-result").innerHTML = `
      ✅ Predicted Flight Count: <b>${data.predicted_flight_count}</b><br/>
    `;
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("prediction-result").innerHTML = `❌ Error: ${error.message}`;
  }
}
