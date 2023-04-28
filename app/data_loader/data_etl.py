import pandas
from app.gateways import ElasticsearchGateway
from app.config import SOURCE_FILE


class DataETL:
    def __init__(self):
        self.source_file = SOURCE_FILE

    def extract(self):
        data = pandas.read_csv(self.source_file)
        return data

    @staticmethod
    def transform(data):
        return data

    @staticmethod
    def load(transformed_data):
        elasticsearch_gateway = ElasticsearchGateway()
        for index, row in transformed_data.iterrows():
            elasticsearch_gateway.upload_item(company_id=row['CompanyId'], description=row['Text'])
        pass

    def run(self):
        extracted_data = self.extract()
        transformed_data = self.transform(extracted_data)
        self.load(transformed_data)
