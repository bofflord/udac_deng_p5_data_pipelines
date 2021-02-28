from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 insert_mode="delete-load",
                 sql_query="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.insert_mode = insert_mode
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info('Connect to redshift db')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if (self.insert_mode=="delete-load"):
            self.log.info(f'Insert mode delete-load. Truncate table {self.table}')
            trunquate_sql = """
                            TRUNCATE {}
                            """.format(self.table)
            redshift.run(trunquate_sql)
        else:
            self.log.info(f'Insert mode append-only.')
        
        self.log.info(f'Insert data into table {self.table}')
        insert_sql = """
                     INSERT INTO {} 
                     """.format(self.table)\
                        + self.sql_query
        self.log.info(f'insert sql query:\n {insert_sql}')
        redshift.run(insert_sql)
