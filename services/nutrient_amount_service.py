from typing import Union, cast
from models.nutrient_amount import NutrientAmount
from models.food_item import FoodItem
from services.constants import FILE_MODE_READ, KEY_DATA, KEY_FOODITEM_URI, KEY_FOODITEMS_WITH_NUTRIENTS, KEY_LABEL_EN, KEY_NUTRIENTS, KEY_UNIT, KEY_URI, KEY_VALUE

import json

# Type hint alias
NutrientAmountData = list[dict[str, Union[str, float]]]
FoodItemsWithNutrientsData = list[dict[str, Union[str, NutrientAmountData]]]

# Constants
ERROR_NUTRIENT_NOT_FOUND: str = 'Nutrient not found.'
NUTRIENT_AMOUNTS_FOR_FOOD_ITEMS_DATA_FILE_PATH: str = 'data/nutrient_amounts_for_food_items.json'


class NutrientAmountServiceException(Exception):
    """An Exception in the NutrientAmount service, do nothing.
    """
    pass


class NutrientAmountService:
    """The NutrientAmount Service is responsible for interacting with the corresponding json files.

    Attributes
    ----------
    nutrient_amounts_by_food_item_uri: dict[str, list[NutrientAmount]]
        The retrieved nutrients ordered by URI, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
    """

    nutrient_amounts_by_food_item_uri: dict[str, list[NutrientAmount]] = {}

    def __init__(self):
        """Create NutrientAmount service. 
        """
        food_items_with_nutrients_data: FoodItemsWithNutrientsData = self.__load_food_items_with_nutrients_data()
        self.nutrient_amounts_by_food_item_uri: dict[str, list[NutrientAmount]] = {str(food_item_with_nutrients[KEY_FOODITEM_URI]): self.__load_nutrient_amounts_array(
            cast(NutrientAmountData, food_item_with_nutrients[KEY_NUTRIENTS])) for food_item_with_nutrients in food_items_with_nutrients_data}

    def get_food_item_uris_for_nutrient_amounts(self) -> list[str]:
        """Get the Food Item URIs for loaded nutrients.

        Returns
        -------
        list[str]
            The Food Item URIs as strings
        """
        return list(self.nutrient_amounts_by_food_item_uri.keys())

    def get_nutrient_amount_by_uri(self, nutrient_amounts: list[NutrientAmount], nutrient_amount_uri: str) -> NutrientAmount:
        """Retrieve a specific NutrientAmount by URI.

        Parameters
        ----------
        nutrient_amounts: list[NutrientAmount]
            The list of NutrientAmounts to look in.
        nutrient_amount_uri: str
            The Nutrient URI to look for, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
        
        Returns
        -------
        NutrientAmount
            The requested NutrientAmount
        """
        nutrient_amount_x = NutrientAmount('_', '_', '_', '_', -1.0)
        for nutrient_amount in nutrient_amounts:
            if nutrient_amount.nutrient_uri == nutrient_amount_uri:
                return nutrient_amount
        return nutrient_amount_x
    
    def get_nutrient_amounts_for_food_item(self, food_item: FoodItem) -> list[NutrientAmount]:
        """Get nutrient amounts for a specific FoodItem.

        Parameters
        ----------
        food_item: FoodItem
            The Food Item to retrieve Nutrients from

        Returns
        -------
        list[NutrientAmount]
            A list of NutrientAmounts coupled to the specific FoodItem
        """
        if food_item.uri in self.nutrient_amounts_by_food_item_uri.keys():
            nutrient_amounts: list[NutrientAmount] = self.nutrient_amounts_by_food_item_uri[food_item.uri]
            return nutrient_amounts
        else:
            raise NutrientAmountServiceException(ERROR_NUTRIENT_NOT_FOUND)

    def __load_food_items_with_nutrients_data(self) -> FoodItemsWithNutrientsData:
        """Load Food Items with nutrient data from JSON

        Returns
        -------
        FoodItemsWithNutrientsData
            The Food Items with nutrientdata dictionary
        """
        food_items_with_nutrients = []
        with open(NUTRIENT_AMOUNTS_FOR_FOOD_ITEMS_DATA_FILE_PATH, FILE_MODE_READ) as data_file:
            food_items_with_nutrients: FoodItemsWithNutrientsData = json.load(
                data_file)[KEY_DATA][0][KEY_FOODITEMS_WITH_NUTRIENTS]
        return food_items_with_nutrients

    def __load_nutrient_amounts_array(self, raw_nutrient_amount_data: NutrientAmountData) -> list[NutrientAmount]:
        """Transform raw_nutrient_data to list of NutrientAmount.

        Parameters
        ----------
        raw_nutrient_amount_data: NutrientAmountData
            The raw nutrient amount data to transform
        
        Returns
        -------
        list[NutrientAmount]
            The NutrientAmount data as a list
        """
        nutrient_amounts: list[NutrientAmount] = []
        for raw_nutrient_amount in raw_nutrient_amount_data:
            food_item_uri: str = str(raw_nutrient_amount[KEY_FOODITEM_URI])
            nutrient_uri: str = str(raw_nutrient_amount[KEY_URI])
            nutrient_label: str = str(raw_nutrient_amount[KEY_LABEL_EN])
            unit: str = str(raw_nutrient_amount[KEY_UNIT])
            value: float = float(raw_nutrient_amount[KEY_VALUE])
            nutrient_amount = NutrientAmount(
                food_item_uri=food_item_uri, nutrient_uri=nutrient_uri, nutrient_label=nutrient_label, unit=unit, value=value)
            nutrient_amounts.append(nutrient_amount)
        return nutrient_amounts
