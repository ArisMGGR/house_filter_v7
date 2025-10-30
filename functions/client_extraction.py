import re


def M_FilterClients_googlesheets(spreadsheet,sheet_unextracted_page_name,sheet_extracted_page_name):
    # Get (name, phone) pairs
    name_phone_pairs = get_name_phone_pairs(spreadsheet,sheet_unextracted_page_name)
    

    extracted_name_phone_pairs = delete_characters_at_start_of_string(name_phone_pairs)
    

    phone_list_single,phone_list_nonsingle = split_numbers_initial(extracted_name_phone_pairs)
    
            
    phone_list_nonsingle,phone_list_single = string_remover(phone_list_nonsingle,phone_list_single)


    # Filter by valid length
    phone_list_nonsingle,phone_list_single = filter_numeric_values(phone_list_nonsingle,phone_list_single)

    
    # Remove duplicates in rows
    phone_list_nonsingle,phone_list_single = remove_duplicates_in_rows(phone_list_nonsingle,phone_list_single)

    
    # Move Greek numbers first
    phone_list_nonsingle = move_greek_number_first(phone_list_nonsingle)


    # Manual user selection if multiple numbers per row
    phone_list_single = manual_user_filtering(phone_list_nonsingle,phone_list_single)

    # Prepend '30' to Greek numbers
    finalized_number_list = prepend_30_greek_numbers(phone_list_single)

    
    F_print_append_results_Filtering(finalized_number_list,spreadsheet,sheet_extracted_page_name)


#Splits the numbers text by "-", " ", ","
def split_numbers_initial(extracted_name_phone_pairs):
    phone_list_refined = []
    phone_list_single = []
    phone_list_nonsingle = []


    for name, phone in extracted_name_phone_pairs:
            if ',' in phone:
                phone_split = phone.split(",")
                phone_list_refined.append((name, phone_split))
            elif '-' in phone:
                phone_split = phone.split("-")
                phone_list_refined.append((name, phone_split))
            elif ' ' in phone:
                phone_split = phone.split(" ")
                phone_list_refined.append((name, phone_split))
            else:
                phone_list_refined.append((name, phone))

        

    for name, phone in phone_list_refined:
        if not isinstance(phone, list):
            phone_list_single.append((name, phone))
        else:
            phone_list_nonsingle.append((name, phone))

    return phone_list_single,phone_list_nonsingle


def delete_characters_at_start_of_string(temp_list):
    new_list = []
    for name, phone in temp_list:
        # Keep removing first character until it's a digit
        while phone and not phone[0].isdigit():
            phone = phone[1:]  # remove the first character
        new_list.append([name,phone])
    return new_list


# Remove non-numeric
def string_remover(phone_list_nonsingle,phone_list_single):
    cleaned_phone_list = []
    for name, phone in phone_list_nonsingle:
        cleaned = []
        unclean = []
        for item in phone:
            item_stripped = item.strip()
            if item_stripped.isdigit():
                cleaned.append(item_stripped)
            else:
                unclean.append(item_stripped)
        cleaned = final_string_cleanup(cleaned,unclean)
        if cleaned:
            cleaned_phone_list.append((name, cleaned))

    temp = []
    for name, phone in cleaned_phone_list:
        if len(phone) == 1:
            phone_list_single.append((name, phone[0]))
        else:
            temp.append((name, phone))
    phone_list_nonsingle = temp
    
    return phone_list_nonsingle,phone_list_single


def final_string_cleanup(cleaned,unclean):
    new_clean = []
    for phone in unclean:
        new_clean.append(''.join(re.findall(r'\d+', phone)))
    for item in cleaned:
        new_clean.append(item)
    return new_clean


