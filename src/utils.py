import datetime
import sqlite3

header_rule = {
    "Subject": "HappyFox",
    "From": "happyfox",
    "Date": "Less than 2 days"
}

def validate_header_rules(headers):
    '''
    Each rule has 3 properties
        - Field name (From / To / Subject / Date Received / etc)
        - Predicate ( contains / not equals / less than )
        - Value

        EX: Default date format - 'Wed, 21 Jun 2023 06:23:11 GMT'
    '''
    status = True
    date_format = "%a, %d %b %Y %H:%M:%S GMT"
    headers_to_validate = [i for i in headers if i['name'] in header_rule]
    # print([i['value'] for i in headers_to_validate])
    for d in headers_to_validate:
        val = d["value"]
        if d["name"] != "Date":
            if header_rule[d["name"]] not in val:
                status = False
                break
        else:
            df = date_format
            if "+0000 (UTC)" in val:
                df = date_format.replace("GMT", "+0000 (UTC)")
            date_obj = datetime.datetime.strptime(val, df)
            if date_obj < datetime.timedelta(days=-10) + datetime.datetime.utcnow():
                status = False
                break
    return status

def update_data_into_sql(filtered_gmail_data):
    try:
        conn = sqlite3.connect('gmail_data_store.db')
        cursor_obj = conn.cursor()
        # Creating table if not exists
        table = """ CREATE TABLE IF NOT EXISTS GMAIL_DATA_FILTER (
                    Subject VARCHAR(255) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    DateReceived VARCHAR(255) NOT NULL
                ); """
        cursor_obj.execute(table)
        for d in filtered_gmail_data:
            query = '''INSERT INTO GMAIL_DATA_FILTER VALUES ('%s', '%s', '%s')'''%(d[0], d[1].split("<")[-1].split(">")[0], d[2])
            cursor_obj.execute(query)
        print("Data Inserted in the table: ")
        data=cursor_obj.execute('''SELECT * FROM GMAIL_DATA_FILTER''')
        for row in data:
            print(row)
        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)





