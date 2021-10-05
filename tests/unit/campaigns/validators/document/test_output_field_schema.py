
class OutputFieldSchemaTestCase(TestCase):
    def setUp(self):
        pass

    def test_constructor(self):
        ...

    def test_from_json(self):
        ...

    def test_validate_correct_record(self):
        ...


    def test_validate_answer_not_found(self):
        ...

    def test_validate_wrong_type(self):
        ...



@dataclass
class OutputFieldSchema(Schema):
    name: str
    type: str
    answers: List[Any] = field(default=None)

    def validate(self, record: RecordDTO):
        validate_type(record.value, self.type)
        if self.answers:
            if record.value not in self.answers:
                raise Exception("VALUE NOT FOUND")

    @staticmethod
    def from_json(output_field_schema: Dict) -> "OutputFieldSchema":
        return OutputFieldSchema(
            name=output_field_schema['name'],
            type=output_field_schema['type'],
            answers=output_field_schema.get('answers'),
        )
