# ============================================================
# main.py
# Main entry point for ReelRoulette.
# Displays a banner, then a menu, and calls the appropriate
# feature functions.
#
# Concepts used (CBSE Class 12):
#   - User-defined functions
#   - while loop (menu loop)
#   - if-elif-else (menu selection)
#   - try-except-finally (error handling)
#   - Modules (import functions, database)
#   - File handling (banner.txt)
# ============================================================

import functions
import database


# ------------------------------------------------------------
# Function to display the banner (cover page) from banner.txt
# ------------------------------------------------------------
def show_banner():
    """Reads and prints the banner.txt file as the cover page."""
    try:
        banner_file = open("banner.txt", "r")
        banner = banner_file.read()
        banner_file.close()
        print(banner)
    except FileNotFoundError:
        print("ReelRoulette - Offline Movie Library & Smart Recommendation System")
    except Exception as e:
        print("ReelRoulette - Offline Movie Library & Smart Recommendation System")


# ------------------------------------------------------------
# Function to display the main menu
# ------------------------------------------------------------
def show_menu():
    """Prints the main menu options."""
    print()
    print("=" * 55)
    print("        REELROULETTE - MOVIE LIBRARY")
    print("=" * 55)
    print("  1. Add Movie")
    print("  2. View All Movies")
    print("  3. Search Movie")
    print("  4. Update Movie Details")
    print("  5. Delete Movie")
    print("  6. Add Movie to Watchlist")
    print("  7. Remove Movie from Watchlist")
    print("  8. View Watchlist")
    print("  9. Mark Movie as Watched")
    print(" 10. Movie Recommendation")
    print(" 11. Dashboard Statistics")
    print("  0. Exit")
    print("=" * 55)


# ------------------------------------------------------------
# Main program starts here
# ------------------------------------------------------------
def main():
    """Runs the main menu loop of the program."""

    # Show the banner as the cover page
    show_banner()

    print()
    print("Welcome to ReelRoulette - Offline Movie Library!")

    # Set up the database and tables (only once at the start)
    database.create_database_and_tables()

    while True:
        try:
            show_menu()
            choice = input("Enter your choice (0-11): ")

            if choice == "1":
                functions.add_movie()
            elif choice == "2":
                functions.view_all_movies()
            elif choice == "3":
                functions.search_movie()
            elif choice == "4":
                functions.update_movie()
            elif choice == "5":
                functions.delete_movie()
            elif choice == "6":
                functions.add_movie_to_watchlist()
            elif choice == "7":
                functions.remove_movie_from_watchlist()
            elif choice == "8":
                functions.view_watchlist()
            elif choice == "9":
                functions.mark_watched()
            elif choice == "10":
                functions.movie_recommendation()
            elif choice == "11":
                functions.dashboard()
            elif choice == "0":
                print()
                print("Thank you for using ReelRoulette. Goodbye!")
                break
            else:
                print()
                print("Invalid choice! Please enter a number between 0 and 11.")

            if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                confirm = input("\nDo you want to continue? (y/n): ")
                if confirm.lower() != 'y':
                    print("\nThank you for using ReelRoulette. Goodbye!")
                    break

        except Exception as e:
            print()
            print("An unexpected error occurred:", e)


# Call the main function to start the program
main()

