import pandas as pd
import customtkinter as tk


from gui import *

if __name__ == "__main__":

    # Define window resolution and app name
    root = tk.CTk()
    root.geometry("1050x500")
    root.title("Shopping List Assembler")
    
    for col in range(8):
        root.columnconfigure(col, weight=1)
    
    for row in range(20):
        root.rowconfigure(row, weight=1)

    DATA = None

    def load_data(data_file: str):
        global DATA
        DATA = pd.read_excel(data_file)

    # Load data from excel file
    load_data('recipe_db.xlsx')

    settings = {
        'breakfast' : {
            'item_list' : DATA[DATA.breakfast == True]['name'].unique().tolist(),
            'button_color' : '#3C565B' #teal
        },
        'intermeal' : {
            'item_list' : DATA[DATA.intermeal == True]['name'].unique().tolist(),
            'button_color' : '#483C32' #oak brown
        },
        'lunch_main' : {
            'item_list' : DATA[DATA.lunch_main == True]['name'].unique().tolist(),
            'button_color' : '#5E5A80' #pale purple
        },
        'lunch_filler' : {
            'item_list' : DATA[DATA.lunch_filler == True]['name'].unique().tolist(),
            'button_color' : '#5E5A80' #pale purple
        },
        'lunch_salad' : {
            'item_list' : DATA[DATA.lunch_salad == True]['name'].unique().tolist(),
            'button_color' : '#5E5A80' #pale purple
        },
        'dinner' : {
            'item_list' : DATA[DATA.dinner == True]['name'].unique().tolist(),
            'button_color' : '#7F462C' #sepia
        },

    }


    # Build main table
    option_menu_objects = {}
    week_frame = build_week_frame_table(root,
                                        option_menu_objects, 
                                        settings)
    week_frame.grid(row=0, column=0, columnspan=8, rowspan=5, padx=10, sticky='nwe')

    # Create 'Clear' button
    clear_options_button = tk.CTkButton(root,
                                        text="Clear choices", 
                                        command=lambda: clear_options_event(option_menu_objects),
                                        fg_color='#A93226')
    clear_options_button.grid(row=5, column=0, sticky='wesn', padx=10)

    # 'Reload Data' button
    reload_data_button = tk.CTkButton(root, 
                                      text="Reload Data",
                                      command= lambda: load_data('recipe_db.xlsx'))
    reload_data_button.grid(row=5, column=1, sticky='wesn')

    # Texbox prompt
    textbox = tk.CTkTextbox(root, corner_radius=0, font=('Consolas', 9))
    textbox.configure(state='normal',
                      text_color='white')
    textbox.grid(row=6, column=4, columnspan=4, rowspan=15, sticky='nwe', padx=10)

    # Create button generating shopping list
    generate_shopping_list_button = tk.CTkButton(root, 
                                                text="Generate shopping list", 
                                                command=lambda: generate_results_event(data=DATA, 
                                                                                       option_menu_objects=option_menu_objects, 
                                                                                       to_excel=False,
                                                                                       textbox=textbox),
                                                corner_radius=0                                       )
    generate_shopping_list_button.grid(row=5, column=4, columnspan=4, padx=10, sticky='wes')

    # 'Save to excel' button
    save_to_excel_button = tk.CTkButton(root, 
                                        text="Save to Excel",
                                        command= lambda: generate_results_event(data=DATA, 
                                                                                option_menu_objects=option_menu_objects, 
                                                                                to_excel=True))
    save_to_excel_button.grid(row=6, column=0, padx=10, sticky='nw')

    

    root.mainloop()