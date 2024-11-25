class DataMapper:
    db_model = None
    schema = None

    # Превращаем модель алхимии в пайдентик схему.
    @classmethod
    def map_to_schema(cls, db_model):
        return cls.schema.model_validate(db_model, from_attributes=True)

    # Превращаем пайдентик схему в модель алхимии
    @classmethod
    def map_to_model(cls, schema):
        return cls.db_model(**schema.model_dump())
