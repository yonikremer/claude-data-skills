---
name: postgresql
description: Interact with PostgreSQL databases. Use for querying, managing tables, and understanding database structure. Requires environment variables for connection.
---

# PostgreSQL Database Interaction

This skill provides guidance and best practices for interacting with PostgreSQL databases.

## Setup and Connection

To connect to a PostgreSQL database instance, the following environment variables **MUST** be set before the Gemini CLI is started:

*   `POSTGRES_HOST`: The hostname or IP address of the PostgreSQL server.
*   `POSTGRES_PORT`: The port number of the PostgreSQL server.
*   `POSTGRES_DATABASE`: The name of the database to connect to.
*   `POSTGRES_USER`: The username for authentication.
*   `POSTGRES_PASSWORD`: The password for authentication.

### Handling Missing Environment Variables

If a command fails due to a missing environment variable, you **MUST** inform the user which variable is missing and instruct them to set it. For example: "The `POSTGRES_HOST` environment variable is not set. Please set it to the hostname or IP of your PostgreSQL server."

### Handling Permission Errors

If an operation fails due to insufficient permissions, it is likely that the user does not have the correct privileges on the PostgreSQL database. Inform the user about the permission issue.

## Usage Guidelines

### Reusing Project Values

When database connection details are required, **DO NOT** prompt the user for environment variable names directly (e.g., `POSTGRES_HOST`). Instead, prompt the user to verify and reuse the *value* of the environment variable. You can retrieve the value using a shell command like `echo $POSTGRES_HOST`.

### Full Table Name Format

**ALWAYS** use the full table name format: `DATABASE_NAME.SCHEMA_NAME.TABLE_NAME` when generating SQL queries or interacting with tables.

-   **Default Schema:** Always default to using "public" for the schema name unless explicitly specified otherwise by the user.
-   **Current Database Name:** To get the current database name, use the command `echo $POSTGRES_DATABASE`.

## Querying Data

To query data, you would typically use a tool that executes SQL commands (e.g., `execute_sql` or `postgres__execute_sql`).

**Example SQL Query Structure:**

```sql
SELECT
    column1,
    column2
FROM
    "your_database_name"."public"."your_table_name"
WHERE
    condition;
```

**Note:** Always ensure that table and column names are properly quoted if they contain special characters or are case-sensitive. The `DATABASE_NAME` should also be quoted.
