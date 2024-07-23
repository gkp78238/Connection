import yaml

def json_to_tml(json_data):
    if isinstance(json_data, list):
        json_data = json_data[0] if json_data else {}

    tml_data = {
        'guid': json_data.get('guid', 'default_guid'),
        'table': {}
    }

    table_data = json_data.get('table', {})
    tml_data['table'] = {
        'name': table_data.get('name', ''),
        'db': table_data.get('db', ''),
        'schema': table_data.get('schema', ''),
        'db_table': table_data.get('db_table', ''),
        'connection': {
            'name': table_data.get('connection', {}).get('name', '')
        },
        'columns': [],
        'joins_with': []
    }

    for column in table_data.get('columns', []):
        tml_column = {
            'name': column.get('name', ''),
            'db_column_name': column.get('db_column_name', ''),
            'properties': column.get('properties', {}),
            'db_column_properties': column.get('db_column_properties', {})
        }
        tml_data['table']['columns'].append(tml_column)

    for join in table_data.get('joins_with', []):
        tml_join = {
            'name': join.get('name', ''),
            'destination': {
                'name': join.get('destination', {}).get('name', '')
            },
            'on': join.get('on', ''),
            'type': join.get('type', '')
        }
        tml_data['table']['joins_with'].append(tml_join)

    tml_string = yaml.dump(tml_data, default_flow_style=False, sort_keys=False)
    return tml_string
