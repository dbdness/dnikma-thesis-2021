SELECT
    REPLACE (
        REPLACE (
            'SELECT ''{table}.{col}'' as col, 
                COUNT(t.`{col}`) as count_total, 
                COUNT(DISTINCT t.`{col}`) as count_distinct, 
                CASE WHEN COUNT(t.`{col}`) = 0
                    THEN 0
                    ELSE COUNT(DISTINCT t.`{col}`) / COUNT(t.`{col}`)
                    END
                AS probability,
                ''{col}'' as ''(helper)col''
            FROM `{table}` t UNION ALL',
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
    AND cols.is_nullable = 'NO'
    AND cols.data_type NOT IN ( 'datetime', 'date', 'timestamp', 'enum', 'money', 'text', 'longtext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cols.table_schema ASC;