from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import operator

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 dq_checks=[{'check_sql': "", 'expected_result': 1 , 'comparison':'='}],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.dq_checks = dq_checks

    def execute(self, context):
        self.log.info('Connect to Redshift database')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        operator_dict = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq}
        
        for check_dict in self.dq_checks:
            check_sql = check_dict['check_sql']
            self.log.info(f'Execute data quality check:\n{check_sql}')
            records = redshift_hook.get_records(check_dict['check_sql'])
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. Check returned no results.")
            num_records = records[0][0]
            if operator_dict[check_dict['comparison']](num_records, check_dict['expected_result']):
                raise ValueError(f"Data quality check failed. Check returned not a value {check_dict['check_sql']} {check_dict['expected_result']}.")
            self.log.info(f"Data quality check on table passed with {records[0][0]} records")
        