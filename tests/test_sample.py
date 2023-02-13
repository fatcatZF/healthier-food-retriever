
from typing import List
from models.food_item import FoodItem
from models.nutrient_amount import NutrientAmount
from services.nutrient_amount_service import NutrientAmountService
from services.recommender_service import RecommenderService

EXEMPLAR_FOOD_ITEM_URI: str = 'http://www.foodvoc.org/resource/nevo#foodItem5083'
EXEMPLAR_FOOD_ITEM_LABEL: str = 'Cake Dutch spiced ontbijtkoek w chocolate'
EXEMPLAR_NUTRIENT_AMOUNT_URI: str = 'http://www.foodvoc.org/resource/nevo#nutrientFAPUN6'


INPUT_FOOD_ITEM_URI: str = 'http://www.foodvoc.org/resource/nevo#foodItem1'
INPUT_FOOD_ITEM_LABEL: str = 'Potatoes raw'

OUTPUT_FOOD_ITEM_URIS: List[str] = ['http://www.foodvoc.org/resource/nevo#foodItem2',
                                     'http://www.foodvoc.org/resource/nevo#foodItem671',
                                     'http://www.foodvoc.org/resource/nevo#foodItem63',
                                     'http://www.foodvoc.org/resource/nevo#foodItem2744',
                                     'http://www.foodvoc.org/resource/nevo#foodItem2112']
OUTPUT_FOOD_ITEM_LABELS: List[str] = ['Potatoes new raw',
                                      'Potato sweet raw',
                                      'Onions raw',
                                      'Potatoes Nicola wo skin boiled',
                                      'Potato sweet boiled']






class TestClass:

    def test_get_nutrients_amount_for_food_item(self):
        """Test the Nutrients amount service by retrieving an examplar URI and checking value.
        """
        nutrient_amount_service: NutrientAmountService = NutrientAmountService()
        foodItem: FoodItem = FoodItem(EXEMPLAR_FOOD_ITEM_URI, EXEMPLAR_FOOD_ITEM_LABEL)
        nutrient_amounts: list[NutrientAmount] = nutrient_amount_service.get_nutrient_amounts_for_food_item(foodItem)
        nutrient_amount: NutrientAmount = nutrient_amount_service.get_nutrient_amount_by_uri(nutrient_amounts, EXEMPLAR_NUTRIENT_AMOUNT_URI)

        assert nutrient_amount.value == 0.2


    #
    # IMPLEMENT THIS TEST FUNCTION
    # This is the test function you need to implement in order to test the recommended healthier food product function.
    #

    def test_recommend_alternative_food_item(self):
        recommender_service:RecommenderService = RecommenderService()

        # test case 1
        foodItem:FoodItem = FoodItem(INPUT_FOOD_ITEM_URI, INPUT_FOOD_ITEM_LABEL)
        foodItem_outputs = recommender_service.recommend_alternative_food_item(foodItem)

        uri_outputs = [food.uri for food in foodItem_outputs]
        label_outputs = [food.label for food in foodItem_outputs]

        assert set(uri_outputs) == set(OUTPUT_FOOD_ITEM_URIS)
        assert set(label_outputs) == set(OUTPUT_FOOD_ITEM_LABELS)





