import pandas as pd
import customtkinter as tk

class Data:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = pd.read_excel(data_path)

    def reload_data(self):
        self.data = pd.read_excel(self.data_path)

    def get_breakfast_list(self):
        return self.data[self.data.breakfast == True]['name'].unique().tolist()
    
    def get_intermeal_list(self):
        return self.data[self.data.intermeal == True]['name'].unique().tolist()
    
    def get_lunch_main_list(self):
        return self.data[self.data.lunch_main == True]['name'].unique().tolist()
    
    def get_lunch_filler_list(self):
        return self.data[self.data.lunch_filler == True]['name'].unique().tolist()
    
    def get_lunch_salad_list(self):
        return self.data[self.data.lunch_salad == True]['name'].unique().tolist()
    
    def get_dinner_list(self):
        return self.data[self.data.dinner == True]['name'].unique().tolist()


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

    #flattened.pop(' ', None)    
    
    return flattened


def convert_recipes_to_prompt(merged_recipes: dict, textbox: tk.CTkTextbox):
    textbox.delete(index1='0.0', index2='500.0')

    unit_index = 20
    value_index = 30

    for i, (ingredient, units) in enumerate(merged_recipes.items()):
        for item in units.items():
            unit = f'[{item[0]}]'
            value = f'{item[1]}'

            # Dirty way of displaying items in even table-like form in apps text-box
            string = f'''{ingredient}{' '*(unit_index-len(ingredient))}{unit}{' '*(value_index-len(unit))}{value}\n'''
            
            textbox.insert(index=f'{i}.0', text=string)