import yaml

def parse_tml_file(tml_content):
    try:
        tml_data = yaml.safe_load(tml_content)
        # Extract relevant information from the TML data
        parsed_data = {
            "table_name": tml_data.get("table", {}).get("name", ""),
            "columns": [col.get("name") for col in tml_data.get("table", {}).get("columns", [])],
            "joins": [join.get("name") for join in tml_data.get("table", {}).get("joins", [])]
        }
        return parsed_data
    except yaml.YAMLError as e:
        print(f"Error parsing TML: {e}")
        return None