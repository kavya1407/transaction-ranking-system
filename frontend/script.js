const BASE_URL = "https://transaction-ranking-system-7szd.onrender.com";

// Add Transaction
document.getElementById("transactionForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const userId = document.getElementById("userId").value;
  const amount = parseFloat(document.getElementById("amount").value);
  const type = document.getElementById("type").value;
  const idempotencyKey = document.getElementById("idempotencyKey").value;

  const resultBox = document.getElementById("transactionResult");

  try {
    const response = await fetch(`${BASE_URL}/transaction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: userId,
        amount: amount,
        type: type,
        idempotency_key: idempotencyKey
      })
    });

    const data = await response.json();

    if (!response.ok) {
      resultBox.innerText = `Error: ${data.detail || "Something went wrong"}`;
      resultBox.style.color = "red";
      return;
    }

    resultBox.innerText = `${data.message} (Transaction ID: ${data.transaction_id})`;
    resultBox.style.color = "green";

    document.getElementById("transactionForm").reset();
    getRanking();
  } catch (error) {
    resultBox.innerText = "Error connecting to backend";
    resultBox.style.color = "red";
  }
});

// Get Summary
async function getSummary() {
  const userId = document.getElementById("summaryUserId").value;
  const summaryBox = document.getElementById("summaryResult");

  if (!userId) {
    summaryBox.innerHTML = "<p style='color:red;'>Please enter a user ID</p>";
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/summary/${userId}`);
    const data = await response.json();

    if (!response.ok) {
      summaryBox.innerHTML = `<p style="color:red;">${data.detail}</p>`;
      return;
    }

    summaryBox.innerHTML = `
      <p><strong>User ID:</strong> ${data.user_id}</p>
      <p><strong>Total Amount:</strong> ${data.total_amount}</p>
      <p><strong>Transaction Count:</strong> ${data.transaction_count}</p>
      <p><strong>Average Transaction:</strong> ${data.average_transaction}</p>
    `;
  } catch (error) {
    summaryBox.innerHTML = "<p style='color:red;'>Error connecting to backend</p>";
  }
}

// Get Ranking
async function getRanking() {
  const tableBody = document.querySelector("#rankingTable tbody");

  try {
    const response = await fetch(`${BASE_URL}/ranking`);
    const data = await response.json();

    tableBody.innerHTML = "";

    data.forEach((user) => {
      const row = `
        <tr>
          <td>${user.rank}</td>
          <td>${user.user_id}</td>
          <td>${user.score}</td>
        </tr>
      `;
      tableBody.innerHTML += row;
    });
  } catch (error) {
    tableBody.innerHTML = `<tr><td colspan="3">Error loading ranking</td></tr>`;
  }
}

// Load ranking on page load
getRanking();