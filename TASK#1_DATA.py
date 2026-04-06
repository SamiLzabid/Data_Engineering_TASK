import re
import json
import mysql.connector


def convert_to_ValidJSON(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    valid_json_str = re.sub(r':(\w+)\s*=>', r'"\1":', raw_content)

    data = json.loads(valid_json_str)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully created valid JSON file: {output_path}")
    return data


def ingest_to_database(data, host="localhost", user="your_username", password="your_password", db_name="your_database"):

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id BIGINT UNSIGNED PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            genre VARCHAR(100),
            publisher VARCHAR(255),
            year INT,
            price VARCHAR(50)
        )
    ''')

    insert_query = '''
        REPLACE INTO books (id, title, author, genre, publisher, year, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    tuples_data = [
        (
            item.get('id'),   
            item.get('title'),
            item.get('author'),
            item.get('genre'),
            item.get('publisher'),
            item.get('year'),
            item.get('price')
        )
        for item in data
    ]

    cursor.executemany(insert_query, tuples_data)
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully ingested {len(data)} records into the MySQL database '{db_name}'!")
    
if __name__ == "__main__":
    input_file = "D:\\Source code\\WEBSITE\\task1_d.json"
    output_file = "D:\\Source code\\WEBSITE\\task1_d_valid.json"
    extracted_data =  convert_to_ValidJSON(input_file, output_file)
    
    ingest_to_database(
        data=extracted_data,
        host="localhost",
        user="root",             
        password="Root_007",    
        db_name="data_engineering"     
    )