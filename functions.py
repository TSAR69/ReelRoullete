# ============================================================
# functions.py
# Feature functions for ReelRoulette.
# This module handles user input, validation, and calls the
# SQL functions defined in database.py.
#
# Concepts used (CBSE Class 12):
#   - User-defined functions
#   - Function arguments & parameters
#   - Return values
#   - if-else, while loops
#   - Lists, string handling
#   - try-except (input validation)
#   - Modular programming
# ============================================================

import database


# ------------------------------------------------------------
# Helper: read a valid integer from the user
# ------------------------------------------------------------
def read_int(prompt):
    """Reads an integer from the user. Repeats until valid input."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")


# ------------------------------------------------------------
# Helper: read a valid float from the user
# ------------------------------------------------------------
def read_float(prompt):
    """Reads a float from the user. Repeats until valid input."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")


# ------------------------------------------------------------
# Helper: read a rating between 0 and 10
# ------------------------------------------------------------
def read_rating(prompt):
    """Reads a rating between 0.0 and 10.0."""
    while True:
        try:
            value = float(input(prompt))
            if 0.0 <= value <= 10.0:
                return value
            else:
                print("Rating must be between 0 and 10.")
        except ValueError:
            print("Invalid input! Please enter a number.")


# ------------------------------------------------------------
# FEATURE 1: Add Movie
# ------------------------------------------------------------
def add_movie():
    """Takes movie details from the user and adds it to the database."""
    print("\n----- ADD NEW MOVIE -----")

    title = input("Enter movie title: ").strip()
    genre = input("Enter genre (e.g. Action, Comedy): ").strip()
    language = input("Enter language (e.g. Hindi, English): ").strip()
    release_year = read_int("Enter release year: ")
    director = input("Enter director name: ").strip()
    runtime = read_int("Enter runtime (in minutes): ")
    imdb_rating = read_rating("Enter IMDb rating (0-10): ")
    personal_rating = read_rating("Enter your personal rating (0-10): ")

    database.insert_movie(title, genre, language, release_year, director,
                          runtime, imdb_rating, personal_rating)


# ------------------------------------------------------------
# FEATURE 2: View All Movies
# ------------------------------------------------------------
def view_all_movies():
    """Displays all movies stored in the library."""
    print("\n----- VIEW ALL MOVIES -----")
    database.view_all_movies()


# ------------------------------------------------------------
# FEATURE 3: Search Movie
# ------------------------------------------------------------
def search_movie():
    """Searches movies by title, genre, language or year."""
    print("\n----- SEARCH MOVIE -----")
    print("Search by:")
    print("  1. Title")
    print("  2. Genre")
    print("  3. Language")
    print("  4. Year")

    choice = read_int("Enter your choice (1-4): ")

    if choice == 1:
        value = input("Enter title (or part of it): ").strip()
        database.search_movies(1, value)
    elif choice == 2:
        value = input("Enter genre: ").strip()
        database.search_movies(2, value)
    elif choice == 3:
        value = input("Enter language: ").strip()
        database.search_movies(3, value)
    elif choice == 4:
        value = read_int("Enter year: ")
        database.search_movies(4, value)
    else:
        print("Invalid choice!")


