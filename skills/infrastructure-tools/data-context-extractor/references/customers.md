# Example: Customers Data Structure

This document provides examples of the data structures and schemas used in the `customers` domain.

## Schema: `dim_customers`

| Column | Type | Description |
| :--- | :--- | :--- |
| `customer_id` | STRING | Unique identifier for each customer. |
| `first_name` | STRING | Customer first name. |
| `last_name` | STRING | Customer last name. |
| `email` | STRING | Primary contact email address. |
| `signup_date` | DATE | Date the customer created their account. |
| `tier` | STRING | Customer loyalty tier: `FREE`, `SILVER`, `GOLD`. |

## Common Queries

### Active Customers
Customers who have placed at least one order in the last 30 days.
```sql
SELECT DISTINCT c.customer_id
FROM dim_customers c
JOIN fact_orders o ON c.customer_id = o.customer_id
WHERE o.order_timestamp > CURRENT_DATE - INTERVAL '30 days'
```
