from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info('Connect to redshift db')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f'Insert data into table {self.table}')
        insert_sql = """
                            INSERT INTO {} 
                        """.format(self.table)\
                        + self.sql_query
        self.log.info(f'insert sql query:\n {insert_sql}')
        redshift.run(insert_sql)
