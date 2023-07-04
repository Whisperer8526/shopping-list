import pandas as pd

class Recipe:
    
    def __init__(self, name: str, data: pd.DataFrame):
        self.name = name
        self.data = data[data.name == self.name]
        self.is_breakfast = self.data.breakfast.unique()[0]
        self.is_lunch = self.data.lunch_main.unique()[0]
        self.is_filler = self.data.lunch_filler.unique()[0]
        self.is_salad = self.data.lunch_salad.unique()[0]
        self.is_intermeal = self.data.intermeal.unique()[0]
        self.is_dinner = self.data.dinner.unique()[0]
        self.double_portion = self.data.double_portion.unique()[0]
        
    def get_ingredients(self) -> dict[float]:
        '''
        Converts DataFrame with ingredient info into nested dictionary.
        '''

        ingredients_dict = dict()
        for row in self.data[['ingredient', 'unit', 'amount']].values:
            ingredients_dict.update(
                {
                    row[0] : {
                        row[1] : row[2]
                    }
                }
            )

        return ingredients_dict

    
def merge_ingredient_dictionaries(recipes_list: list[dict]) -> dict[float]:
    '''
    Merges nested dictionaries and adds up values.   
    '''

    result_dict = {}
    for input_dict in recipes_list:
        assert isinstance(input_dict, dict)

        if len(result_dict) == 0:
            result_dict = input_dict
        
        else:
            for ingredient in input_dict.keys():
                if ingredient in result_dict.keys():
                    for unit in input_dict[ingredient].keys():
                    
                        if unit in result_dict[ingredient].keys():
                            result_dict[ingredient][unit] += input_dict[ingredient][unit]   
                            
                        else:
                            result_dict[ingredient].update({unit : input_dict[ingredient][unit]})
                
                else:
                    result_dict.update({ingredient : input_dict.get(ingredient)})

                                
    return result_dict


def flatten_dictionary(dictionary: dict[float]) -> dict[float]:
    '''
    Flattens nested dictionary by merging keys.
    '''

    flattened = {}
    for ingredient, units in dictionary.items():
        for item in units.items():
            unit = item[0]
            value = item[1]
            flattened.update({f'{ingredient} [{unit}]' : value})
    
    return flattened