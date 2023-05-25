import pandas as pd
import customtkinter as tk

root = tk.CTk()
root.geometry("1000x500")
root.title("Shopping List Assembler")

full_data = pd.read_excel('recipe_db.xlsx')


class Recipe:
    
    def __init__(self, name, full_data):
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

    
def merge_ingredient_dictionaries(input_dict, result_dict):
    '''
    Merges nested dictionaries and adds up values.
    NOTE: It modifies original result_dict.    
    '''

    if len(result_dict) == 0:
        return input_dict
    
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

def flatten_dictionary(dictionary):
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


def option_menu_callback(choice):
    choice

def clear_options_event():
    for option in options_dict:
        options_dict[option].set('')


def generate_shopping_list_event():

    selected_recipes = []
    for option in options_dict.keys():
        selected_option = options_dict[option].get()
        if selected_option != '':
        
            recipe = Recipe(selected_option, full_data)
            
            # This needs to be revised after adding extra 'number of portions' button
            # For now program creates list for 2 persons by default
            if recipe.double_portion:
                selected_recipes.append(recipe.get_ingredients())
            else:
                selected_recipes.append(recipe.get_ingredients())
                selected_recipes.append(recipe.get_ingredients())

    merged_recipes = {}
    for item in selected_recipes:
        merged_recipes = merge_ingredient_dictionaries(item, merged_recipes)

    result_dataframe = (
        pd.DataFrame()
        .from_dict(
            flatten_dictionary(merged_recipes), 
            orient='index', 
            columns=['Ilość']
            )
        .sort_index()
    )

    try:  
        print(result_dataframe)
    except UnboundLocalError:
        print('No recipes selected.')

options_dict = {}

week_frame = tk.CTkFrame(root)
for i in range(8):
    week_frame.columnconfigure(i, weight=1)

weekdays = ['','Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'So', 'Nd']
meals = ['', 'Śniadanie', 'Brunch', 'Obiad', 'Podwieczorek', 'Kolacja']


def build_option_menu(day, meal, item_list):
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
    option_menu.grid(row=meals.index(meal), 
                    column=weekdays.index(day), 
                    sticky='we')
    options_dict.update({f'{day}_{meal}' : option_menu})


for day in weekdays:
    for meal in meals:
        if weekdays.index(day) == 0:
            tile = tk.CTkLabel(week_frame, text=meal, font=("Arial", 10))
            tile.grid(row=meals.index(meal), column=weekdays.index(day), sticky='we')
        
        elif meals.index(meal) == 0:
            tile = tk.CTkLabel(week_frame, text=day, font=("Arial", 10))
            tile.grid(row=meals.index(meal), column=weekdays.index(day), sticky='we')
        
        else:           
            if meal == 'Śniadanie':
                build_option_menu(day=day,
                                  meal=meal,
                                  item_list= full_data[full_data.breakfast == True]['name'].unique().tolist()
                                  )
                
            elif meal == 'Brunch' or meal == 'Podwieczorek':
                build_option_menu(day=day,
                                  meal=meal,
                                  item_list= full_data[full_data.intermeal == True]['name'].unique().tolist()
                                  )
            
            elif meal == 'Obiad':
                build_option_menu(day=day,
                                  meal=meal,
                                  item_list= full_data[full_data.lunch == True]['name'].unique().tolist()
                                  )
            
            elif meal == 'Kolacja':
                build_option_menu(day=day,
                                  meal=meal,
                                  item_list= full_data[full_data.dinner == True]['name'].unique().tolist()
                                  )


week_frame.pack(fill='x', padx=20, pady=20)

clear_options_button = tk.CTkButton(root, text="Clear", command=clear_options_event)
clear_options_button.pack(padx=20, pady=20)

generate_shopping_list_button = tk.CTkButton(root, text="Generate shopping list", command=generate_shopping_list_event)
generate_shopping_list_button.pack(padx=20, pady=20)

root.mainloop()