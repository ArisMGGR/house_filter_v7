import gspread
from google.oauth2.service_account import Credentials
from functions import refine_sheets as rs
from functions import client_extraction as ce
from functions import final_filtering as ff
from consts_vars import sensitive_consts as sc
from consts_vars import googlesheets_permissions as gp
from consts_vars import other_consts as oc
import sys

#--------------FUNCTIONS--------------------------------------------------#

def connect_to_sheets(sheet_filename):
    SERVICE_ACCOUNT_FILE = sc.get_service_account_file_name()

    # Define the scopes
    SCOPES = gp.get_scopes()
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(sheet_filename)
    return spreadsheet

def argv_user_input():
    if len(sys.argv) > 1:  
        user_input1 = sys.argv[1]
    else:
        user_input1 = ""
    return user_input1

def initial_menu(user_input1):
    if check_user_pick(user_input1,1) or check_user_pick(user_input1,2) or check_user_pick(user_input1,3) or check_user_pick(user_input1,0):
        return user_input1
    while not check_user_pick(user_input1,1) and not check_user_pick(user_input1,2) and not check_user_pick(user_input1,3) and not check_user_pick(user_input1,0):
        print("\n\t+--------------------------------+")
        print("\t+  1 -> Initial Filtering        +     <-takes initial data (current clients) and filters them - puts them in client filtered")
        print("\t+  2 -> Categorize numbers       +     <-")
        print("\t+  3 -> Create Excell            +")    
        print("\t+  0 -> exit                     +")
        print("\t+--------------------------------+\n")
        user_input1 = input("\t")

    return user_input1

def check_user_pick(user_input1,option):
    user_pick_exists = False
    if(option==1):
        filterClients_googlesheets_Options = oc.get_filterClients_googlesheets_Options()
        for i in filterClients_googlesheets_Options:
            if(i==user_input1):
                user_pick_exists = True
    if(option==2):
        categorize_googleSheets_Options = oc.get_categorize_googleSheets_Options()
        for i in categorize_googleSheets_Options:
            if(i==user_input1):
                user_pick_exists = True
    if(option==3):
        create_excell_Options = oc.get_create_excell_Options()
        for i in create_excell_Options:
            if(i==user_input1):
                user_pick_exists = True
    if(option==0):
        call_all_Options = oc.get_call_all_Options()
        for i in call_all_Options:
            if(i==user_input1):
                user_pick_exists = True
    
    return user_pick_exists
    
    

    

    


#--------------GLOBAL--------------------------------------------------#

G_sheets_names = oc.get_sheets_names()
G_categories_sheets = oc.get_categories_sheets()
G_sheet_file_name = oc.get_sheet_file_name()
G_sheet_unextracted_page_name = oc.get_sheet_unextracted_page_name()
G_sheet_extracted_page_name = oc.get_sheet_extracted_page_name()



#--------------START OF PROGRAM-------------------------------------------#

user_input1 = argv_user_input()

    
user_input1 = initial_menu(user_input1)


spreadsheet = connect_to_sheets(G_sheet_file_name)


if check_user_pick(user_input1,1):
    ce.M_FilterClients_googlesheets(spreadsheet,G_sheet_unextracted_page_name,G_sheet_extracted_page_name)

elif(check_user_pick(user_input1,2)):
   rs.M_categorize_googleSheets(G_sheets_names,spreadsheet,G_categories_sheets)
    
elif(check_user_pick(user_input1,3)):
    ff.M_create_excell(spreadsheet,G_sheet_extracted_page_name,G_categories_sheets)

elif(check_user_pick(user_input1,0)):
    rs.M_categorize_googleSheets(G_sheets_names,spreadsheet,G_categories_sheets)

    ce.M_FilterClients_googlesheets(spreadsheet,G_sheet_unextracted_page_name,G_sheet_extracted_page_name)
    
    ff.M_create_excell(spreadsheet,G_sheet_extracted_page_name,G_categories_sheets)