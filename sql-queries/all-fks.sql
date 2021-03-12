SELECT
	fks.table_schema,
	fks.table_name,
	fks.constraint_name,
	fks.constraint_type 
FROM
	information_schema.table_constraints fks,
	information_schema.TABLES tab 
WHERE
	fks.table_schema = tab.table_schema 
	AND fks.table_name = tab.table_name 
	AND fks.constraint_type = 'FOREIGN KEY' 
	AND tab.table_type = 'BASE TABLE' 
	AND tab.table_schema NOT IN ( 'mysql', 'information_schema', 'performance_schema', 'sys' ) 
ORDER BY
	tab.table_schema,
	tab.table_name;