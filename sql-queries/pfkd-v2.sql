SELECT
    REPLACE (
        REPLACE (
            REPLACE (
                REPLACE (
                    'SELECT ''{Ltable}.{Lcol}'' as left_col, ''{Rtable}.{Rcol}'' as right_col,
                        COUNT(l.`{Lcol}`) as count_left, 
                        COUNT(r.`{Rcol}`) as count_right, 
                        COUNT(r.`{Rcol}`) - COUNT(l.`{Lcol}`) as count_equal,
                        COUNT(DISTINCT l.`{Lcol}`) as distinct_left, 
                        COUNT(DISTINCT r.`{Rcol}`) as distinct_right, 
                        COUNT(DISTINCT r.`{Rcol}`) - COUNT(DISTINCT l.`{Lcol}`) as distinct_equal,
                        CASE WHEN COUNT(r.`{Rcol}`) = 0 
                            THEN 0
                            ELSE COUNT(l.`{Lcol}`) / COUNT(r.`{Rcol}`)
                            END 
                        AS probability,
                            CASE WHEN COUNT(DISTINCT r.`{Rcol}`) = 0
                            THEN 0
                            ELSE COUNT(DISTINCT l.`{Lcol}`) / COUNT(DISTINCT r.`{Rcol}`)
                            END
                        AS probability_distinct,
                        ''{Ltable}'' as ''lt(helper)'', ''{Lcol}'' as ''lc(helper)'', 
                        ''{Rtable}'' as ''rt(helper)'', ''{Rcol}'' as ''rc(helper)''
                    FROM `{Ltable}` l 
                    RIGHT JOIN `{Rtable}` r ON l.`{Lcol}` = r.`{Rcol}` 
                    UNION ALL',
                '{Ltable}',
                cl.table_name
                ),
            '{Rtable}',
            cr.table_name
            ),
        '{Lcol}',
        cl.column_name
        ),
    '{Rcol}',
    cr.column_name
    )
FROM
    information_schema.COLUMNS cl
    INNER JOIN information_schema.COLUMNS cr ON cl.table_name <> cr.table_name
    AND cl.table_schema = cr.table_schema
    AND cl.data_type = cr.data_type
    AND CONCAT(cl.table_name, '.', cl.column_name) IN (
        SELECT DISTINCT CONCAT(table_name, '.', column_name)
        FROM
            information_schema.statistics
        WHERE
            table_schema = DATABASE()
            AND index_name = 'primary'
    )
    AND CONCAT(cr.table_name, '.', cr.column_name) NOT IN (
        SELECT DISTINCT CONCAT(table_name, '.', column_name)
        FROM
            information_schema.statistics
        WHERE
            table_schema = DATABASE()
            AND index_name = 'primary'
    )
WHERE
    cl.table_schema = DATABASE()
    AND cl.data_type NOT IN ( 'datetime', 'date', 'timestamp', 'enum', 'money', 'text', 'longtext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cl.table_schema;