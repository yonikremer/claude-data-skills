# Example: Orders Data Structure

This document provides examples of the data structures and schemas used in the `orders` domain.

## Schema: `fact_orders`

| Column | Type | Description |
| :--- | :--- | :--- |
| `order_id` | STRING | Unique identifier for each order. |
| `customer_id` | STRING | Reference to the customer who placed the order. |
| `order_timestamp` | TIMESTAMP | When the order was placed. |
| `total_amount` | NUMERIC | Total order value including tax and shipping. |
| `status` | STRING | Current status: `PENDING`, `SHIPPED`, `DELIVERED`, `CANCELLED`. |

## Metrics Definitions

### Gross Merchandise Value (GMV)
Total value of all orders placed, regardless of status.
```sql
SELECT SUM(total_amount) FROM fact_orders
```

### Net Merchandise Value (NMV)
Total value of orders that were not cancelled.
```sql
SELECT SUM(total_amount) FROM fact_orders WHERE status != 'CANCELLED'
```
