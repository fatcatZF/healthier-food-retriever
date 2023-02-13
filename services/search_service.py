from models.food_item import FoodItem
from services.nutrient_amount_service import NutrientAmountService
from services.food_item_service import FoodItemService
from typing import List 
from operator import itemgetter
from sentence_transformers import SentenceTransformer, util
import torch 


class SearchService:
    """
      The search service retrieves relevant food items given text
    """
    def __init__(self) -> None:
        self.food_labels = []
        self.food_uris = []
        self.food_label_embeddings = []
        self.food_item_service = FoodItemService()
        self.embedder = SentenceTransformer("Linus4Lyf/test-food")
        self.__get_food_labels()
        self.__get_food_uris()
        self.__compute_food_label_embeddings()

    def __get_food_labels(self)->None:
        food_item_all = self.food_item_service.get_food_items()
        self.food_labels = [food_item.label for food_item in food_item_all]

    def __get_food_uris(self)->None:
        food_item_all = self.food_item_service.get_food_items()
        self.food_uris = [food_item.uri for food_item in food_item_all]

    def __compute_food_label_embeddings(self):
        self.food_label_embeddings = self.embedder.encode(self.food_labels, 
                                      convert_to_tensor=True)

    def compute_top_k_sim_items(self, search_text:str, topk=20) -> List[FoodItem]:
        food_label_embedding = self.embedder.encode(search_text, convert_to_tensor=True)
        cos_scores = util.cos_sim(food_label_embedding, self.food_label_embeddings)[0]
        top_results = torch.topk(cos_scores, k=topk+1)
        top_results_indices = top_results[1].tolist()
        top_labels = itemgetter(*top_results_indices)(self.food_labels)
        top_uris = itemgetter(*top_results_indices)(self.food_uris)
        top_labels_uris = list(zip(top_uris, top_labels))
        top_food_items = [FoodItem(*label_uri) for label_uri in top_labels_uris]

        return top_food_items