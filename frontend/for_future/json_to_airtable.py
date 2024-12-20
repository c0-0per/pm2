import requests
import json

# Airtable setup
AIRTABLE_API_KEY = 'patwN5zs8PvYco1aq.5186adce2a05f585419a30f20ed42c0ba9b0bf10aba6d8b19b8e46221890500e'
AIRTABLE_BASE_ID = 'appuToHM0Lp9zrj9C'

def add_row_to_airtable(row, table_name):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"fields": row}, headers=headers)
    return response.json()

def update_row_in_airtable(record_id, row, table_name):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}/{record_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.patch(url, json={"fields": row}, headers=headers)
    return response.json()

def create_rows_in_airtable(data, name_to_id_dict, column_name, json_attribute_name, table_name, json_name):
    updated = False  
    for source in data:
        record_id = source.get("record_id", "")
        if record_id == "":
            new_row = {
                column_name: source.get(json_attribute_name)
            }
            airtable_response = add_row_to_airtable(new_row, table_name)
            # Check for errors
            if 'error' in airtable_response:
                print(f"Error adding {new_row[column_name]} to Airtable: {airtable_response['error']}")
            else:
                new_record_id = airtable_response.get('id')
                print(f"Successfully added {new_row[column_name]} to Airtable with record_id {new_record_id}.")
                source['record_id'] = new_record_id
                name_to_id_dict[source.get(json_attribute_name)] = new_record_id
                updated = True

    if updated:
        with open(json_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        with open('json_utils/names_to_record_id.json', 'w', encoding='utf-8') as f:
            json.dump(name_to_id_dict, f, indent=2)

def new_startup_from_country():
    pass

def new_tracking_report_from_country():
    pass

def new_data_source_from_country():
    pass

def new_country_from_data_source():
    pass

def new_tracking_report_from_data_source():
    pass

def new_startup_from_data_source():
    pass

def new_startup_from_investor():
    pass

def new_startup_from_investor():
    pass

def new_startup_from_investor():
    pass

def new_data_source_from_startup():
    pass

def new_investor_from_startup():
    pass

def new_tracking_report_from_startup():
    pass

def new_startup_from_tracking_report():
    pass

def new_country_from_tracking_report():
    pass



def convert_array_elements_to_record_ids(array, name_to_id_dict):
    new_array = []
    for element in array:
        new_array.append(name_to_id_dict[element])
    return new_array

def convert_name_to_record_id(name, name_to_id_dict):
    if name != "":
        return name_to_id_dict[name]
    else:
        return None

def get_startup_info_from_json(data, name_to_id_dict):
    info = {
        "Startup Name": data.get("startup_name"),
        "Industry": data.get("industry"),
        "Founders": data.get("founders"),
        "Amount Raised": data.get("amount_raised"),
        "Tags": data.get("tags"),
        "Website": data.get("website"),
        "Country": convert_array_elements_to_record_ids(data.get("country"), name_to_id_dict),
        "Data Sources": convert_array_elements_to_record_ids(data.get("data_sources"), name_to_id_dict),
        "Investors": convert_array_elements_to_record_ids(data.get("investors"), name_to_id_dict),
        "Tracking Reports": convert_array_elements_to_record_ids(data.get("tracking_reports"), name_to_id_dict),
    }

    date_of_funding = data.get("date_of_funding")
    if date_of_funding != '':
        info["Date of Funding"] = date_of_funding

    founded_date = data.get("founded_date")
    if founded_date != '':
        info["Founded Date"] = founded_date

    last_updated = data.get("last_updated")
    if last_updated != '':
        info["Last Updated"] = last_updated

    return info

def get_tracking_report_info_from_json(data, name_to_id_dict):
    info = {
        "Report ID": data.get("report_id"),
        "Data Source": convert_array_elements_to_record_ids(data.get("data_source"), name_to_id_dict),
        "Summary": data.get("summary"),
        "Startups Covered": convert_array_elements_to_record_ids(data.get("startups_covered"), name_to_id_dict),
        "Countries Covered": convert_array_elements_to_record_ids(data.get("countries"), name_to_id_dict),
        "Generated By": data.get("generated_by")
    }

    report_date = data.get("report_date")
    if report_date != '':
        info["Report Date"] = report_date
    return info

def get_country_info_from_json(data, name_to_id_dict):
    info = {
        "Country": data.get("country"),
        "Number of Startups": len(data.get("startups")),
        "Primary Language": data.get("primary_language"),
        "Currency Used": data.get("currency_used"),
        "Startups in Country": convert_array_elements_to_record_ids(data.get("startups"), name_to_id_dict),
        "Tracking Reports": convert_array_elements_to_record_ids(data.get("tracking_reports"), name_to_id_dict),
        "Data Sources": convert_array_elements_to_record_ids(data.get("data_sources"), name_to_id_dict)
    }
    return info

def get_data_source_info_from_json(data, name_to_id_dict):
    info = {
        "Source Name": data.get("source_name"),
        "Source URL": data.get("source_url"),
        "Data Type": data.get("data_type"),
        "Collection Frequency": data.get("collection_frequency"),
        "Associated Countries": convert_array_elements_to_record_ids(data.get("associated_countries"), name_to_id_dict),
        "Related Tracking Reports": convert_array_elements_to_record_ids(data.get("related_tracking_reports"), name_to_id_dict),
        "Startups": convert_array_elements_to_record_ids(data.get("startups"), name_to_id_dict)
    }

    last_updated = data.get("last_updated")
    if last_updated != '':
        info["Last Updated"] = last_updated
    return info

def get_investor_info_from_json(data, name_to_id_dict):
    info = {
        "Investor Name": data.get("investor_name"),
        "Investor Type": data.get("investor_type"),
        "Investment Amount": data.get("investment_amount"),
        "Contact Information": data.get("countact_information"),
        "Associated Startups": convert_array_elements_to_record_ids(data.get("associated_startups"), name_to_id_dict)
    }
    return info

def adding_info_to_rows_in_airtable(data, name_to_id_dict, table_name, info_getter_function):
    for source in data:
        record_id = source.get("record_id")
        updated_row = info_getter_function(source, name_to_id_dict)
        airtable_response = update_row_in_airtable(record_id, updated_row, table_name)
        if 'error' in airtable_response:
            print(f"Error adding {updated_row} to Airtable: {airtable_response['error']}")
        else:
            print(f"Successfully updated {updated_row}")

def creating_new_rows():
    with open('json_utils/names_to_record_id.json', 'r', encoding='utf-8') as f:
        name_to_id_dict = json.load(f)
    with open('json_files/data_sources.json', 'r', encoding='utf-8') as f:
        data_sources = json.load(f)
    with open('json_files/startups.json', 'r', encoding='utf-8') as f:
        startups = json.load(f)
    with open('json_files/countries.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    with open('json_files/tracking_reports.json', 'r', encoding='utf-8') as f:
        tracking_reports = json.load(f)
    with open('json_files/investors.json', 'r', encoding='utf-8') as f:
        investors = json.load(f)

    create_rows_in_airtable(tracking_reports, name_to_id_dict, "Report ID", "report_id", "Tracking Reports", "json_files/tracking_reports.json")
    create_rows_in_airtable(startups, name_to_id_dict, "Startup Name", "startup_name", "Startups", "json_files/startups.json")
    create_rows_in_airtable(investors, name_to_id_dict, "Investor Name", "investor_name", "Investors", "json_files/investors.json")
    create_rows_in_airtable(data_sources, name_to_id_dict, "Source Name", "source_name", "Data Sources", "json_files/data_sources.json")
    create_rows_in_airtable(countries, name_to_id_dict, "Country", "country", "Countries", "json_files/countries.json")

def updating_information():
    with open('json_utils/names_to_record_id.json', 'r', encoding='utf-8') as f:
        name_to_id_dict = json.load(f)
    with open('json_files/data_sources.json', 'r', encoding='utf-8') as f:
        data_sources = json.load(f)
    with open('json_files/startups.json', 'r', encoding='utf-8') as f:
        startups = json.load(f)
    with open('json_files/countries.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    with open('json_files/tracking_reports.json', 'r', encoding='utf-8') as f:
        tracking_reports = json.load(f)
    with open('json_files/investors.json', 'r', encoding='utf-8') as f:
        investors = json.load(f)

    adding_info_to_rows_in_airtable(data_sources, name_to_id_dict, "Data Sources", get_data_source_info_from_json)
    adding_info_to_rows_in_airtable(startups, name_to_id_dict, "Startups", get_startup_info_from_json) 
    adding_info_to_rows_in_airtable(countries, name_to_id_dict, "Countries", get_country_info_from_json)
    adding_info_to_rows_in_airtable(tracking_reports, name_to_id_dict, "Tracking Reports", get_tracking_report_info_from_json)
    adding_info_to_rows_in_airtable(investors, name_to_id_dict, "Investors", get_investor_info_from_json)
   
if __name__ == "__main__":
    creating_new_rows()
    updating_information()