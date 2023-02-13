from typing import Any

class FoodItem:
    """Represents a FoodItem as found in the ontology.

    Attributes
    ----------
    uri: str
        A Uniform Resource Identifier, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
    label: str
        A common name for the FoodItem.
    """
    uri: str
    label: str

    def __init__(self, uri: str, label: str):
        """Create a FoodItem.
        
        Parameters
        ----------
        uri: str
            A Uniform Resource Identifier, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
        label: str
            A common name for the FoodItem.
        """
        self.uri = uri
        self.label = label

    def serialize(self) -> dict[str, Any]:
        """Serialize the FoodItem to a dictionary mapping the attributes -> value

        Returns
        ----------
        dict[str, Any]
            The serialized FoodItem
        """
        return self.__dict__
