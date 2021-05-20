SELECT
    REPLACE (
        REPLACE (
            'SELECT ''{table}.{col}'' as col, 
                COUNT(t.{col}) as count_total, 
                COUNT(DISTINCT t.{col}) as count_distinct,
                CASE WHEN COUNT(t.{col}) = 0
                    THEN 0
                    ELSE COUNT(DISTINCT t.{col}) / COUNT(t.{col}) * 100
                    END
                AS percent_match,
                ''{col}'' as ''(helper)col''
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
    AND cols.data_type NOT IN ( 'datetime', 'timestamp', 'money', 'text', 'lontext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cols.table_schema ASC;