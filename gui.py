import pandas as pd
import customtkinter as tk
from data_processing import (
    Recipe,
    merge_ingredient_dictionaries,
    flatten_dictionary,
    convert_recipes_to_prompt
)

def option_menu_callback(choice):
    choice


def clear_options_event(option_menu_objects: dict[tk.CTkOptionMenu]):
    for option in option_menu_objects:
        option_menu_objects[option].set('')


def generate_results_event(data: pd.DataFrame, 
                           option_menu_objects: dict[tk.CTkOptionMenu], 
                           to_excel: bool, 
                           textbox: tk.CTkTextbox):

    selected_recipes = []
    for option in option_menu_objects.keys():
        selected_option = option_menu_objects[option].get()
        if selected_option != '':
        
            recipe = Recipe(selected_option, data)
            
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
        textbox.delete(index1='0.0', index2='500.0')
        textbox.insert(index='0.0', text='No recipes selected.')
        print('No recipes selected.')
    else:
        if to_excel:
            result_dataframe.to_excel('Lista zakupów.xlsx')
        else:
            
            convert_recipes_to_prompt(merged_recipes, textbox)
            print(result_dataframe)

def convert_recipes_to_prompt(merged_recipes: dict, textbox: tk.CTkTextbox):
    textbox.delete(index1='0.0', index2='500.0')

    unit_index = 25
    value_index = 15

    for i, (ingredient, units) in enumerate(merged_recipes.items()):
        for item in units.items():
            unit = f'[{item[0]}]'
            value = f'{item[1]}'

            string = f'''{ingredient}{' '*(unit_index-len(ingredient))}{unit}{' '*(value_index-len(unit))}{value}\n'''
            
            textbox.insert(index=f'{i}.0', text=string)


def build_option_menu(
        week_frame: tk.CTkFrame, 
        day_index: int, 
        meal_index: int, 
        item_list: list[str], 
        option_menu_objects: dict[tk.CTkOptionMenu], 
        color: str): 
    
    '''
    Creates option menu object. It stores name of the dish selected for given day and meal.
    '''
    
    #item_list.append('')
    option_menu = tk.CTkOptionMenu(
        week_frame,
        values= item_list + [''],
        command=option_menu_callback,
        variable=tk.StringVar(),
        corner_radius=0,
        anchor='w',
        dynamic_resizing=False,
        font=('Arial', 10),
        button_color=color,
        fg_color=color
        )
    option_menu.set('')
    option_menu.grid(
        row=meal_index, 
        column=day_index, 
        sticky='we'
        )
    option_menu_objects.update({f'{day_index}_{meal_index}' : option_menu})


def build_week_frame_table(root: tk.CTk, option_menu_objects: dict[tk.CTkOptionMenu], settings: dict) -> tk.CTkFrame:

    '''
    Creates a table containing option menu objects
    '''

    week_frame = tk.CTkFrame(root)
    for i in range(8):
        week_frame.columnconfigure(i, weight=1)

    weekdays = ['','Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'So', 'Nd']
    meals = ['', 'Śniadanie', 'Brunch', 'Obiad', 'Zapychacz', 'Surówka', 'Podwieczorek', 'Kolacja']

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
                    build_option_menu(
                        week_frame,
                        day_index=day_index,
                        meal_index=meal_index,
                        item_list=settings['breakfast'].get('item_list'),
                        option_menu_objects=option_menu_objects,
                        color=settings['breakfast'].get('button_color')
                        )
                    
                elif meal == 'Brunch' or meal == 'Podwieczorek':
                    build_option_menu(
                        week_frame,
                        day_index=day_index,
                        meal_index=meal_index,
                        item_list=settings['intermeal'].get('item_list'),
                        option_menu_objects=option_menu_objects,
                        color=settings['intermeal'].get('button_color')
                        )
                
                elif meal == 'Obiad':
                    build_option_menu(
                        week_frame,
                        day_index=day_index,
                        meal_index=meal_index,
                        item_list=settings['lunch_main'].get('item_list'),
                        option_menu_objects=option_menu_objects,
                        color=settings['lunch_main'].get('button_color')
                                    )
                    
                elif meal == 'Zapychacz':
                    build_option_menu(
                        week_frame,
                        day_index=day_index,
                        meal_index=meal_index,
                        item_list=settings['lunch_filler'].get('item_list'),
                        option_menu_objects=option_menu_objects,
                        color=settings['lunch_filler'].get('button_color')
                                    )
                    
                elif meal == 'Surówka':
                    build_option_menu(
                        week_frame,
                        day_index=day_index,
                        meal_index=meal_index,
                        item_list=settings['lunch_salad'].get('item_list'),
                        option_menu_objects=option_menu_objects,
                        color=settings['lunch_salad'].get('button_color')
                                    )
                
                elif meal == 'Kolacja':
                    build_option_menu(
                        week_frame,
                        day_index=day_index,
                        meal_index=meal_index,
                        item_list=settings['dinner'].get('item_list'),
                        option_menu_objects=option_menu_objects,
                        color=settings['dinner'].get('button_color')
                                    )
                    
    return week_frame