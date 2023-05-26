import pandas as pd
import customtkinter as tk


# === Data processing Functions ===

class Recipe:
    
    def __init__(self, name: str, full_data: pd.DataFrame):
        self.name = name
        self.data = full_data[full_data.name == self.name]
        self.is_breakfast = self.data.breakfast.unique()[0]
        self.is_lunch = self.data.lunch.unique()[0]
        self.is_dinner = self.data.dinner.unique()[0]
        self.is_salad = self.data.salad.unique()[0]
        self.is_intermeal = self.data.intermeal.unique()[0]
        self.double_portion = self.data.double_portion.unique()[0]
        
    def get_ingredients(self):
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

    
def merge_ingredient_dictionaries(recipes_list: list):
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


def flatten_dictionary(dictionary: dict):
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


# === GUI Functions ===

def option_menu_callback(choice):
    choice

def clear_options_event():
    for option in option_menu_objects:
        option_menu_objects[option].set('')


def generate_shopping_list_event():

    selected_recipes = []
    for option in option_menu_objects.keys():
        selected_option = option_menu_objects[option].get()
        if selected_option != '':
        
            recipe = Recipe(selected_option, full_data)
            
            # This needs to be revised after adding extra 'number of portions' button
            # For now program creates list for 2 persons by default
            if recipe.double_portion:
                selected_recipes.append(recipe.get_ingredients())
            else:
                selected_recipes.append(recipe.get_ingredients())
                selected_recipes.append(recipe.get_ingredients())

    
    merged_recipes = merge_ingredient_dictionaries(selected_recipes)

    result_dataframe = (
        pd.DataFrame()
        .from_dict(
            flatten_dictionary(merged_recipes), 
            orient='index', 
            columns=['Ilość']
            )
        .sort_index()
    )

    if result_dataframe.empty:
        print('No recipes selected.')
    else:
        print(result_dataframe)
    

def build_option_menu(week_frame, day_index: int, meal_index: int, item_list: list, option_menu_objects: dict): 
    '''
    Creates option menu object. It stores name of the dish selected for given day and meal.
    '''
        
    item_list.append('')
    option_menu = tk.CTkOptionMenu(week_frame,
                                    values=item_list,
                                    command=option_menu_callback,
                                    variable=tk.StringVar(),
                                    corner_radius=0,
                                    anchor='w',
                                    dynamic_resizing=True,
                                    font=('Arial', 10)
                                    )
    option_menu.set('')
    option_menu.grid(row=meal_index, 
                        column=day_index, 
                        sticky='we')
    option_menu_objects.update({f'{day_index}_{meal_index}' : option_menu})

def build_week_frame_table(option_menu_objects):

    '''
    Creates a table containing option menu objects
    '''

    week_frame = tk.CTkFrame(root)
    for i in range(8):
        week_frame.columnconfigure(i, weight=1)

    weekdays = ['','Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'So', 'Nd']
    meals = ['', 'Śniadanie', 'Brunch', 'Obiad', 'Podwieczorek', 'Kolacja']

    for day_index, day in enumerate(weekdays):
        for meal_index, meal in enumerate(meals):
            
            if day_index == 0:
                tile = tk.CTkLabel(week_frame, text=meal, font=("Arial", 10))
                tile.grid(row=meal_index, column=day_index, sticky='we')
            
            elif meal_index == 0:
                tile = tk.CTkLabel(week_frame, text=day, font=("Arial", 10))
                tile.grid(row=meal_index, column=day_index, sticky='we')
            
            else:           
                if meal == 'Śniadanie':
                    build_option_menu(week_frame,
                                      day_index=day_index,
                                    meal_index=meal_index,
                                    item_list= full_data[full_data.breakfast == True]['name'].unique().tolist(),
                                    option_menu_objects=option_menu_objects
                                    )
                    
                elif meal == 'Brunch' or meal == 'Podwieczorek':
                    build_option_menu(week_frame,
                                      day_index=day_index,
                                      meal_index=meal_index,
                                      item_list= full_data[full_data.intermeal == True]['name'].unique().tolist(),
                                      option_menu_objects=option_menu_objects
                                    )
                
                elif meal == 'Obiad':
                    build_option_menu(week_frame,
                                      day_index=day_index,
                                      meal_index=meal_index,
                                      item_list= full_data[full_data.lunch == True]['name'].unique().tolist(),
                                      option_menu_objects=option_menu_objects
                                    )
                
                elif meal == 'Kolacja':
                    build_option_menu(week_frame,
                                      day_index=day_index,
                                      meal_index=meal_index,
                                      item_list= full_data[full_data.dinner == True]['name'].unique().tolist(),
                                      option_menu_objects=option_menu_objects
                                    )
                    
    return week_frame

# === Main ===

# Define window resolution and app name
root = tk.CTk()
root.geometry("1000x500")
root.title("Shopping List Assembler")

# Load data from excel file
full_data = pd.read_excel('recipe_db.xlsx')

# Build main table
option_menu_objects = {}
week_frame = build_week_frame_table(option_menu_objects)
week_frame.pack(fill='x', padx=20, pady=20)

# Create 'Clear' button
clear_options_button = tk.CTkButton(root, 
                                    text="Clear", 
                                    command=clear_options_event)
clear_options_button.pack(padx=20, pady=20)

# Create button generating shopping list
generate_shopping_list_button = tk.CTkButton(root, 
                                             text="Generate shopping list", 
                                             command=generate_shopping_list_event)
generate_shopping_list_button.pack(padx=20, pady=20)


root.mainloop()