def filter_numeric_values(phone_list_nonsingle,phone_list_single):
    filtered_data = []
    
    for name, sublist in phone_list_nonsingle:
        filtered_sublist = [num for num in sublist if 7 <= len(num) <= 15]
        filtered_data.append((name, filtered_sublist))

    temp = []
    for name, phone in filtered_data:
        if len(phone) == 1:
            phone_list_single.append((name, phone[0]))
        else:
            temp.append((name, phone))
    phone_list_nonsingle = temp

    
    return phone_list_nonsingle,phone_list_single


def remove_duplicates_in_rows(phone_list_nonsingle,phone_list_single):
    result = []
    for name, sublist in phone_list_nonsingle:
        seen = set()
        filtered_sublist = []
        for num in sublist:
            if num not in seen:
                seen.add(num)
                filtered_sublist.append(num)
        result.append((name, filtered_sublist))

    temp = []
    for name, phone in result:
        if len(phone) == 1:
            phone_list_single.append((name, phone[0]))
        else:
            temp.append((name, phone))
    phone_list_nonsingle = temp


    return phone_list_nonsingle,phone_list_single


def move_greek_number_first(data):
    for i in range(len(data)):
        name, row = data[i]
        index = next((i for i, num in enumerate(row) if num.startswith("69") or num.startswith("3069")), None)
        if index is not None and index != 0:
            greek_num = row.pop(index)
            row.insert(0, greek_num)
        data[i] = (name, row)
    return data


# Get (name, phone) pairs
def get_name_phone_pairs(spreadsheet,sheet_unextracted_page_name):
    worksheet = spreadsheet.worksheet(sheet_unextracted_page_name)
    sheets_data = worksheet.get_all_values() 
    name_phone_pairs = [(row[1], row[2]) for row in sheets_data if len(row) >= 3]
    return name_phone_pairs


# Manual user selection if multiple numbers per row
def manual_user_filtering(phone_list_nonsingle,phone_list_single):
    user_number_pick = ""
    while user_number_pick != "y":
        print("+---------------------------------------------------------------+")
        for i, (name, row) in enumerate(phone_list_nonsingle):
            print(i, name, "->", row)
        print("+---------------------------------------------------------------+")
        user_number_pick = input("Continue? (enter number or 'y' to stop): ").strip()
        if user_number_pick == "y":
            break
        found = False
        for i, (name, row) in enumerate(phone_list_nonsingle):
            if user_number_pick in row:
                phone_list_nonsingle[i] = (name, [user_number_pick])
                print(f"Number {user_number_pick} saved and row truncated.")
                found = True
                break
        if not found:
            print("Number not found in the data. Please try again.")

    for name, row in phone_list_nonsingle:
        phone_list_single.append((name, row[0]))

    return phone_list_single


# Prepend '30' to Greek numbers
def prepend_30_greek_numbers(phone_list_single):
    """
    Adds '30' in front of Greek mobile numbers (those starting with '69') 
    in a list of (name, phone) pairs.
    """
    result = []
    for name, number in phone_list_single:
        if number.startswith("69"):
            number = "30" + number
        result.append((name, number))
    return result


def F_print_append_results_Filtering(finalized_number_list,spreadsheet,sheet_extracted_page_name):

    if(len(finalized_number_list)<100):
        print("\n")
        print("\t+------------------------------+")
        print(f"\t+  Total numbers: {len(finalized_number_list)}           +")
        print("\t+  Numbers Uploaded To sheets  +")
        print("\t+------------------------------+")
        print("\n")
    if(len(finalized_number_list)>=100):
        print("\n")
        print("\t+------------------------------+")
        print(f"\t+  Total numbers: {len(finalized_number_list)}          +")
        print("\t+  Numbers Uploaded To sheets  +")
        print("\t+------------------------------+")
        print("\n")

    #worksheet = spreadsheet.worksheet("current_clients_filtered")
    worksheet = spreadsheet.worksheet(sheet_extracted_page_name)
    worksheet.clear()
    worksheet.update(values=[[number, name] for name, number in finalized_number_list], range_name='A1')
