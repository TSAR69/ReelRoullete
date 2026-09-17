# ============================================================
# database.py
# Handles MySQL connection, database/table creation,
# and all SQL operations for ReelRoulette.
#
# Concepts used (CBSE Class 12):
#   - mysql.connector module
#   - User-defined functions
#   - try-except-finally (exception handling)
#   - Parameterized queries with %s
#   - CREATE DATABASE / CREATE TABLE / SHOW TABLES / DESCRIBE
#   - INSERT / SELECT / UPDATE / DELETE / WHERE / LIKE / BETWEEN
#   - ORDER BY / DISTINCT / COUNT / MAX / MIN / AVG / SUM
#   - PRIMARY KEY / FOREIGN KEY / INNER JOIN
# ============================================================

import mysql.connector
from mysql.connector import Error

# ------------------------------------------------------------
# Function to create and return a database connection
# ------------------------------------------------------------
def get_connection():
    #Creates a connection to the reelroulette database.
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="your udername here",
            password="your password here",
            database="reelroulette"
        )
        return connection
    except Error as e:
        print("\nError while connecting to MySQL:", e)
        return None


# ------------------------------------------------------------
# Function to create the database and tables (called once at start)
# ------------------------------------------------------------
def create_database_and_tables():
    """Creates the database, movies and watchlist tables if they don't exist."""
    connection = None
    cursor = None
    try:
        # Step 1: Connect WITHOUT selecting a database (to create it if missing)
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="your username here",
            password="your password here"
        )
        cursor = connection.cursor()

        # CREATE DATABASE
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + "reelroulette")
        print("\nDatabase '" + "reelroulette" + "' is ready (created / already exists).")

        # USE DATABASE
        cursor.execute("USE " + "reelroulette")

        # CREATE TABLE movies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id        INT AUTO_INCREMENT PRIMARY KEY,
                title           VARCHAR(100) NOT NULL,
                genre           VARCHAR(50),
                language        VARCHAR(50),
                release_year    INT,
                director        VARCHAR(100),
                runtime         INT,
                imdb_rating     DECIMAL(3, 1),
                personal_rating DECIMAL(3, 1),
                watched         TINYINT(1) DEFAULT 0
            )
        """)

        # CREATE TABLE watchlist (with FOREIGN KEY on movie_id)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id     INT,
                date_added   DATE,
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
            )
        """)

        connection.commit()

        # SHOW TABLES
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\nTables in database '" + "reelroulette" + "':")
        for table in tables:
            print("  ->", table[0])

        # DESCRIBE TABLE movies
        print("\nStructure of 'movies' table:")
        cursor.execute("DESCRIBE movies")
        for row in cursor.fetchall():
            print("  ", row[0], "-", row[1])

        print("\nDatabase setup completed successfully!")

    except Error as e:
        print("\nError while setting up database:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: General INSERT function (used for adding a movie)
# ------------------------------------------------------------
def insert_movie(title, genre, language, release_year, director, runtime,
                 imdb_rating, personal_rating):
    """Adds a new movie to the movies table. Returns True on success."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Check for duplicate movie (same title + release year)
        check_query = "SELECT COUNT(*) FROM movies WHERE title = %s AND release_year = %s"
        cursor.execute(check_query, (title, release_year))
        count = cursor.fetchone()[0]

        if count > 0:
            print("\nError: A movie with this title and year already exists!")
            return False

        # INSERT query using parameterized values
        insert_query = """
            INSERT INTO movies
            (title, genre, language, release_year, director, runtime,
             imdb_rating, personal_rating, watched)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0)
        """
        values = (title, genre, language, release_year, director, runtime,
                  imdb_rating, personal_rating)
        cursor.execute(insert_query, values)
        connection.commit()
        print("\nMovie added successfully!")
        return True

    except Error as e:
        print("\nError while adding movie:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: View all movies (SELECT ... ORDER BY title)
# ------------------------------------------------------------
def view_all_movies():
    """Fetches and displays all movies sorted by title."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        query = """
            SELECT movie_id, title, genre, language, release_year, director,
                   runtime, imdb_rating, personal_rating, watched
            FROM movies
            ORDER BY title
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("\nNo movies found in the library. Add some movies first!")
            return

        print("\n" + "=" * 95)
        print("ALL MOVIES IN LIBRARY")
        print("=" * 95)
        print("{:<4} {:<30} {:<15} {:<12} {:<6} {:<22} {:<8} {:<8} {:<8} {:<8}".format(
            "ID", "TITLE", "GENRE", "LANGUAGE", "YEAR", "DIRECTOR",
            "RUNTIME", "IMDb", "MINE", "WATCHED"))
        print("-" * 95)

        for row in rows:
            status = "Yes" if row[9] == 1 else "No"
            print("{:<4} {:<30} {:<15} {:<12} {:<6} {:<22} {:<8} {:<8} {:<8} {:<8}".format(
                row[0], row[1][:28], row[2][:13], row[3][:10], row[4],
                row[5][:20], row[6], row[7], row[8], status))
        print("=" * 95)

    except Error as e:
        print("\nError while fetching movies:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Search movies (SELECT ... WHERE ... LIKE / =)
# ------------------------------------------------------------
def search_movies(search_by, search_value):
    """
    Searches movies by:
      1 -> Title (LIKE)
      2 -> Genre (LIKE)
      3 -> Language (LIKE)
      4 -> Year (BETWEEN same year = equal)
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        if search_by == 4:
            # Search by release year (exact match)
            query = """
                SELECT movie_id, title, genre, language, release_year, director,
                       runtime, imdb_rating, personal_rating, watched
                FROM movies
                WHERE release_year = %s
                ORDER BY title
            """
            cursor.execute(query, (search_value,))
        else:
            # Search by title / genre / language using LIKE
            pattern = "%" + search_value + "%"
            if search_by == 1:
                query = """
                    SELECT movie_id, title, genre, language, release_year, director,
                           runtime, imdb_rating, personal_rating, watched
                    FROM movies
                    WHERE title LIKE %s
                    ORDER BY title
                """
            elif search_by == 2:
                query = """
                    SELECT movie_id, title, genre, language, release_year, director,
                           runtime, imdb_rating, personal_rating, watched
                    FROM movies
                    WHERE genre LIKE %s
                    ORDER BY title
                """
            else:
                query = """
                    SELECT movie_id, title, genre, language, release_year, director,
                           runtime, imdb_rating, personal_rating, watched
                    FROM movies
                    WHERE language LIKE %s
                    ORDER BY title
                """
            cursor.execute(query, (pattern,))

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("\nNo movies found matching your search.")
            return

        print("\n" + "=" * 95)
        print("SEARCH RESULTS")
        print("=" * 95)
        print("{:<4} {:<30} {:<15} {:<12} {:<6} {:<22} {:<8} {:<8} {:<8} {:<8}".format(
            "ID", "TITLE", "GENRE", "LANGUAGE", "YEAR", "DIRECTOR",
            "RUNTIME", "IMDb", "MINE", "WATCHED"))
        print("-" * 95)

        for row in rows:
            status = "Yes" if row[9] == 1 else "No"
            print("{:<4} {:<30} {:<15} {:<12} {:<6} {:<22} {:<8} {:<8} {:<8} {:<8}".format(
                row[0], row[1][:28], row[2][:13], row[3][:10], row[4],
                row[5][:20], row[6], row[7], row[8], status))
        print("=" * 95)

    except Error as e:
        print("\nError while searching movies:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Update a movie (UPDATE ... SET ... WHERE)
# ------------------------------------------------------------
def update_movie(movie_id, field, new_value):
    """
    Updates one field of a movie.
    Allowed fields: title, genre, language, release_year, director,
                    runtime, imdb_rating, personal_rating, watched
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Allowed columns (whitelist) so SQL injection is not possible
        allowed_fields = ["title", "genre", "language", "release_year",
                          "director", "runtime", "imdb_rating",
                          "personal_rating", "watched"]

        if field not in allowed_fields:
            print("\nInvalid field name.")
            return False

        # Check the movie exists
        check_query = "SELECT COUNT(*) FROM movies WHERE movie_id = %s"
        cursor.execute(check_query, (movie_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print("\nNo movie found with that ID.")
            return False

        # UPDATE query (field name is validated, value uses %s)
        update_query = "UPDATE movies SET " + field + " = %s WHERE movie_id = %s"
        cursor.execute(update_query, (new_value, movie_id))
        connection.commit()
        print("\nMovie updated successfully!")
        return True

    except Error as e:
        print("\nError while updating movie:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Delete a movie (DELETE ... WHERE)
# ------------------------------------------------------------
def delete_movie(movie_id):
    """Deletes a movie from the library (and its watchlist entries)."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Check the movie exists
        check_query = "SELECT COUNT(*) FROM movies WHERE movie_id = %s"
        cursor.execute(check_query, (movie_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print("\nNo movie found with that ID.")
            return False

        # First delete from watchlist (foreign key reference)
        cursor.execute("DELETE FROM watchlist WHERE movie_id = %s", (movie_id,))

        # Then delete the movie
        cursor.execute("DELETE FROM movies WHERE movie_id = %s", (movie_id,))

        connection.commit()
        print("\nMovie deleted successfully!")
        return True

    except Error as e:
        print("\nError while deleting movie:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Add a movie to the watchlist (INSERT)
# ------------------------------------------------------------
def add_to_watchlist(movie_id):
    """Adds a movie to the watchlist table."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Check the movie exists
        check_query = "SELECT COUNT(*) FROM movies WHERE movie_id = %s"
        cursor.execute(check_query, (movie_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print("\nNo movie found with that ID.")
            return False

        # Check it is not already in the watchlist
        check_query2 = "SELECT COUNT(*) FROM watchlist WHERE movie_id = %s"
        cursor.execute(check_query2, (movie_id,))
        count2 = cursor.fetchone()[0]

        if count2 > 0:
            print("\nThis movie is already in your watchlist!")
            return False

        # INSERT into watchlist
        insert_query = "INSERT INTO watchlist (movie_id, date_added) VALUES (%s, CURDATE())"
        cursor.execute(insert_query, (movie_id,))
        connection.commit()
        print("\nMovie added to watchlist successfully!")
        return True

    except Error as e:
        print("\nError while adding to watchlist:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Remove a movie from the watchlist (DELETE)
# ------------------------------------------------------------
def remove_from_watchlist(movie_id):
    """Removes a movie from the watchlist table."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Check it exists in the watchlist
        check_query = "SELECT COUNT(*) FROM watchlist WHERE movie_id = %s"
        cursor.execute(check_query, (movie_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print("\nThis movie is not in your watchlist.")
            return False

        cursor.execute("DELETE FROM watchlist WHERE movie_id = %s", (movie_id,))
        connection.commit()
        print("\nMovie removed from watchlist successfully!")
        return True

    except Error as e:
        print("\nError while removing from watchlist:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: View the watchlist (INNER JOIN)
# ------------------------------------------------------------
def view_watchlist():
    """Displays all movies in the watchlist using INNER JOIN."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            SELECT m.movie_id, m.title, m.genre, m.language, m.release_year,
                   m.imdb_rating, w.date_added
            FROM watchlist w
            INNER JOIN movies m ON w.movie_id = m.movie_id
            ORDER BY w.date_added DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("\nYour watchlist is empty. Add some movies to it!")
            return

        print("\n" + "=" * 80)
        print("YOUR WATCHLIST")
        print("=" * 80)
        print("{:<6} {:<30} {:<15} {:<12} {:<6} {:<8} {:<12}".format(
            "ID", "TITLE", "GENRE", "LANGUAGE", "YEAR", "IMDb", "DATE ADDED"))
        print("-" * 80)

        for row in rows:
            # Convert date object to string for proper formatting
            date_added = str(row[6])
            print("{:<6} {:<30} {:<15} {:<12} {:<6} {:<8} {:<12}".format(
                row[0], row[1][:28], row[2][:13], row[3][:10], row[4],
                row[5], date_added))
        print("=" * 80)

    except Error as e:
        print("\nError while viewing watchlist:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Mark a movie as watched (UPDATE)
# ------------------------------------------------------------
def mark_movie_watched(movie_id):
    """Sets the watched field of a movie to 1."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        # Check the movie exists
        check_query = "SELECT COUNT(*) FROM movies WHERE movie_id = %s"
        cursor.execute(check_query, (movie_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print("\nNo movie found with that ID.")
            return False

        update_query = "UPDATE movies SET watched = 1 WHERE movie_id = %s"
        cursor.execute(update_query, (movie_id,))
        connection.commit()
        print("\nMovie marked as watched!")
        return True

    except Error as e:
        print("\nError while marking movie as watched:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Show available genres and languages (DISTINCT)
# ------------------------------------------------------------
def show_available_options():
    """Shows all distinct genres and languages present in the library."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        # DISTINCT genres
        cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
        genres = cursor.fetchall()

        # DISTINCT languages
        cursor.execute("SELECT DISTINCT language FROM movies ORDER BY language")
        languages = cursor.fetchall()

        genre_list = []
        for g in genres:
            genre_list.append(g[0])

        language_list = []
        for lang in languages:
            language_list.append(lang[0])

        print("  Genres   :", ", ".join(genre_list) if genre_list else "None")
        print("  Languages:", ", ".join(language_list) if language_list else "None")

    except Error as e:
        print("\nError while fetching options:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Movie recommendation (SELECT ... WHERE ... ORDER BY RAND())
# ------------------------------------------------------------
def recommend_movie(genre, language, min_imdb):
    """
    Picks one random movie matching genre, language and minimum IMDb rating.
    Uses ORDER BY RAND() LIMIT 1 to pick a random match.
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            SELECT movie_id, title, genre, language, release_year, director,
                   runtime, imdb_rating, personal_rating, watched
            FROM movies
            WHERE genre = %s AND language = %s AND imdb_rating >= %s
            ORDER BY RAND()
            LIMIT 1
        """
        cursor.execute(query, (genre, language, min_imdb))
        row = cursor.fetchone()

        if row is None:
            print("\nNo movie found matching your preferences. Try relaxing them!")
            return

        print("\n" + "=" * 60)
        print("RECOMMENDED MOVIE FOR YOU")
        print("=" * 60)
        print("  Title       :", row[1])
        print("  Genre       :", row[2])
        print("  Language    :", row[3])
        print("  Year        :", row[4])
        print("  Director    :", row[5])
        print("  Runtime     :", row[6], "minutes")
        print("  IMDb Rating :", row[7])
        print("  My Rating   :", row[8])
        print("=" * 60)

    except Error as e:
        print("\nError while recommending movie:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# HELPER: Dashboard statistics (aggregate functions)
# ------------------------------------------------------------
def dashboard_statistics():
    """
    Shows statistics using SQL aggregate functions:
      COUNT, AVG, MAX, MIN, SUM
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        # Total movies
        cursor.execute("SELECT COUNT(*) FROM movies")
        total_movies = cursor.fetchone()[0]

        # Watched movies
        cursor.execute("SELECT COUNT(*) FROM movies WHERE watched = 1")
        watched_movies = cursor.fetchone()[0]

        # Unwatched movies
        cursor.execute("SELECT COUNT(*) FROM movies WHERE watched = 0")
        unwatched_movies = cursor.fetchone()[0]

        # Average IMDb rating
        cursor.execute("SELECT AVG(imdb_rating) FROM movies")
        avg_imdb = cursor.fetchone()[0]

        # Highest rated movie (MAX rating)
        cursor.execute("""
            SELECT title, MAX(imdb_rating)
            FROM movies
            GROUP BY title
            ORDER BY MAX(imdb_rating) DESC
            LIMIT 1
        """)
        highest = cursor.fetchone()

        # Total watchlist movies
        cursor.execute("SELECT COUNT(*) FROM watchlist")
        total_watchlist = cursor.fetchone()[0]

        # Total runtime of all movies (SUM)
        cursor.execute("SELECT SUM(runtime) FROM movies")
        total_runtime = cursor.fetchone()[0]

        # DISTINCT genres available
        cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
        genres = cursor.fetchall()

        # Print the dashboard
        print("\n" + "=" * 55)
        print("REELROULETTE DASHBOARD")
        print("=" * 55)
        print("  Total Movies        :", total_movies)
        print("  Watched Movies      :", watched_movies)
        print("  Unwatched Movies    :", unwatched_movies)
        if avg_imdb is not None:
            print("  Average IMDb Rating :", round(avg_imdb, 2))
        else:
            print("  Average IMDb Rating : N/A")
        if highest is not None:
            print("  Highest Rated Movie :", highest[0], "(", highest[1], ")")
        else:
            print("  Highest Rated Movie : N/A")
        print("  Total Watchlist     :", total_watchlist)
        if total_runtime is not None:
            print("  Total Runtime (min) :", total_runtime)
        else:
            print("  Total Runtime (min) : N/A")

        print("\n  Genres Available:")
        if len(genres) > 0:
            genre_list = []
            for g in genres:
                genre_list.append(g[0])
            print("    ", ", ".join(genre_list))
        else:
            print("    None")
        print("=" * 55)

    except Error as e:
        print("\nError while generating dashboard:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

