class NutrientAmount:
    """Represents a FoodItem as found in the ontology.

    Attributes
    ----------
    food_item_uri: str
        Food Item Uniform Resource Identifier, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
    nutrient_uri: str
        Nutrient Uniform Resource Identifier.
    nutrient_label: str
        A common name for the nutrient.
    unit: str
        The unit of measurement as found in https://foodvoc.org/page/om-2.
    value: float
        The amount of this nutrient.
    """

    food_item_uri: str # TODO: Why not FoodItem instance?
    nutrient_uri: str
    nutrient_label: str
    unit: str
    value: float

    def __init__(self, food_item_uri: str, nutrient_uri: str, nutrient_label: str, unit: str, value: float):
        """Represents a FoodItem as found in the ontology.

        Attributes
        ----------
        food_item_uri: str
            Food Item Uniform Resource Identifier, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
        nutrient_uri: str
            Nutrient Uniform Resource Identifier.
        nutrient_label: str
            A common name for the nutrient.
        unit: str
            The unit of measurement as found in https://foodvoc.org/page/om-2.
        value: float
            The amount of this nutrient.
        """
        self.food_item_uri = food_item_uri
        self.nutrient_uri = nutrient_uri
        self.nutrient_label = nutrient_label
        self.unit = unit
        self.value = value

    def serialize(self):
        """Serialize the NutrientAmount to a dictionary mapping the attributes -> value

        Returns
        ----------
        dict[str, Any]
            The serialized NutrientAmount
        """
        return self.__dict__
