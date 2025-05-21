import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)

#cursor object to run SQL commands
cursor = conn.cursor()

#while loop(will ask user to exit)
while True:
    search_term = input("\nEnter a ticker or keyword to search (or type 'exit' to quit): ")

    #break the loop
    if search_term.lower() == "exit":
        print("You have exited successfully!")
        break

    try:
        #SQL query to search for rows where the ticker or headline contains the keyword
        query = """
        SELECT ticker, headline
        FROM headlines
        WHERE ticker LIKE %s OR headline LIKE %s
        """
        # These values will be substituted into the query
        values = (f"%{search_term}%", f"%{search_term}%")

        # Execute the query with the user's input
        cursor.execute(query, values)
        results = cursor.fetchall()

        #Display the matches
        print(f"\n Found {len(results)} matching headlines:\n")
        for row in results:
            print(f"[{row[0]}] {row[1]}") # row[0] is the ticker, row[1] is the headline

    #This handles any MySQL errors that I was dealing with
    except mysql.connector.Error as e:
        print(f" MySQL Error: {e}")
        continue

# Close connections 
cursor.close()
conn.close()
