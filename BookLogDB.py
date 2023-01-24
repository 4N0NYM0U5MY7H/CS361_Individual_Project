# Author: August Frisk
# GitHub username: @4N0NYM0U5MY7H
# Date: 2023, January 23
# Description: This class represents the database for the
#              CS 361 Book Log program.

import re
import sqlite3
from contextlib import closing


class BookLogDB:
    """Represents a Book Log Database object."""
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(BookLogDB)
            return cls.instance
        return cls.instance

    def __init__(self):
        self._sqlite_file = "book_log.db"
        self._connection = self.create_connection()
        self.create_table()

    def create_connection(self):
        """Establishes a connection to the database."""
        try:
            return sqlite3.connect(self._sqlite_file)
        except sqlite3.Error as error:
            print(f"create_connection: {error}")

    def __del__(self):
        """Closes a connection to the database."""
        try:
            self._connection.close()
        except sqlite3.Error as error:
            print(f"__del__: {error}")

    def create_table(self):
        """Creates a table if it does not exist."""
        sql_string = """CREATE TABLE IF NOT EXISTS books(
                        book_id INTEGER PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        author VARCHAR(100) NOT NULL,
                        date VARCHAR(10))"""
        try:
            with closing(self._connection) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(sql_string)
        except sqlite3.Error as error:
            print(f"create_table: {error}")

    def add_new_record(self):
        """Adds a new record to the database."""
        book_title = self.prompt_user_for_book_title()
        author_name = self.prompt_user_for_author_name()
        date_completed = self.prompt_user_for_date_completed()
        sql_string = """INSERT INTO books(title, author, date)
                        VALUES (?,?,?)"""
        try:
            with closing(self.create_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(sql_string, (book_title, author_name, date_completed))
                connection.commit()
            success_string = f"{book_title} by {author_name} completed on {date_completed}."
            print(f"Book successfully added!\n{success_string}")
        except sqlite3.Error as error:
            print(f"add_new_record: {error}")

    def delete_a_record(self):
        """Deletes a record from the database."""
        print("Enter a Book ID to delete.")
        print("Input a number and press ENTER to select an option.")
        while True:
            try:
                user_input = int(input("Your input: "))
            except ValueError:
                continue
            else:
                break
        sql_select_string = """SELECT * FROM books WHERE book_id = ?"""
        sql_delete_string = """DELETE FROM books WHERE book_id = ?"""
        try:
            with closing(self.create_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    query = cursor.execute(sql_select_string, (user_input,))
                    query_string = query.fetchone()
                    if query_string:
                        print("Are you sure you want to delete this from your records?")
                        print(query_string)
                        while True:
                            print("Type 'yes' to continue or press ENTER to cancel.")
                            continue_prompt = input("Your input: ")
                            if continue_prompt.lower() == "yes":
                                cursor.execute(sql_delete_string, (user_input,))
                                print("Book successfully deleted!")
                                connection.commit()
                                break
                            else:
                                print("Canceling delete Request.")
                                break
                    else:
                        print(f"No records found with Book ID {user_input}.")
        except sqlite3.Error as error:
            print(f"delete_a_record: {error}")

    def view_all_records(self):
        """Displays all records in the database."""
        sql_string = """SELECT * FROM books ORDER BY title DESC"""
        try:
            with closing(self.create_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    query = cursor.execute(sql_string).fetchall()
                    results = ""
                    for row in query:
                        results += f"{row}\n"
            return results
        except sqlite3.Error as error:
            print(f"view_all_records: {error}")

    def prompt_user_for_book_title(self):
        """Prompt the user to enter the title of a book."""
        while True:
            print("Enter a Book Title.\n" +
                  "Must only use A(a)-Z(z). Can include spaces.\n" +
                  "Must be less than 200 characters.")
            book_title = input("Book Title: ").title()
            if re.search("^[a-zA-Z\s]+$", book_title):
                if len(book_title) < 201:
                    break
        return book_title

    def prompt_user_for_author_name(self):
        """Prompt the user to enter the author of a book."""
        while True:
            print("Enter an Author's name.\n" +
                  "Must only use A(a)-Z(z). Can include spaces.\n" +
                  "Must be less than 100 characters.")
            author_name = input("Author Name: ").title()
            if re.search("^[a-zA-Z\s]+$", author_name):
                if len(author_name) < 100:
                    break
        return author_name

    def prompt_user_for_date_completed(self):
        """Prompt the user to enter the date a book was completed."""
        while True:
            print("Enter a date the book was completed.\n"
                  + "Must be in the following format: MM/DD/YYYY.")
            date_completed = input("Date Completed: ")
            if re.match("(\d{2})[/](\d{2})[/](\d{4})$", date_completed):
                break
        return date_completed

    def search_by_title(self):
        """Search for a record by Book Title."""
        book_title = self.prompt_user_for_book_title()
        sql_string = """SELECT * FROM books WHERE title = ?"""
        try:
            with closing(self.create_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    query = cursor.execute(sql_string, (book_title,)).fetchall()
                    results = ""
                    if query:
                        for row in query:
                            results += f"{row}\n"
                        return results
                    else:
                        return f"No results found with the Book Title {book_title}"
        except sqlite3.Error as error:
            print(f"search_by_title: {error}")

    def search_by_author(self):
        """Search for a record by Author Name."""
        author_name = self.prompt_user_for_author_name()
        sql_string = """SELECT * FROM books WHERE author = ?"""
        try:
            with closing(self.create_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    query = cursor.execute(sql_string, (author_name,)).fetchall()
                    results = ""
                    if query:
                        for row in query:
                            results += f"{row}\n"
                        return results
                    else:
                        return f"No results found with the Author Name {author_name}"
        except sqlite3.Error as error:
            print(f"search_by_author: {error}")

    def search_by_date(self):
        """Search for a record by Date it was completed."""
        date_completed = self.prompt_user_for_date_completed()
        sql_string = """SELECT * FROM books WHERE date = ?"""
        try:
            with closing(self.create_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    query = cursor.execute(sql_string, (date_completed,)).fetchall()
                    results = ""
                    if query:
                        for row in query:
                            results += f"{row}\n"
                        return results
                    else:
                        return f"No results found with the Completion Date {date_completed}"
        except sqlite3.Error as error:
            print(f"search_by_date: {error}")