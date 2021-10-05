from dataclasses import dataclass

from campaigns.models import Campaign
from campaigns.serializers import QuerySerializer
from lib.base.factory import BaseFactory


@dataclass
class QueryFactory(BaseFactory):
    campaign: Campaign

    def create(self):
        if self.campaign.queries.count():
            raise Exception("CAMPAIGN ALREADY HAS QUERIES")

        for raw_query in self.campaign.template['queries']:
            raw_query['data'] = raw_query.pop('data_fields')
            serializer = QuerySerializer(data=raw_query)
            serializer.is_valid()
            serializer.save(campaign=self.campaign)
