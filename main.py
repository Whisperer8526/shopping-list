import pandas as pd
import customtkinter as tk


from gui import *

if __name__ == "__main__":

    # Define window resolution and app name
    root = tk.CTk()
    root.geometry("1000x500")
    root.title("Shopping List Assembler")

    # Load data from excel file
    full_data = pd.read_excel('recipe_db.xlsx')

    settings = {
        'breakfast' : {
            'item_list' : full_data[full_data.breakfast == True]['name'].unique().tolist(),
            'button_color' : '#3C565B' #teal
        },
        'intermeal' : {
            'item_list' : full_data[full_data.intermeal == True]['name'].unique().tolist(),
            'button_color' : '#483C32' #oak brown
        },
        'lunch_main' : {
            'item_list' : full_data[full_data.lunch_main == True]['name'].unique().tolist(),
            'button_color' : '#5E5A80' #pale purple
        },
        'lunch_filler' : {
            'item_list' : full_data[full_data.lunch_filler == True]['name'].unique().tolist(),
            'button_color' : '#5E5A80' #pale purple
        },
        'lunch_salad' : {
            'item_list' : full_data[full_data.lunch_salad == True]['name'].unique().tolist(),
            'button_color' : '#5E5A80' #pale purple
        },
        'dinner' : {
            'item_list' : full_data[full_data.dinner == True]['name'].unique().tolist(),
            'button_color' : '#7F462C' #sepia
        },


    }



    # Build main table
    option_menu_objects = {}
    week_frame = build_week_frame_table(root, option_menu_objects, settings)
    week_frame.pack(fill='x', padx=20, pady=20)

    # Create 'Clear' button
    clear_options_button = tk.CTkButton(root, 
                                        text="Clear", 
                                        command=lambda: clear_options_event(option_menu_objects))
    clear_options_button.pack(padx=20, pady=20)

    # Create button generating shopping list
    generate_shopping_list_button = tk.CTkButton(root, 
                                                text="Generate shopping list", 
                                                command=lambda: generate_shopping_list_event(option_menu_objects, full_data),
                                                )
    generate_shopping_list_button.pack(padx=20, pady=20)


    root.mainloop()