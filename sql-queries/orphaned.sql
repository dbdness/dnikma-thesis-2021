SELECT 
	REPLACE(
		REPLACE(
			REPLACE(
				REPLACE('SELECT ''{ctab}.{ccol}'' AS ''orphan'', 
				''{ptab}.{pcol}'' AS ''parent'', 
				ct.{ccol} AS ''orphan_val'' FROM `{ctab}` ct
				LEFT JOIN `{ptab}` pt ON ct.{ccol} = pt.{pcol}
				WHERE ct.{ccol} IS NOT NULL 
				AND pt.{pcol} IS NULL;', 
			'{ctab}', 
			c.table_name),
		'{ccol}',
		c.column_name),
	'{ptab}',
	p.table_name),
'{pcol}',
p.column_name)
FROM information_schema.COLUMNS c, information_schema.COLUMNS p
WHERE c.table_schema = DATABASE()
	AND p.table_schema = DATABASE()
	AND c.table_name = %(child_tab)s
	AND c.column_name = %(child_col)s
	AND p.table_name = %(parent_tab)s
	AND p.column_name = %(parent_col)s
