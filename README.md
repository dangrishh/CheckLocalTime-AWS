# CheckLocalTime-AWS

Here’s a concise and accurate description for your third Lambda function:

---

### 🕒 Lambda Function: Business Cutoff Time Checker (GMT+10)

This AWS Lambda function checks whether the **current time in GMT+10** (e.g., Sydney/Melbourne timezone) is **past a defined business cutoff time**. It's useful for time-based logic in contact flows, automation rules, or routing decisions.

---

### ✅ Functionality:

1. **`get_current_date_gmt_plus_10()`**
   Returns today’s date in **GMT+10** timezone.

2. **`business_closing_time()`**
   Compares the current GMT+10 time to the configured **cutoff time** (from environment variable `BUSINESS_CUTOFF_TIME`, e.g., `"16:30"`).
   Returns `True` if current time is after cutoff.

3. **`lambda_handler()`**
   Combines both functions and returns:

   ```json
   {
     "date": "YYYY-MM-DD",
     "BusinessClosingTime": true/false
   }
   ```

---

### 🌐 Environment Variable Required:

* `BUSINESS_CUTOFF_TIME` – in `"HH:MM"` 24-hour format (e.g., `"16:30"` for 4:30 PM)

---

### 🛠️ Example Use Case:

This function is ideal for:

* Determining if customer contact happens **after business hours**
* Conditional routing in **Amazon Connect Contact Flows**
* Automating end-of-day processing

---

