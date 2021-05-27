SELECT
    REPLACE (
        REPLACE (
            REPLACE (
                REPLACE (
                    'SELECT ''{Ltable}.{Lcol}'' as left_col, ''{Rtable}.{Rcol}'' as right_col,
                        @lcount:=COUNT(l.`{Lcol}`) as count_left, 
                        @rcount:=COUNT(r.`{Rcol}`) as count_right, 
                        FORMAT(@rcount-@lcount,0) as diff_equal, 
                        @ldis:=COUNT(DISTINCT(l.`{Lcol}`)) as distinct_left, 
                        @rdis:=COUNT(DISTINCT(r.`{Rcol}`)) as distinct_right, 
                        FORMAT(@rdis-@ldis,0) as diff_distinct,
                        CASE WHEN @rcount = 0 
                            THEN 0.0000
                            ELSE @lcount/@rcount
                            END 
                        AS percent_match,
                            CASE WHEN @rdis = 0
                            THEN 0.0000
                            ELSE @ldis/@rdis
                            END
                        AS percent_match_distinct,
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
    AND cl.data_type = cr.data_type
AND cl.column_name IN (
    SELECT
        DISTINCT column_name
    FROM
        information_schema.statistics
    WHERE
        table_schema = DATABASE()
        AND index_name = 'primary'
    )
AND cr.column_name NOT IN (
    SELECT
        DISTINCT column_name
    FROM
        information_schema.statistics
    WHERE
        table_schema = DATABASE()
        AND index_name = 'primary'
    )
WHERE
    cl.table_schema = DATABASE()
    AND cr.table_schema = DATABASE()
    AND cl.data_type NOT IN ( 'datetime', 'date', 'timestamp', 'enum', 'money', 'text', 'longtext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cr.table_schema;