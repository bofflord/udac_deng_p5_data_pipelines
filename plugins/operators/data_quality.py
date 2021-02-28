from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_checks=[""],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_checks = sql_checks

    def execute(self, context):
        self.log.info('Connect to Redshift database')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        for check in self.sql_checks:
            self.log.info(f'Execute data quality check:\n{check}')
            records = redshift_hook.get_records(check)
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. Check returned no results.")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. Check returned zero rows.")
            logging.info(f"Data quality on table check passed with {records[0][0]}             records")
        