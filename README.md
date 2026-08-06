# Platform Usage & Behavioral Insights

---

## Project Overview
This end-to-end data pipeline project transforms raw digital banking transaction logs and in-app activity data into structured Excel performance reports and an interactive executive dashboard. The objective is to evaluate transaction success/failure performance across payment channels, understand customer behavior on the app and net banking platforms, and identify peak usage windows for each user action.

## Data Pipeline & Architecture
The project follows a structured ETL (Extract, Transform, Load) pipeline:  
**CSV → MySQL → SQL Views → Python Data Cleaning → Excel → Tableau**

1. **Database Ingestion:** Ingested three core raw datasets into a MySQL database (`sql_analytics4`) using the Python `sqlalchemy` engine.
2. **SQL Auditing & Views:** Ran comprehensive data quality checks to identify missing channel types, invalid age groups/regions, malformed transaction amounts, and inconsistent timestamp formats, along with duplicate record checks. Created optimized SQL views (`v_transactions` and `v_app_activity`) for stream processing.
3. **Python Cleaning & Normalization:** Standardized text strings (age groups, regions, payment channels, transaction statuses), parsed monetary values by removing `Rs.` and `,` characters, handled missing values, and converted string timestamps to standard `datetime` objects using `pandas`. Merged transaction and activity data, backfilling missing channel types via a payment-channel mapping.
4. **Behavioral & Performance Analysis:** Built a peak-hour analysis engine in Python (grouping activity into Night/Morning/Afternoon/Evening windows) to determine when each action is most frequently performed, producing two core executive exports:
   * **Event Action Analysis Report:** Aggregates total actions by channel type and action performed, identifies each action's peak activity window, and calculates each action's share of total platform activity.
   * **Transaction Performance Report:** Evaluates passed versus failed transactions across channel and payment channel combinations to calculate settled volume, volume at risk, and overall success rate.
5. **Dashboard Visualization:** Connected the output reports into a Tableau dashboard to highlight KPI metric cards, channel success rates, and behavioral breakdowns.

---

## Project Deliverables & Visual Preview

### 1. Event Action Report
Evaluates in-app and net banking activity, tracking total actions performed per channel and the peak time window (Night, Morning, Afternoon, Evening) in which each action occurs. It calculates each action's share of overall platform activity.

<img width="815" height="286" alt="image" src="https://github.com/user-attachments/assets/80399dde-45ca-41ea-9d6d-8ce383ba3cec" />

### 2. Transaction Performance Report
Tracks passed versus failed transactions across channel type and payment channel to identify settled volume and volume at risk. It calculates a success rate for each channel/payment-channel combination.

<img width="1150" height="280" alt="image" src="https://github.com/user-attachments/assets/ac5dd1f2-fca1-43a1-905c-a41554bb2b2b" />

### 3. Live Tableau Executive Dashboard
An interactive dashboard displaying key behavioral metrics: **83.80%** Transaction Success rate, **₹5.27M** Settled Amount, **738** Unresolved Transactions, and **₹1.05M** Unresolved Amount. The dashboard features breakdown charts for Payment Channel Success Rate, People Actions distribution, Settled vs. Risky Volume by payment channel, and Peak Hour by Actions.

> 📄 [**Tableau Dashboard Direct Link**](https://public.tableau.com/views/PlatformUsageBehavioralInsights/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

<img width="1164" height="776" alt="Dashboard_cropped" src="https://github.com/user-attachments/assets/2d885163-b2f3-4b3f-a7ba-963b6376ee4c" />

---

## Repository Structure

* [`app_events.csv`](./app_events.csv)
* [`customers.csv`](./customers.csv)
* [`digital_transfers.csv`](./digital_transfers.csv)

---

* [`data_transfer4.py`](./data_transfer4.py)
 --> [`SQL_Analytics4.sql`](./SQL_Analytics4.sql)
 --> [`python_analytics4.py`](./python_analytics4.py)

---

* [`Event_Action_Analysis.xlsx`](./Event_Action.xlsx)
* [`Transaction_Performance.xlsx`](./Transaction_Performance.xlsx)

---

* [`Platform Usage & Behavioral Insights.twbx`](./Platform%20Usage%20%26%20Behavioral%20Insights.twbx)

---

## Technologies Used
* **Languages:** Python (`pandas`, `sqlalchemy`, `numpy`), SQL
* **Database:** MySQL
* **Reporting & Viz:** Excel, Tableau
* **Environment:** VS Code
