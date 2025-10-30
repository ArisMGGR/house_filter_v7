sheets_names = ["msg_already_sent","5million+","KTIRIA_eos_5m","0-150k","150k-300k","300k-500k","500k-1m","Oikopeda_mexri_500k","epaggelmatika_genika"]
categories_sheets = ["NBH","GVB","GVT","FLIP","IND"] 

sheet_unextracted_page_name = "current_clients_unextracted"
sheet_extracted_page_name = "current_clients_extracted"

sheet_file_name = "DATA OF CLIENTS"

filterClients_googlesheets_Options = ["filter","1"]
categorize_googleSheets_Options = ["categorize","2"]
create_excell_Options = ["create","3"]
call_all_Options = ["combos","0"]

#NEEDED FOR G_categories_sheets SETUP
categories_sheets.insert(0, "NSA")
categories_sheets.append("OTHER")



def get_sheets_names():
    return sheets_names

def get_categories_sheets():
    return categories_sheets

def get_sheet_file_name():
    return sheet_file_name

def get_sheet_unextracted_page_name():
    return sheet_unextracted_page_name

def get_sheet_extracted_page_name():
    return sheet_extracted_page_name

def get_filterClients_googlesheets_Options():
    return filterClients_googlesheets_Options

def get_categorize_googleSheets_Options():
    return categorize_googleSheets_Options

def get_create_excell_Options():
    return create_excell_Options

def get_call_all_Options():
    return call_all_Options