# ------------------------------------------------------------
# FEATURE 4: Update Movie Details
# ------------------------------------------------------------
def update_movie():
    """Updates a selected field of a movie."""
    print("\n----- UPDATE MOVIE DETAILS -----")

    movie_id = read_int("Enter movie ID to update: ")

    print("\nWhich field do you want to update?")
    print("  1. Title")
    print("  2. Genre")
    print("  3. Language")
    print("  4. Release Year")
    print("  5. Director")
    print("  6. Runtime")
    print("  7. IMDb Rating")
    print("  8. Personal Rating")
    print("  9. Watched Status")

    choice = read_int("Enter your choice (1-9): ")

    if choice == 1:
        new_value = input("Enter new title: ").strip()
        database.update_movie(movie_id, "title", new_value)
    elif choice == 2:
        new_value = input("Enter new genre: ").strip()
        database.update_movie(movie_id, "genre", new_value)
    elif choice == 3:
        new_value = input("Enter new language: ").strip()
        database.update_movie(movie_id, "language", new_value)
    elif choice == 4:
        new_value = read_int("Enter new release year: ")
        database.update_movie(movie_id, "release_year", new_value)
    elif choice == 5:
        new_value = input("Enter new director: ").strip()
        database.update_movie(movie_id, "director", new_value)
    elif choice == 6:
        new_value = read_int("Enter new runtime (minutes): ")
        database.update_movie(movie_id, "runtime", new_value)
    elif choice == 7:
        new_value = read_rating("Enter new IMDb rating (0-10): ")
        database.update_movie(movie_id, "imdb_rating", new_value)
    elif choice == 8:
        new_value = read_rating("Enter new personal rating (0-10): ")
        database.update_movie(movie_id, "personal_rating", new_value)
    elif choice == 9:
        print("Watched status options:")
        print("  0. Not watched")
        print("  1. Watched")
        new_value = read_int("Enter new watched status (0 or 1): ")
        database.update_movie(movie_id, "watched", new_value)
    else:
        print("Invalid choice!")


# ------------------------------------------------------------
# FEATURE 5: Delete Movie
# ------------------------------------------------------------
def delete_movie():
    """Deletes a movie from the library."""
    print("\n----- DELETE MOVIE -----")

    movie_id = read_int("Enter movie ID to delete: ")
    confirm = input("Are you sure? (y/n): ").strip().lower()

    if confirm == "y":
        database.delete_movie(movie_id)
    else:
        print("Deletion cancelled.")


# ------------------------------------------------------------
# FEATURE 6: Add Movie to Watchlist
# ------------------------------------------------------------
def add_movie_to_watchlist():
    """Adds a movie to the watchlist."""
    print("\n----- ADD TO WATCHLIST -----")

    movie_id = read_int("Enter movie ID to add to watchlist: ")
    database.add_to_watchlist(movie_id)


# ------------------------------------------------------------
# FEATURE 7: Remove Movie from Watchlist
# ------------------------------------------------------------
def remove_movie_from_watchlist():
    """Removes a movie from the watchlist."""
    print("\n----- REMOVE FROM WATCHLIST -----")

    movie_id = read_int("Enter movie ID to remove from watchlist: ")
    database.remove_from_watchlist(movie_id)


# ------------------------------------------------------------
# FEATURE 8: View Watchlist
# ------------------------------------------------------------
def view_watchlist():
    """Displays the current watchlist."""
    print("\n----- VIEW WATCHLIST -----")
    database.view_watchlist()


# ------------------------------------------------------------
# FEATURE 9: Mark Movie as Watched
# ------------------------------------------------------------
def mark_watched():
    """Marks a movie as watched."""
    print("\n----- MARK MOVIE AS WATCHED -----")

    movie_id = read_int("Enter movie ID: ")
    database.mark_movie_watched(movie_id)


# ------------------------------------------------------------
# FEATURE 10: Movie Recommendation
# ------------------------------------------------------------
def movie_recommendation():
    """Recommends a random movie based on genre, language and rating."""
    print("\n----- MOVIE RECOMMENDATION -----")
    print("Tell us your preferences and we will pick a movie for you!")

    # Show available genres to help the user
    print("\nShowing available genres and languages...")
    database.show_available_options()

    genre = input("\nEnter genre: ").strip()
    language = input("Enter language: ").strip()
    min_imdb = read_float("Enter minimum IMDb rating (0-10): ")

    database.recommend_movie(genre, language, min_imdb)


# ------------------------------------------------------------
# FEATURE 11: Dashboard Statistics
# ------------------------------------------------------------
def dashboard():
    """Shows the library dashboard statistics."""
    print("\n----- DASHBOARD -----")
    database.dashboard_statistics()

