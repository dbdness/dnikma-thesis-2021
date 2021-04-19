SET
    @db = 'northwind_nofks',
    @pk_nullable = 'NO'; -- for some DB designs, this might be 'YES'.

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
                        AS percent_match
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
		DISTINCT(sta.column_name) 
	FROM
		information_schema.TABLES AS tab
	INNER JOIN information_schema.statistics AS sta ON sta.table_schema = tab.table_schema 
		AND sta.table_name = tab.table_name 
	    AND sta.index_name = 'primary'
	JOIN information_schema.COLUMNS AS cls ON tab.TABLE_SCHEMA = cls.TABLE_SCHEMA 
        AND tab.TABLE_NAME = cls.TABLE_NAME 
		AND sta.column_name = cls.column_name 
	WHERE
		tab.table_schema = @db 
		AND tab.table_type = 'BASE TABLE' 
	)
AND cr.column_name NOT IN (
	SELECT
		DISTINCT(sta.column_name)
	FROM
		information_schema.TABLES AS tab
	INNER JOIN information_schema.statistics AS sta ON sta.table_schema = tab.table_schema 
		AND sta.table_name = tab.table_name 
		AND sta.index_name = 'primary'
	JOIN information_schema.COLUMNS AS cls ON tab.TABLE_SCHEMA = cls.TABLE_SCHEMA 
		AND tab.TABLE_NAME = cls.TABLE_NAME 
		AND sta.column_name = cls.column_name 
	WHERE
		tab.table_schema = @db 
		AND tab.table_type = 'BASE TABLE' 
	)
WHERE
    cl.is_nullable = @pk_nullable
    AND cl.table_schema = @db
    AND cr.table_schema = @db
ORDER BY
    cr.table_schema;