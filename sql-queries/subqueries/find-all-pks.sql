SET @db = 'northwind_nofks';

SELECT
	tab.table_schema AS database_schema,
	sta.index_name AS pk_name,
	sta.seq_in_index AS column_id,
	sta.column_name,
	tab.table_name,
	cls.data_type 
FROM
	information_schema.TABLES AS tab
	INNER JOIN information_schema.statistics AS sta ON sta.table_schema = tab.table_schema 
	AND sta.table_name = tab.table_name 
	AND sta.index_name = 'primary'
	JOIN information_schema.`COLUMNS` AS cls ON tab.TABLE_SCHEMA = cls.TABLE_SCHEMA 
	AND tab.TABLE_NAME = cls.TABLE_NAME 
	AND sta.column_name = cls.column_name 
WHERE
	tab.table_schema = @db 
	AND tab.table_type = 'BASE TABLE' 
ORDER BY
	tab.table_name,
	column_id;