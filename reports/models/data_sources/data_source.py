from django.db import models
from django.utils.translation import gettext_lazy as _


class DataSourceTypes(models.TextChoices):
    CAMPAIGN = 'CAMPAIGN', _('Campaign')
    JOINED = 'JOINED', _('Joined')


class DataSource(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=12,
                            choices=DataSourceTypes.choices,
                            default=DataSourceTypes.CAMPAIGN)

    def to_child(self) -> "DataSource":
        ...

    def get_queryset(self):
        ...


"""

możemy dodać analizy żeby pogrupować sobie datasety

chcemy sobie przygotować dataset:
- wybieramy instytucje
    - możemy wybrać

- wybieramy kampanie
    - sprawdza czy możemy użyć tych instytucji (instytucje z


co jak chcemy analize calej kampanii z roznymi instytucjon group

co jak chcemy joinowac rozne kampanie dla tych samych isntytucji

co jak chcemy joinowac po hierarchi instytucji
- join odbywa sie tylko po instytucjach
- jak decydujemy się joinować po wyższym poziomie hierarchii instytucji to trzeba już dla wszystkich



dataset zwraca queryseta na którym robi sie agregacje


raporty to wizualizacje

"""