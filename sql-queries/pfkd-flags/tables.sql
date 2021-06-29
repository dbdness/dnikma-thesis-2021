SELECT
    REPLACE (
        REPLACE (
            REPLACE (
                REPLACE (
                    'SELECT ''{Ltable}.{Lcol}'' as left_col, ''{Rtable}.{Rcol}'' as right_col,
                        CASE 
                            WHEN ''{Rcol}'' LIKE CONCAT(''%%'',SUBSTRING(''{Ltable}'', 1, 4),''%%'') AND ''{Rcol}'' LIKE ''%%id%%'' THEN (COUNT(l.`{Lcol}`)/COUNT(r.`{Rcol}`))+(COUNT(DISTINCT(l.`{Lcol}`))/COUNT(DISTINCT(r.`{Rcol}`))) + 2
                            WHEN ''{Rcol}'' LIKE CONCAT(''%%'',SUBSTRING(''{Ltable}'', 1, 4),''%%'') THEN (COUNT(l.`{Lcol}`)/COUNT(r.`{Rcol}`))+(COUNT(DISTINCT(l.`{Lcol}`))/COUNT(DISTINCT(r.`{Rcol}`))) + 1
                            WHEN ''{Rcol}'' LIKE ''%%id%%'' THEN (COUNT(l.`{Lcol}`)/COUNT(r.`{Rcol}`))+(COUNT(DISTINCT(l.`{Lcol}`))/COUNT(DISTINCT(r.`{Rcol}`))) + 1
                            WHEN COUNT(r.`{Rcol}`) = 0 THEN 0.0000
                            ELSE (COUNT(l.`{Lcol}`)/COUNT(r.`{Rcol}`))+(COUNT(DISTINCT(l.`{Lcol}`))/COUNT(DISTINCT(r.`{Rcol}`)))
                            END
                        AS score,
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
    AND cl.table_name IN (%s) -- < Flag is here
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