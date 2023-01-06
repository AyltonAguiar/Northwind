locals {
  # Grupos e usuários individual, respectivamente
  groups = {"bi_users":1, "dbt_users":2, "loaders_users":3}
  users_groups = {"dbt_prod":1, "dbt_dev":2,"looker":3,"airbyte":4}

  # Usuários por grupo (users:group)
  groups_category ={
    "looker":"bi_users",
    "dbt_prod": "dbt_users",
    "dbt_dev": "dbt_users",
    "airbyte":"loaders_users"
    }

}

