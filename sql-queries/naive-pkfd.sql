SET
    @db = 'northwind_nofks',
    @pk_nullable = 'NO'; -- for some DB designs, this might be 'YES'.

SELECT
    REPLACE (
        REPLACE (
            REPLACE (
                REPLACE (
                    'SELECT ''{Ltable}.{Lcol}'' as left_col, ''{Rtable}.{Rcol}'' as right_col, COUNT(l.{Lcol}) as count_left, COUNT(r.{Rcol}) as count_right, 
                    CASE WHEN count(l.{Lcol}) = 0 
                    THEN 0 
                    ELSE COUNT(r.{Rcol})/COUNT(l.{Lcol})
                    END 
                    AS percent_match
				FROM {Ltable} l LEFT JOIN {Rtable} r ON l.{Lcol} = r.{Rcol} UNION ALL',
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
    INNER JOIN information_schema.COLUMNS cr ON cl.table_name < cr.table_name
    AND cl.data_type = cr.data_type
WHERE
    cl.is_nullable = @pk_nullable
    AND cl.table_schema = @db
    AND cr.table_schema = @db
	AND cl.data_type NOT IN ( 'datetime', 'timestamp', 'money', 'text', 'lontext', 'longblob', 'blob', 'decimal' ) 
	AND cr.data_type NOT IN ( 'datetime', 'timestamp', 'money', 'text', 'lontext', 'longblob', 'blob', 'decimal' ) 
ORDER BY
    cl.data_type ASC;

    