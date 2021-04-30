SELECT
  fks.TABLE_SCHEMA,
	fks.table_name,
	fks.constraint_name
FROM
	information_schema.table_constraints fks,
	information_schema.TABLES tab 
WHERE
	fks.table_schema = tab.table_schema 
	AND fks.table_name = tab.table_name 
	AND fks.constraint_type = 'FOREIGN KEY' 
	AND tab.table_type = 'BASE TABLE' 
	AND tab.table_schema = DATABASE()
ORDER BY
	tab.table_schema,
	tab.table_name;