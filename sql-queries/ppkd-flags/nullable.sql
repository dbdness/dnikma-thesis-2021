SELECT
    REPLACE (
        REPLACE (
            'SELECT ''{table}.{col}'' as col, 
                @count:=COUNT(t.{col}) as count_total, 
                @dis:=COUNT(DISTINCT t.{col}) as count_distinct, 
                CASE WHEN @count = 0
                    THEN 0.0000
                    ELSE FORMAT(@dis / @count,4)
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
    AND cols.data_type NOT IN ( 'datetime', 'date', 'timestamp', 'money', 'text', 'longtext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cols.table_schema ASC;