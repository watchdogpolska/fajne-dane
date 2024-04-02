from campaigns.models import FileSource
from dataclasses import dataclass
from .component import ReportComponent
from .consts import ReportComponentTypes
from datetime import datetime



@dataclass
class Reference:
  name: str
  timestamp: datetime
  link: str

  def to_json(self):
    return {
      "name": self.name,
      "timestamp": str(self.timestamp),
      "link": self.link
    }


class ReferencesComponent(ReportComponent):

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = ReportComponentTypes.REFERENCES
        super().__init__(*args, **kwargs)

    @property
    def data(self):
        sources = FileSource.objects.filter(campaign__source__views__report_components__report=self.report).distinct()
        return [
            Reference(
                name=source.name,
                timestamp=source.source_date,
                link=source.source_link
            ).to_json()
            for source in sources
        ]
