SELECT
    REPLACE (
        REPLACE (
            REPLACE (
                REPLACE (
                    'SELECT ''{Ltable}.{Lcol}'' as left_col, ''{Rtable}.{Rcol}'' as right_col, 
                        COUNT(l.{Lcol}) as count_left, 
                        COUNT(r.{Rcol}) as count_right, 
                        COUNT(r.{Rcol})-COUNT(l.{Lcol}) as diff_equal, 
                        COUNT(DISTINCT(l.{Lcol})) as distinct_left, 
                        COUNT(DISTINCT(r.{Rcol})) as distinct_right, 
                        COUNT(DISTINCT(r.{Rcol}))-COUNT(DISTINCT(l.{Lcol})) as diff_distinct,
                        CASE WHEN count(r.{Rcol}) = 0 
                            THEN 0 
                            ELSE COUNT(l.{Lcol})/COUNT(r.{Rcol})
                            END 
                        AS percent_match,
						CASE WHEN COUNT(DISTINCT(l.{Lcol})) = 0
						    THEN 0
							ELSE COUNT(DISTINCT(l.{Lcol}))/COUNT(DISTINCT(r.{Rcol}))
							END
						AS percent_match_distinct,
                        ''{Ltable}'' as ''lt(helper)'', ''{Lcol}'' as ''lc(helper)'', 
                        ''{Rtable}'' as ''rt(helper)'', ''{Rcol}'' as ''rc(helper)''
                    FROM {Ltable} l 
                    RIGHT JOIN {Rtable} r ON l.{Lcol} = r.{Rcol} 
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
AND cr.column_name LIKE '%id%' -- < Flag is here
WHERE
    cl.table_schema = DATABASE()
    AND cr.table_schema = DATABASE()
    AND cl.data_type NOT IN ( 'datetime', 'date', 'timestamp', 'money', 'text', 'longtext', 'longblob', 'blob', 'decimal' )
ORDER BY
    cr.table_schema;