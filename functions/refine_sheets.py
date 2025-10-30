from consts_vars import other_consts as oc
from gspread_formatting import CellFormat, NumberFormat, format_cell_range
import gspread


def M_categorize_googleSheets(sheets_names, spreadsheet, categories_sheets):
    numbers_comment_list = get_all_active_sheet_data(sheets_names, spreadsheet)

    sort_data_using_comments(categories_sheets, numbers_comment_list, spreadsheet)

    set_textFormat_PlainText_googleSheets(spreadsheet)
    

def set_textFormat_PlainText_googleSheets(spreadsheet):
    plain_text_format = CellFormat(
        numberFormat=NumberFormat(type='TEXT', pattern='')  # pattern must be set
    )

    # Loop through each sheet and format as Plain Text
    worksheet = spreadsheet.worksheet(oc.get_sheet_unextracted_page_name())
    rows = worksheet.row_count
    cols = worksheet.col_count
    range_str = f"A1:{gspread.utils.rowcol_to_a1(rows, cols)}"

    # Apply Plain Text formatting to the range
    format_cell_range(worksheet, range_str, plain_text_format)


#gets a list that has all the numbers from a category from sheets(NSA,FLIP,etc) & returns a list with 2 values ready to be inserted to sheets
def format_for_sheets_filteringData(list0):  
    temp_list=[]
    for item in list0:
        temp_list.append([item[0],item[1]])
    return temp_list


def write_to_sheet(sheet_name, data,spreadsheet):
    worksheet = spreadsheet.worksheet(sheet_name)
    
    # Clear the worksheet before writing (optional, for clean overwrite)
    worksheet.clear()

    # Update the worksheet starting from cell A1
    worksheet.update(range_name='A1', values=data)


def input_numbers_to_category(sheet_name,list0,spreadsheet):
    temp_list=[]
    temp_list = format_for_sheets_filteringData(list0)
    write_to_sheet(sheet_name,temp_list,spreadsheet)


#gets names of sheets categories & all phone-comments and updates the sheets categories
def sort_data_using_comments(G_categories_sheets,numbers_comment_list,spreadsheet):
    counter_tick = 100/len(G_categories_sheets)
    counter_curr = 0
    print("\t\t+-----+")
    for category in G_categories_sheets:
        temp_list = []
        
        if(category!="OTHER"):
            temp_rest_of_list = []
            for number_comment in numbers_comment_list:
                
                    if(category in number_comment[1]):
                        temp_list.append(number_comment)
                    else:
                        temp_rest_of_list.append(number_comment)
            numbers_comment_list = temp_rest_of_list
        else:
            temp_list = numbers_comment_list
            
        
        write_to_sheet(category,temp_list,spreadsheet)
        counter_curr+=counter_tick
        if(round(counter_curr)<100):
            print(f"\t\t+  {round(counter_curr)} +")
        else:
            print(f"\t\t+ {round(counter_curr)} +")

    print("\t\t+-----+")
    print("\n")


def get_all_active_sheet_data(sheet_name_list,spreadsheet):
    print("\n")
    print(f"\t+ Getting Sheets Data +")
    
    data_list = []
    for current_worksheet_data_list_name in sheet_name_list:
        worksheet = spreadsheet.worksheet(current_worksheet_data_list_name)
        current_worksheet_data_list = worksheet.get_all_values()
        for item in current_worksheet_data_list:
            if item[1].strip()!="":
                data_list.append([item[0],item[1]])
    print(f"\t+      Data Saved     +")
    print("\n")
    return data_list
