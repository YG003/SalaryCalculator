// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
  // Get the calculate button
  const calculateBtn = document.getElementById("calculateBtn");

  // Add event listener to the calculate button
  calculateBtn.addEventListener("click", async (e) => {
    e.preventDefault(); // Prevent form default behavior

    // Collect form data
    const data = {
      hours_per_week: parseFloat(document.getElementById("NumberofHours").value) || 0,
      hourly_rate: parseFloat(document.getElementById("HourlyRate").value) || 0,
      overtime_hours: parseFloat(document.getElementById("OvertimeHours").value) || 0,
      overtime_rate: parseFloat(document.getElementById("OvertimeRate").value) || 1,
      tax_code: document.getElementById("TaxCode").value || "1257L",
      national_insurance: parseFloat(document.getElementById("NationalInsurance").value) || 0,
      pension_percent: parseFloat(document.getElementById("PensionContributions").value) || 0,
      student_loan_plan: document.getElementById("StudentLoan").value,
    };

    try {
      // Send data to the backend
      const response = await fetch("http://127.0.0.1:5000/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      // Check for successful response
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      // Parse JSON response
      const result = await response.json();

      // Display results
      displayResults(result);
    } catch (error) {
      console.error("Error during calculation:", error);
      alert("An error occurred while calculating your salary. Please try again.");
    }
  });

  // Function to display results on the page
  function displayResults(data) {
    // Find or create the result div
    let resultDiv = document.getElementById("result");
    if (!resultDiv) {
      resultDiv = document.createElement("div");
      resultDiv.id = "result";
      resultDiv.style.marginTop = "20px";
      document.getElementById("SalaryCalculatorForm").appendChild(resultDiv);
    }

    // Populate the result div with the salary breakdown
    resultDiv.innerHTML = `
      <h2>Salary Breakdown</h2>
      <p><strong>Gross Salary:</strong> £${data.gross_salary.toFixed(2)}</p>
      <p><strong>Tax Deduction:</strong> £${data.tax_deduction.toFixed(2)}</p>
      <p><strong>National Insurance Deduction:</strong> £${data.ni_deduction.toFixed(2)}</p>
      <p><strong>Pension Deduction:</strong> £${data.pension_deduction.toFixed(2)}</p>
      <p><strong>Student Loan Deduction:</strong> £${data.student_loan_deduction.toFixed(2)}</p>
      <hr>
      <p><strong>Take-Home Salary:</strong> £${data.net_salary.toFixed(2)}</p>
    `;
  }
});
