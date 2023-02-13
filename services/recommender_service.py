from models.food_item import FoodItem
from models.nutrient_amount import NutrientAmount
from services.nutrient_amount_service import NutrientAmountService
from services.food_item_service import FoodItemService
import math
from operator import itemgetter
from typing import List

from sentence_transformers import SentenceTransformer, util
import torch 
# Transformer model to embedding food labels to compute similarity between food items




class RecommenderServiceException(Exception):
    """An Exception in the Recommender service, do nothing.
    """
    pass


class RecommenderService:
    """The recommender service recommends healthier alternatives.
       The goal is to recommend similar food items with highest nutrition value

       1. compute nutrition value:
          We consider the following features for computing nutrition value:
              'alcohol', 'calcium', 'carbohydrate', 'fat, total', 
              'polyunsaturated fatty acids', 'saturated fatty acids',
              'trans fatty acids', 'fibre', 'protein', 'vitamin', 'energy'
              'thiamin', 'sugars'
            We expect healthier food items have lower energy, carbohydrate, sugars, alcohol,
               fat, saturated fatty acids, trans fatty acida, and have more calcium, 
               polyunsaturated fatty acids, fibre, protein, vitamin, thiamin. The desired features' 
               weights are 1 and undesired features' weights are -1.
               
       2. compute similarity between food items:
          It's reasonable to recommend similar food items. E.g., when someone is looking for bread, it 
            makes no sense to recommend soy sauce. A pre-trained transformer model is applied to compute 
            similarity between food items by computing the embeddings of food labels.
            The model can be found at https://huggingface.co/Linus4Lyf/test-food 
    """
    #
    # IMPLEMENT THIS FUNCTION
    # This is the core function you need to implement in order to get the recommended healthier food product.
    #
    def __init__(self, use_nutrient_dict:dict={
            'alcohol': -1,
            'calcium': 1,
            'carbohydrate': -1,
            'fat, total': -1,
            'fatty acids, total polyunsaturated': 1,
            'fatty acids, total saturated': -1,
            'fatty acids, total trans': -1,
            'fibre, total dietary': 1,
            'protein, total': 1,
            'vitamin B-12': 1,
            'vitamin B-6, total': 1,
            'vitamin C': 1,
            'vitamin D': 1,
            'vitamin E; alpha-tocopherol equiv from E vitamer activities': 1,
            'vitamin K, total': 1,
            'energy kcal, total metabolisable': -1,
            'thiamin': 1,
            'sugars, total': -1
            }):
        self.food_value_dict = {}
        self.food_labels = []
        self.food_uris = []
        self.food_label_embeddings = []
        self.food_item_service = FoodItemService()
        self.nutrient_amount_service = NutrientAmountService()
        self.embedder = SentenceTransformer("Linus4Lyf/test-food")
        # a transformer model to compute embeddings by using the food label
        self.__get_food_labels()
        self.__get_food_uris()
        self.__compute_nutrient_value(use_nutrient_dict)
        self.__compute_food_label_embeddings()

    def __get_food_labels(self)->None:
        food_item_all = self.food_item_service.get_food_items()
        self.food_labels = [food_item.label for food_item in food_item_all]

    def __get_food_uris(self)->None:
        food_item_all = self.food_item_service.get_food_items()
        self.food_uris = [food_item.uri for food_item in food_item_all]

    def __compute_nutrient_value(self, use_nutrient_dict:dict)->None:
        food_item_all = self.food_item_service.get_food_items()
        nutrient_amount_all = [self.nutrient_amount_service.get_nutrient_amounts_for_food_item(food_item) \
                               for food_item in food_item_all]
        for i, nutrient_amount in enumerate(nutrient_amount_all):
            food_item_uri = food_item_all[i].uri
            value = sum([use_nutrient_dict.get(nutrient_amount_i.nutrient_label, 0)*\
                nutrient_amount_i.value for nutrient_amount_i in nutrient_amount])
            self.food_value_dict[food_item_uri] = 1/(1+math.exp(-value*0.01))
            #scale the nutrient value to the range [0, 1]
            #prevent overflow by multiplying the scalor 0.01

    def __compute_food_label_embeddings(self):
        self.food_label_embeddings = self.embedder.encode(self.food_labels, 
                                      convert_to_tensor=True)

    def __compute_top_k_sim_items(self, food_item:FoodItem, top_k=10) -> List[FoodItem]:
        """
        return top 10 similar food items 
        """
        food_label = food_item.label
        food_uri = food_item.uri 
        food_label_embedding = self.embedder.encode(food_label, convert_to_tensor=True)
        cos_scores = util.cos_sim(food_label_embedding, self.food_label_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k+1)
        top_results_indices = top_results[1].tolist()

        top_labels = itemgetter(*top_results_indices)(self.food_labels)
        top_uris = itemgetter(*top_results_indices)(self.food_uris)
        top_labels_uris = list(zip(top_uris, top_labels))
        top_food_items = [FoodItem(*label_uri) for label_uri in top_labels_uris]

        return top_food_items


    def recommend_alternative_food_item(self, food_item: FoodItem) -> List[FoodItem]:
        sim_food_items = self.__compute_top_k_sim_items(food_item) 

        uri = food_item.uri 
        # compute similar food items
        nutrient_value = self.food_value_dict.get(food_item.uri, 0)

        # filter healthier food items
        food_item_healthier = [food_item for food_item in sim_food_items if self.food_value_dict.get(food_item.uri,0)>nutrient_value and food_item.uri!=uri]

        #The purpose is to reduce the size of filtered dictionary to improve efficiency
        if food_item_healthier:#if healthier options exist 
            return food_item_healthier 
        else:
            return [food_item]
