SET
    @db = 'northwind_nofks',
    @pk_nullable = 'NO'; -- Design this as a flag for the CLI tool (for some DB designs, this might be 'YES').

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
    cols.table_schema = @db
    AND cols.is_nullable = @pk_nullable
    AND cols.data_type NOT IN ( 'datetime', 'timestamp', 'money', 'text', 'lontext', 'longblob', 'blob', 'decimal' ) 
    AND cols.data_type NOT IN ( 'datetime', 'timestamp', 'money', 'text', 'lontext', 'longblob', 'blob', 'decimal' ) 
ORDER BY
    cols.table_schema ASC;