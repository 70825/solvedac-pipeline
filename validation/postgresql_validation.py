import pandas as pd
from database.postgresql import postgresql


class postgresql_validation(postgresql):
    def user_validation(self, df):
        query = 'SELECT * FROM userID'
        result_query = self.readQuery(query)
        if result_query == []:
            sql_df = pd.DataFrame({'index': [], 'name': []})
        else:
            index, name = [], []
            for idx, uname in result_query:
                index.append(idx)
                name.append(uname)
            sql_df = pd.DataFrame({'index': index, 'name': name})
        df = pd.concat((df, sql_df))

        return df['name'].is_unique

    def problem_validation(self, df):
        query = 'SELECT * FROM problemID'
        result_query = self.readQuery(query)
        if result_query == []:
            sql_df = pd.DataFrame({'index': [], 'num': []})
        else:
            index, num = [], []
            for idx, pnum in result_query:
                index.append(idx)
                num.append(pnum)
            sql_df = pd.DataFrame({'index': index, 'num': num})
        df = pd.concat((df, sql_df))

        return df['num'].is_unique
