// Load the monthly_sales.csv instead of JSON
fetch("output/monthly_sales.csv")
  .then((response) => response.text())
  .then((data) => {
    const rows = data
      .trim()
      .split("\n")
      .map((r) => r.split(","));
    const tbody = document.querySelector("#monthly-sales tbody");

    // Skip header row and populate table
    for (let i = 1; i < rows.length; i++) {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${rows[i][0]}</td><td>$${parseFloat(
        rows[i][1]
      ).toFixed(2)}</td>`;
      tbody.appendChild(row);
    }
  })
  .catch((error) => {
    console.error("Failed to load CSV data:", error);
  });
