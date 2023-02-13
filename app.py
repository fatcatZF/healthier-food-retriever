from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from services.recommender_service import RecommenderService, RecommenderServiceException
from services.food_item_service import FoodItemService, FoodItemServiceException
from services.nutrient_amount_service import NutrientAmountService, NutrientAmountServiceException
from services.search_service import SearchService
from models.food_item import FoodItem

app = Flask(__name__)

ARGUMENT_FOOD_ITEM_URI: str = 'food_item_uri'
ARGUMENT_SEARCH_TEXT: str = "search_text"

@app.route("/")
def home_page():
    return """
             <html>
                <h1>Healthier Food Retriever</h1>
                <p>
                Available APIs
                <ul>
                  <li>browse available food items: /food-items</li>
                  <li>browse available food item uris: /food-item-uris</li>
                  <li>check the detail of specific food item: /detail/food-items/food_item_uri</li>
                  <li>recommend healthier similar food items: /recommend-alternative-food-items</li>
                </ul>
                </p>
             </html> 
           """

recommender_service = RecommenderService() # initialise the RecommenderService() to reduce response time 

@app.route("/recommend-alternative-food-item")
def recommend_alternative_food_item():
    """Recommend a healthy alternative to given fooditem. Expects argument 'food_item_uri'.
    """
    #recommender_service = RecommenderService() # It takes time to initialize the recommender_service, because of the embedding process
    food_item_service = FoodItemService()

    food_item_uri: str = request.args.get(ARGUMENT_FOOD_ITEM_URI, default='')
    if food_item_uri == '':
        raise HTTPException('Invalid food item uri.')
    food_item: FoodItem = food_item_service.get_food_item(
        food_item_uri=food_item_uri)
    alternative_food_item = recommender_service.recommend_alternative_food_item(
        food_item=food_item)
    return jsonify(alternative_food_item.serialize())


@app.route("/food-items")
def food_items():
    """Retrieve all fooditems.
    """
    food_item_service = FoodItemService()
    food_items: list[FoodItem] = food_item_service.get_food_items()
    return jsonify([food_item.serialize() for food_item in food_items])


@app.route("/food-item-uris")
def food_item_uris():
    """Retrieve the food-item uris.
    """
    nutrient_amount_service = NutrientAmountService()
    food_item_uris = nutrient_amount_service.get_food_item_uris_for_nutrient_amounts()
    start_index = max(int(request.args.get('start_index', default=0)), 0)
    end_index = min(int(request.args.get(
        'end_index', default=100)), len(food_item_uris) - 1)
    filtered_food_item_uris = sorted(food_item_uris)[
        start_index:(end_index + 1)]
    return jsonify(filtered_food_item_uris)



search_service = SearchService()

@app.route("/search")
def search_food():
    """
    search relevant food items given text
    """
    search_text: str = request.args.get(ARGUMENT_SEARCH_TEXT, default='') 
    if search_text == '':
        raise HTTPException("Invalid food name.")
    relevant_food_items = search_service.compute_top_k_sim_items(search_text)

    return jsonify([food.serialize() for food in relevant_food_items])




@app.route("/detail")
def food_item_detail():
    """
    view detail of a specific food item given uri
    """
    food_item_service = FoodItemService()
    nutrient_amount_service = NutrientAmountService()
    food_item_uri: str = request.args.get(ARGUMENT_FOOD_ITEM_URI, default='')
    if food_item_uri == '':
        raise HTTPException('Invalid food item uri.')
    food_item: FoodItem = food_item_service.get_food_item(
        food_item_uri=food_item_uri)
    nutrient_amount = nutrient_amount_service.get_nutrient_amounts_for_food_item(food_item)
    food_item_nutrient_dict = {"food_item": food_item.serialize(),
        "nutrient_amounts":[nutrient.serialize() for nutrient in nutrient_amount]               
    }
    return jsonify(food_item_nutrient_dict)
    
    
    






@app.errorhandler(Exception)
def handle_exception(e):
    """Handle Errornous requests to API by returning HTTP 500.
    """
    exception_classes = [HTTPException, NutrientAmountServiceException,
                         FoodItemServiceException, RecommenderServiceException]
    if type(e) in exception_classes:
        return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "See internal logs."}), 500
