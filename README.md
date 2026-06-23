# Transaction Ranking System

A simple full-stack application built for a backend engineering assignment.
It provides transaction processing, user summaries, and a ranking system while demonstrating API design, validation, duplicate prevention, consistent updates, and basic fairness logic.

---

## Features

* Add **credit/debit transactions** for a user
* Prevent **duplicate transaction processing** using an **idempotency key**
* View **user transaction summary**
* View **ranking leaderboard**
* Validate bad input and handle invalid requests gracefully
* Prevent **debit transactions** when balance is insufficient
* Use a **multi-factor ranking formula** instead of ranking only by total amount
* Basic fairness improvement by capping the transaction-count contribution in ranking

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

### Frontend

* HTML
* CSS
* JavaScript

---

## Project Structure

```bash
transaction-ranking-system/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── ranking.py
│   │   └── init_db.py
│   │
│   ├── requirements.txt
│   ├── transactions.db
│   └── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

## API Endpoints

### 1. POST `/transaction`

Creates a new transaction for a user.

#### Request Body

```json
{
  "user_id": "user1",
  "amount": 500,
  "type": "credit",
  "idempotency_key": "abc123"
}
```

#### Validation Rules

* `user_id` cannot be empty
* `idempotency_key` cannot be empty
* `amount` must be greater than 0
* `amount` cannot exceed 10000
* `type` must be either `"credit"` or `"debit"`

#### Behaviour

* If the `idempotency_key` already exists, the request is treated as a duplicate and is not processed again.
* Credit transactions increase the user balance.
* Debit transactions decrease the user balance only if sufficient balance exists.

---

### 2. GET `/summary/{user_id}`

Returns summary information for a user.

#### Example Response

```json
{
  "user_id": "user1",
  "total_amount": 500,
  "transaction_count": 2,
  "average_transaction": 450
}
```

#### Summary Fields

* `total_amount` → current balance / net amount after credits and debits
* `transaction_count` → number of successful transactions
* `average_transaction` → average transaction amount based on total transaction volume

---

### 3. GET `/ranking`

Returns ranked users based on a scoring formula.

#### Example Response

```json
[
  {
    "user_id": "user1",
    "score": 264,
    "rank": 1
  }
]
```

---

## Ranking Logic

The ranking is based on **more than one factor** to make it fairer than simply sorting by total amount.

### Current formula

```python
score = (total_amount * 0.5) + (min(transaction_count, 20) * 2) + recency_bonus
```

### Factors used

1. **Total amount (50%)**

   * Rewards users with higher net contribution / balance.

2. **Transaction count contribution**

   * Rewards consistent activity.
   * It is capped using `min(transaction_count, 20)` so users cannot easily manipulate ranking with too many tiny transactions.

3. **Recency bonus**

   * Users who have recent activity in the last 24 hours receive a small bonus.

---

## How duplicate requests are prevented

Duplicate transaction processing is prevented using an **idempotency key**.

### How it works

* Each transaction request must contain a unique `idempotency_key`.
* Before processing a transaction, the backend checks whether that key already exists in the `transactions` table.
* If it exists, the backend returns the existing transaction result instead of processing it again.

This ensures that repeated requests (whether accidental retries or abuse attempts) do not create duplicate transactions.

---

## Data Consistency / Safe Updates

When a transaction is processed:

1. The transaction is inserted into the `transactions` table
2. The user’s stats are updated in `user_stats`
3. Both updates are committed together

If an error occurs during processing, the transaction is rolled back.

This helps keep transaction data and summary data consistent.

---

## Database Schema

### `transactions`

Stores every transaction request that was successfully processed.

Fields:

* `id`
* `user_id`
* `amount`
* `type`
* `timestamp`
* `idempotency_key`

### `user_stats`

Stores summary data for each user.

Fields:

* `user_id`
* `total_amount`
* `total_transaction_volume`
* `transaction_count`
* `last_transaction_time`

---

## How to run the project

# 1) Clone the repository

```bash
git clone <your-repo-link>
cd transaction-ranking-system
```

# 2) Set up backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

Swagger docs:

```bash
http://127.0.0.1:8000/docs
```

# 3) Run frontend

Open the `frontend/index.html` file in a browser
or use VS Code Live Server.

---

## Assumptions / Limitations

* SQLite is used for simplicity in this assignment.
* For a production system, PostgreSQL would be better for stronger concurrency handling and row-level locking.
* The ranking formula is intentionally simple but multi-factor.
* Abuse prevention is basic and includes:

  * duplicate prevention via idempotency key
  * maximum transaction amount limit
  * capped transaction-count contribution in ranking
  * debit balance checks

---

## Possible Future Improvements

* Move from SQLite to PostgreSQL
* Add proper rate limiting
* Add authentication / authorization
* Add pagination for rankings
* Add transaction history endpoint
* Add tests with pytest
* Use Alembic migrations for schema changes

---

## Demo Flow

1. Add a transaction from the frontend
2. Check the user summary
3. Refresh the leaderboard
4. Try the same idempotency key again to see duplicate prevention
5. Try a large debit to see validation / insufficient balance handling
