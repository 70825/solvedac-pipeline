import pandas as pd
from database.postgresql import postgresql


class postgresql_validation(postgresql):
    def user_validation(self, df):
        query = 'SELECT * FROM userID'
        result_query = self.readQuery(query)
        sql_df = pd.DataFrame({'id': result_query['id'], 'userId': result_query['userId']})
        df = pd.concat((df, sql_df))

        return df['userId'].is_unique

    def problem_validation(self, df):
        query = 'SELECT * FROM problemID'
        result_query = self.readQuery(query)
        sql_df = pd.DataFrame({'id': result_query['id'], 'userId': result_query['problemId']})
        df = pd.concat((df, sql_df))

        return df['problemId'].is_unique
