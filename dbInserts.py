import sqlite3

# Function to execute SQL script line by line
def execute_sql_script(script_path):
    conn = sqlite3.connect('exhibition.db')
    c = conn.cursor()

    # Read SQL script from file
    with open(script_path, 'r') as file:
        lines = file.readlines()

    # Execute SQL script line by line
    for line_number, line in enumerate(lines, start=1):
        try:
            c.execute(line)
        except sqlite3.Error as e:
            print(f"Error executing script at line {line_number}: {e}")
            conn.rollback()
            break  # Stop execution on error
    else:
        conn.commit()
        print("Script executed successfully.")

    conn.close()

# Path to the SQL script file
script_path = 'dbinsert.sql'

# Execute SQL script line by line
execute_sql_script(script_path)
