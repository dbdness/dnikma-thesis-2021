SET
    @child_tab = 'order_details',
    @child_col = 'product_id',
    @parent_tab = 'products',
    @parent_col = 'id';

SELECT 
	REPLACE(
		REPLACE(
			REPLACE(
				REPLACE('SELECT ''{ctab}.{ccol}'' AS ''orphan'', 
				''{ptab}.{pcol}'' AS ''parent'', 
				{ccol} AS ''orphan_val'' FROM {ctab} ct 
				LEFT JOIN {ptab} pt ON ct.{ccol} = pt.{pcol} 
				WHERE pt.{pcol} IS NULL;', 
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
	AND c.table_name = @child_tab
    AND c.column_name = @child_col
    AND p.table_name = @parent_tab
    AND p.column_name = @parent_col;
