from typing import Union, cast
from models.food_item import FoodItem
from services.constants import FILE_MODE_READ, KEY_DATA, KEY_LABEL, KEY_PREFLABELS, KEY_URI
import json

# Type hints
PrefLabelData = dict[str, str]
PrefLabelsData = list[PrefLabelData]
FoodItemLabelData = dict[str, Union[str, PrefLabelsData]]
FoodItemsLabelData = list[FoodItemLabelData]

# Constants
ERROR_MESSAGE_FOOD_ITEM_NOT_FOUND: str = 'Food item not found.'
FOOD_ITEMS_DATA_FILE_PATHS: list[str] = ['data/food_item_labels_0_200.json',
                              'data/food_item_labels_201_400.json',
                              'data/food_item_labels_401_600.json',
                              'data/food_item_labels_601_800.json',
                              'data/food_item_labels_801_1000.json',
                              'data/food_item_labels_1001_1200.json',
                              'data/food_item_labels_1201_1400.json',
                              'data/food_item_labels_1401_1600.json',
                              'data/food_item_labels_1601_1800.json',
                              'data/food_item_labels_1801_2000.json',
                              'data/food_item_labels_2001_2151.json']

class FoodItemServiceException(Exception):
    """An Exception in the FoodItems service, do nothing.
    """
    pass


class FoodItemService:
    """The FoodItem Service is responsible for interacting with the corresponding json files.

    Attributes
    ----------
    food_items_by_food_item_uri: dict[str, FoodItem]
        The retrieved fooditems ordered by URI, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
    """
    food_items_by_food_item_uri: dict[str, FoodItem] = {}

    def __init__(self):
        """Create the FoodItem service by loading fooditems.
        """
        food_items_label_data: FoodItemsLabelData = self.__load_food_items_label_data()

        self.food_items_by_food_item_uri: dict[str, FoodItem] = {str(food_item_label_data[KEY_URI]): self.__load_food_item(
            food_item_label_data) for food_item_label_data in food_items_label_data}

    def get_food_items(self) -> list[FoodItem]:
        """Retrieve fooditems by listing the values retrieved during creation.

        Returns
        -------
        list[FoodItem]
            The list of all the Food Items
        """
        return list(self.food_items_by_food_item_uri.values())

    def get_food_item(self, food_item_uri: str) -> FoodItem:
        """Retrieve a specific FoodItem by URI.

        Parameters
        ----------
        food_item_uri:str
            The Uniform Resource Identifier for a FoodItem, see https://nl.wikipedia.org/wiki/Uniform_resource_identifier
        
        Returns
        -------
        FoodItem
            The Food Item found for given URI
        """
        if food_item_uri not in self.food_items_by_food_item_uri.keys():
            raise FoodItemServiceException(ERROR_MESSAGE_FOOD_ITEM_NOT_FOUND)

        food_item = self.food_items_by_food_item_uri[food_item_uri]
        return food_item

    def __load_food_item(self, food_item_label_data: FoodItemLabelData) -> FoodItem:
        """Load a FoodItem from data loaded by JSON.

        Parameters
        ----------
        food_item_label_data: FoodItemLabelData
            LabelData loaded from JSON

        Returns
        -------
        FoodItem
            The FoodItem loaded from FoodItemLabelData
        """
        pref_label: PrefLabelData = cast(
            PrefLabelsData, food_item_label_data[KEY_PREFLABELS])[0]
        food_item_uri: str = str(food_item_label_data[KEY_URI])
        food_item_label: str = str(pref_label[KEY_LABEL])
        food_item = FoodItem(uri=food_item_uri, label=food_item_label)
        return food_item

    def __load_food_items_label_data(self) -> FoodItemsLabelData:
        """Load FoodItemsLabelData from JSON.

        Returns
        -------
        FoodItemsLabelData
            The FoodItemsLabelData retrieved from the json file
        """
        food_items_label_data: FoodItemsLabelData = []
        for food_items_data_file_path in FOOD_ITEMS_DATA_FILE_PATHS:
            with open(food_items_data_file_path, FILE_MODE_READ) as data_file:
                food_items_label_data = food_items_label_data + json.load(
                    data_file)[KEY_DATA]
        return food_items_label_data
