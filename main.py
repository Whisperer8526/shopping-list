import pandas as pd
import customtkinter as tk


from gui import *
from data_processing import Data


if __name__ == "__main__":

    DATA = Data('recipe_db.xlsx')
    NUMBER_OF_PORTIONS = 0

    # Define window resolution and app name
    root = tk.CTk()
    root.geometry("1050x510")
    root.title("Shopping List Assembler")
    

    # Configuartion of apps grid
    for col in range(8):
        root.columnconfigure(col, weight=1)
    for row in range(20):
        root.rowconfigure(row, weight=1)

    
    settings = {
        'breakfast' : {
            'item_list' : DATA.get_breakfast_list(),
            'button_color' : '#3C565B' #teal
        },
        'intermeal' : {
            'item_list' : DATA.get_intermeal_list(),
            'button_color' : '#483C32' #oak brown
        },
        'lunch_main' : {
            'item_list' : DATA.get_lunch_main_list(),
            'button_color' : '#5E5A80' #pale purple
        },
        'lunch_filler' : {
            'item_list' : DATA.get_lunch_filler_list(),
            'button_color' : '#5E5A80' #pale purple
        },
        'lunch_salad' : {
            'item_list' : DATA.get_lunch_salad_list(),
            'button_color' : '#5E5A80' #pale purple
        },
        'dinner' : {
            'item_list' : DATA.get_dinner_list(),
            'button_color' : '#7F462C' #sepia
        },

    }


    # Build main table
    option_menu_objects = {}
    week_frame = build_week_frame_table(root,
                                        option_menu_objects, 
                                        settings)
    week_frame.grid(row=0, column=0, columnspan=8, rowspan=5, padx=10, sticky='nwes')

    # Create 'Clear' button
    clear_options_button = tk.CTkButton(root,
                                        text="Clear choices", 
                                        command=lambda: clear_options_event(option_menu_objects, number_of_portions_menu, textbox),
                                        fg_color='#A93226')
    clear_options_button.grid(row=5, column=0, sticky='wesn', padx=10)

    # 'Reload Data' button
    reload_data_button = tk.CTkButton(root, 
                                      text="Reload Data",
                                      command= lambda: DATA.reload_data())
    reload_data_button.grid(row=5, column=1, sticky='wesn')

    # Texbox prompt
    textbox = tk.CTkTextbox(root, corner_radius=0, font=('Consolas', 11))
    textbox.configure(state='normal',
                      text_color='white')
    textbox.grid(row=6, column=4, columnspan=4, rowspan=13, sticky='nwe', padx=10)

    # Create button generating shopping list
    generate_shopping_list_button = tk.CTkButton(root, 
                                                text="Generate shopping list", 
                                                command=lambda: generate_results_event(data=DATA.data, 
                                                                                       option_menu_objects=option_menu_objects, 
                                                                                       number_of_portions=NUMBER_OF_PORTIONS,
                                                                                       to_excel=False,
                                                                                       textbox=textbox
                                                                                       ),
                                                corner_radius=0                                       )
    generate_shopping_list_button.grid(row=5, column=4, columnspan=4, padx=10, sticky='wes')

    # 'Save to excel' button
    save_to_excel_button = tk.CTkButton(root, 
                                        text="Save to Excel",
                                        command= lambda: generate_results_event(data=DATA.data, 
                                                                                option_menu_objects=option_menu_objects, 
                                                                                to_excel=True),
                                        fg_color='#10793F')
    save_to_excel_button.grid(row=19, column=4, padx=10, pady=10, sticky='nw')

    # Number of portions menu

    def portions_menu_callback(choice):
        global NUMBER_OF_PORTIONS
        NUMBER_OF_PORTIONS = int(choice)

    number_of_portions_label = tk.CTkLabel(root, text='Number of portions:', font=("Arial", 14))
    number_of_portions_label.grid(row=6, column=0, sticky='wesn', padx=10)

    number_of_portions_menu = tk.CTkOptionMenu(
        root,
        values= [str(n) for n in range(1,6)],
        command=portions_menu_callback,
        variable=tk.StringVar(),
        corner_radius=0,
        anchor='center',
        dynamic_resizing=False,
        font=('Arial', 14)
        )
    number_of_portions_menu.set('Choose number of portions')
    number_of_portions_menu.grid(row=6, column=1, sticky='we')

    

    root.mainloop()