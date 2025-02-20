"""
This python script generates SQL queries for updating different column values from different table at once.
Generate SQL query with right mappings

Usage:
    1. Modify data table as
        data = {
            "tablename1": {
                "columnname1": {
                    "previous_value1_in_column1": "new_value1_in_column1",
                    "previous_value2_in_column1": "new_value2_in_column1",
                    "previous_value3_in_column1": "new_value3_in_column1",
                },
                "columnname2": {
                    "previous_value1_in_column2": "new_value1_in_column2",
                    "previous_value2_in_column2": "new_value2_in_column2",
                    "previous_value3_in_column2": "new_value3_in_column2",
                },
            },
            "tablename2": {
                "columnname3": {
                    "previous_value1_in_column3": "new_value1_in_column3",
                    "previous_value2_in_column3": "new_value2_in_column3",
                    "previous_value3_in_column3": "new_value3_in_column3",
                },
                "columnname4": {
                    "previous_value1_in_column4": "new_value1_in_column4",
                    "previous_value2_in_column4": "new_value2_in_column4",
                    "previous_value3_in_column4": "new_value3_in_column4",
                },
            },
        }
    2. Run python script
    3. Use the printed SQL query
"""

data = {
    "my_schema.sentiments": {
        "licensability": {
            "Unlikely": "unlikely",
            "Very Unlikely": "veryunlikely",
            "Probably Likely": "likely",
            "Ununlikely": "likely",
            "Likelihood": "likely",
            "Likely": "likely",
            "Very Likely": "verylikely",
        },
        "sentiment": {
            "Negative": "negative",
            "strong negative": "negative",
            "mixed": "neutral",
            "Mixed": "neutral",
            "Neutral": "neutral",
            "neutr---": "neutral",
            "Positive": "positive",
        },
        "link_source": {
            "Parsed": "parsed",
            "HTML Extract": "parsed",
            "Generated by Context": "generated",
            "generated": "generated",
            "Generated": "generated",
            "Adweek": "other",
            "Derived": "other",
            "Not applicable": "other",
            "https://www.facebook.com/TheBennetGang/": "other",
            "Not Applicable": "other",
            "https://www.instagram.com/carol_starr/ ": "other",
            "NaN": "notfound",
            "Website Not Found": "notfound",
        },
    },
    "my_schema.brands": {
        "entity_type": {
            "Person": "person",
            "Company": "company",
            "Event": "event",
            "Government": "government",
            "Educational": "educational",
            "NGO": "ngo",
        },
    },
}


def generate_update_queries(data):
    queries = []

    # Iterate through each table in the dictionary
    for tablename, columns in data.items():
        for columnname, value_map in columns.items():
            # Generate update queries for mapped values
            for prev_value, new_value in value_map.items():
                query = f"""
                UPDATE {tablename}
                SET {columnname} = '{new_value}'
                WHERE {columnname} = '{prev_value}';
                """
                queries.append(query.strip())

            # Generate query to set 'other' for values not in the mapping and not NULL
            not_in_mapping_values = "', '".join(set(value_map.values()))
            other_values_query = f"""
            UPDATE {tablename}
            SET {columnname} = 'other'
            WHERE {columnname} NOT IN ('{not_in_mapping_values}')
            AND {columnname} IS NOT NULL;
            """
            queries.append(other_values_query.strip())
    return queries


# Generate SQL queries
queries = generate_update_queries(data)

# Print all generated SQL queries
for query in queries:
    # The printed SQL query can now be used in our db
    print(query)
