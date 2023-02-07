# IMPORTS
import sqlite3

# DATABASE
db_path = "data/ebookstore"

records = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
]


def initialise(db_path, records):
    try:
        db = sqlite3.connect(db_path)
        cursor = db.cursor()  # Get a cursor object

        cursor.execute(
            "CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)"
        )
        db.commit()
        cursor.executemany(
            "INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)",
            records,
        )
        db.commit()
    finally:
        return db, cursor


def add_book(cursor, db, record):
    # record consists of (id, Title, Author, Qty)
    cursor.execute(f"INSERT INTO books(id, Title, Author, Qty) VALUES{record}")
    db.commit()


def delete_book(cursor, db, id):
    cursor.execute(f"DELETE FROM books WHERE id = {id}")

    db.commit()


def search_books(cursor, query):
    cursor.execute(
        f"SELECT * FROM books WHERE id LIKE '%{query}%' OR Title LIKE '%{query}%' OR Author LIKE '%{query}%'"
    )
    for book in cursor.fetchall():
        print(
            f'    id: {book[0]}    Title: "{book[1]}"    Author: "{book[2]}"    Quantity: {book[3]}'
        )


def update_book(cursor, db, id, parameter, new_value):
    cursor.execute(f"UPDATE books SET {parameter} = '{new_value}' WHERE id = {id} ")
    db.commit()


def show_all_books(cursor):
    cursor.execute("SELECT * FROM books")
    for book in cursor.fetchall():
        print(
            f'    id: {book[0]}    Title: "{book[1]}"    Author: "{book[2]}"    Quantity: {book[3]}'
        )


def shutdown(cursor, db):
    cursor.execute("DROP TABLE books")
    print("books table deleted")

    db.commit()
    db.close()
    print("Connection to database closed")


# MENU
menu = """
1. Enter book
2. Update book
3. Delete book
4. Search books
5. Show All books
0. Exit
"""


def main():
    # Display menu, respond to inputs
    # Handle exceptions gracefully
    try:
        db, cursor = initialise(db_path, records)
    except Exception as e:
        # Not certain this does anything
        print(e)
        db.rollback()
        db, cursor = initialise(db_path, records)

    running = True
    while running:
        try:
            user_input = int(input(menu)[0])
            match user_input:
                case 0:
                    # Allows loop to end, which then calls shutdown()
                    running = False
                case 1:
                    new_record = (
                        input("Enter new book's id: "),
                        input("Enter new book's title: "),
                        input("Enter new book's author: "),
                        input("Input quantity of new book: "),
                    )
                    add_book(cursor, db, record=new_record)
                case 2:
                    update_id = input("Enter the id of the book to update: ")
                    update_parameter = input(
                        "Which parameter would you like to update? [id, Title, Author, Qty]: "
                    )
                    new_value = input(
                        "What should the new value for this parameter be? "
                    )
                    update_book(cursor, db, update_id, update_parameter, new_value)
                case 3:
                    delete_id = input("Enter the id of the book to delete: ")
                    delete_book(cursor, db, id=delete_id)
                case 4:
                    search_query = input("Enter search term: ")
                    search_books(cursor, query=search_query)
                case 5:
                    show_all_books(cursor)
        except Exception as e:
            print(f"Error occurred: {e}")
    shutdown(cursor, db)


if __name__ == "__main__":
    main()
