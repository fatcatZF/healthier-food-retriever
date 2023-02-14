# Healthier Food Retriever

This flask web application implements food retrieval and healthier alternative recommendation. The food retrieval is based on the transformer model "Linus4Lyf/test-food"; the details can be found at https://huggingface.co/Linus4Lyf/test-food. The health value of a food item is computed based on the amounts of nutrients of the food.

## RUN
```flask --app app run```


## API endpoints 
<ul>
  <li>browse available food items: /food-items</li>  
  <li>check detail of a specific food item: /detail/food-items?food_item_uri=...</li>
  <li>search relevant food items given input text: /search?search_text=...</li>
  <li>recommend healthier similar food items: /recommend-alternative-food-items?food_item_uri=...</li>
</ul>
