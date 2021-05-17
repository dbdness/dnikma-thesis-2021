SELECT
    REPLACE (
        REPLACE (
            'SELECT ''{table}.{col}'' as col, 
                COUNT(t.{col}) as count_total, 
                COUNT(DISTINCT t.{col}) as count_distinct, 
                (COUNT(DISTINCT t.{col}) / COUNT(t.{col})) * 100 as percent_match 
            FROM {table} t UNION ALL',
        '{table}',
        cols.table_name
        ),
    '{col}',
    cols.column_name
    )
FROM
    information_schema.COLUMNS cols
WHERE
    cols.table_schema = DATABASE()
    AND cols.is_nullable = 'YES'
    AND cols.data_type NOT IN ( 'datetime', 'timestamp', 'money', 'text', 'lontext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cols.table_schema ASC;