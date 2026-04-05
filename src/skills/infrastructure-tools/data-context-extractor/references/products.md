# Example: Products Data Structure

This document provides examples of the data structures and schemas used in the `products` domain.

## Schema: `dim_products`

| Column         | Type    | Description                                         |
|:---------------|:--------|:----------------------------------------------------|
| `product_id`   | STRING  | Unique identifier for each product.                 |
| `product_name` | STRING  | Display name of the product.                        |
| `category`     | STRING  | Product category: `ELECTRONICS`, `APPAREL`, `HOME`. |
| `unit_price`   | NUMERIC | Standard retail price.                              |
| `is_active`    | BOOLEAN | If the product is currently for sale.               |

## Common Metrics

### Category Distribution

Count of products in each category.

```sql
SELECT category, COUNT(*) FROM dim_products GROUP BY 1
```

### Price Statistics

Summary stats for prices across categories.

```sql
SELECT category, AVG(unit_price), MAX(unit_price) FROM dim_products GROUP BY 1
```
