[cite: 1] import mysql.connector as mysql, csv

def create_db_connection():
    """
    Creates and returns a connection to the database.
    """
    # !!! UPDATE THESE VALUES to match your MySQL setup !!!
    return mysql.connect(
        host = 'localhost',  # or 'arch-inspiron' 
        user = 'your_username', # or 'dezer0' 
        password = 'your_password', # or '1245' 
        database = 'school' [cite: 1]
    )

def _print_student_table(rows):
    """
    Helper function to print a formatted table of student data.
    """
    if not rows:
        print("No records found.")
        return

    # Print table header
    print("+----+----------------------+---------------------------+--------+")
    print("| ID | Name                 | Department                | Marks  |") [cite: 3, 4, 5, 6]
    print("+----+----------------------+---------------------------+--------+")
    
    # Print each row
    for row in rows:
        print(f"|{row[0]:<3} | {row[1]:<20} | {row[2]:<25} | {row[3]:>6d} |") [cite: 8]
    
    print("+----+----------------------+---------------------------+--------+")

def add_new_students():
    """
    Prompts the user to add one or more new students to the database.
    """
    try:
        n = int(input("Enter number of students to be added: "))
        if n <= 0:
            print("Please enter a positive number.")
            return

        added_count = 0
        with create_db_connection() as conn:
            with conn.cursor() as cur:
                for _ in range(n):
                    print(f"\nEntering details for student {_+1}:")
                    name = input("  Enter name: ")
                    dept = input("  Enter department: ")
                    marks = int(input("  Enter marks: "))
                    
                    cur.execute(
                        "INSERT INTO students (name, department, marks) VALUES (%s, %s, %s)",
                        (name, dept, marks)
                    ) [cite: 2]
                    added_count += 1
                
                conn.commit() [cite: 2]
        
        print(f"Successfully added {added_count} student(s)!")

    except ValueError:
        print("Invalid input. Please enter numbers where required.")
    except mysql.Error as err:
        print(f"Database error: {err}")

def view_all_students():
    """
    Fetches and displays all students from the database.
    """
    try:
        with create_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM students") [cite: 2]
                rows = cur.fetchall() [cite: 2]
                _print_student_table(rows)
    except mysql.Error as err:
        print(f"Database error: {err}")

def find_students_by_dept():
    """
    Searches for and displays students by a department name (partial match).
    """
    dept_search = input("Search by department name: ")
    try:
        with create_db_connection() as conn:
            with conn.cursor() as cur:
                # Fixed: Use LIKE for partial matching
                cur.execute("SELECT * FROM students WHERE department LIKE %s", (dept_search + '%',))
                rows = cur.fetchall()
                if not rows:
                    print("No students found for that department.") [cite: 7]
                else:
                    _print_student_table(rows)
    except mysql.Error as err:
        print(f"Database error: {err}")

def remove_student_by_id():
    """
    Deletes a student from the database using their ID.
    """
    try:
        sid = int(input("Enter Student ID to delete: "))
        
        with create_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM students WHERE id = %s", (sid,)) [cite: 7]
                conn.commit() [cite: 7]
                
                if cur.rowcount == 0:
                    print("No record found with that ID.") [cite: 7]
                else:
                    print(f"Student ID {sid} deleted successfully.")
                    
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
    except mysql.Error as err:
        print(f"Database error: {err}")

def show_performance_analytics():
    """
    Displays aggregate analytics like count, average, max, and min marks.
    """
    try:
        with create_db_connection() as conn:
            with conn.cursor() as cur: [cite: 9]
                # Overall Analytics
                cur.execute("SELECT COUNT(name), AVG(marks), MAX(marks), MIN(marks) FROM students") [cite: 9]
                count_, avg_, max_, min_ = cur.fetchone()
                print("\n--- Overall Performance ---")
                print(f"Total Students: {count_} | Average Marks: {avg_:.2f} | Highest Marks: {max_} | Lowest Marks: {min_}") [cite: 10, 11]
                
                # Department-wise Analytics
                cur.execute("SELECT department, AVG(marks) FROM students GROUP BY department") [cite: 11]
                rows = cur.fetchall() [cite: 11]
                print("\n--- Department-wise Average Marks ---")
                print("+--------------------------+---------+")
                print("| Department               | Avg Marks|")
                print("+--------------------------+---------+")
                for dept, avg in rows:
                    print(f"|{dept:<26}| {avg:>7.2f} |")
                print("+--------------------------+---------+")
                
    except mysql.Error as err:
        print(f"Database error: {err}")

def display_top_performers(threshold=90):
    """
    Shows all students with marks at or above a given threshold.
    """
    print(f"\n--- Top Performers (Marks >= {threshold}) ---")
    try:
        with create_db_connection() as conn:
            with conn.cursor() as cur: [cite: 12]
                cur.execute("SELECT * FROM students WHERE marks >= %s", (threshold,))
                rows = cur.fetchall() [cite: 12]
                _print_student_table(rows)
    except mysql.Error as err:
        print(f"Database error: {err}")

def show_dept_leaderboard():
    """
    Displays a leaderboard for a specific department, ordered by marks.
    """
    print("\n--- Department Leaderboards ---")
    print("1. Civil\n2. Mechanical\n3. Computer Science\n4. Information Technology\n5. Electronics")
    
    try:
        choice = int(input("Select department (1-5): ").strip()) [cite: 15]
        choices = {
            1: "Civil",
            2: "Mechanical",
            3: "Computer Science", [cite: 16]
            4: "Information Technology",
            5: "Electronics",
        }
        
        dept = choices.get(choice)
        if not dept:
            print("Invalid choice. Please select from 1-5.")
            return

        with create_db_connection() as conn:
            with conn.cursor() as cur: [cite: 17]
                cur.execute(
                    "SELECT * FROM students WHERE department = %s ORDER BY marks DESC",
                    (dept,)
                ) [cite: 17]
                rows = cur.fetchall()
                print(f"\n--- Leaderboard for {dept} ---")
                _print_student_table(rows) [cite: 18]

    except ValueError: [cite: 15]
        print("Invalid choice. Please enter a number.")
    except mysql.Error as err:
        print(f"Database error: {err}")

def update_bonus_marks():
    """
    Provides a menu to add bonus marks to a single student or an entire department.
    """
    while True:
        print("\n--- Add Bonus Marks ---")
        print("1. Add to a specific student (by ID)")
        print("2. Add to an entire department")
        print("3. Back to main menu")
        
        try:
            choice = int(input("Enter your choice (1-3): ")) [cite: 22]
            
            if choice == 1:
                # Add marks to one student
                sid = int(input("Enter student ID: "))
                bonus = int(input(f"Enter bonus marks for student {sid}: +"))
                with create_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE students SET marks = marks + %s WHERE id = %s", (bonus, sid)) [cite: 23]
                        conn.commit()
                        if cur.rowcount == 0:
                            print(f"No student found with ID {sid}.")
                        else:
                            print("Bonus marks added successfully!")

            elif choice == 2:
                # Add marks to a department
                print("\nSelect Department:")
                print("1. Civil\n2. Mechanical\n3. Computer Science\n4. Information Technology\n5. Electronics")
                raw = input("Enter dept (1-5): ").strip() [cite: 24]
                
                choice_num = int(raw) [cite: 25]
                choices = {
                    1: "Civil", 2: "Mechanical", 3: "Computer Science", [cite: 26]
                    4: "Information Technology", 5: "Electronics"
                }
                dept_name = choices.get(choice_num)
                
                if not dept_name:
                    print("Invalid department choice.") [cite: 27]
                    continue
                    
                bonus = int(input(f"Enter bonus marks for {dept_name}: +").strip())
                
                with create_db_connection() as conn: [cite: 28]
                    with conn.cursor() as cur:
                        cur.execute(
                            "UPDATE students SET marks = marks + %s WHERE department = %s",
                            (bonus, dept_name)
                        ) [cite: 28]
                        conn.commit() [cite: 29]
                        
                        if cur.rowcount == 0:
                            print("Department not found or no rows updated.")
                        else:
                            print(f"Added +{bonus} marks to {cur.rowcount} student(s) in {dept_name}.")

            elif choice == 3: [cite: 30]
                print("Returning to main menu...")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except mysql.Error as err:
            print(f"Database error: {err}")

def export_top_students_csv(threshold=90):
    """
    Exports all students with marks >= threshold to a CSV file.
    """
    filename = "high_performers.csv"
    print(f"\nExporting high performers (Marks >= {threshold}) to {filename}...")
    try:
        with create_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM students WHERE marks >= %s", (threshold,)) [cite: 30]
                rows = cur.fetchall()
                
                if not rows:
                    print("No high performers found to export.")
                    return

                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([d[0] for d in cur.description])  # Write header [cite: 31]
                    writer.writerows(rows) [cite: 31]
        
        print(f"Successfully exported {len(rows)} students to {filename}.")
        
    except mysql.Error as err:
        print(f"Database error: {err}")
    except IOError as err:
        print(f"File error: {err}")

def main():
    """
    Main function to run the application menu.
    """
    while True:
        print("\n===== STUDENT PERFORMANCE ANALYZER =====")
        print(" 1. Add New Students")
        print(" 2. View All Students")
        print(" 3. Find Students by Department")
        print(" 4. Remove Student by ID") [cite: 36]
        print(" 5. Show Performance Analytics") [cite: 38]
        print(" 6. Display Top Performers (>= 90)")
        print(" 7. Show Department Leaderboard")
        print(" 8. Update Bonus Marks")
        print(" 9. Export High Performers to CSV")
        print("10. Exit") [cite: 39]
        
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == '1':
            add_new_students() [cite: 37]
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            find_students_by_dept()
        elif choice == '4':
            remove_student_by_id()
        elif choice == '5':
            show_performance_analytics()
        elif choice == '6':
            display_top_performers() # Uses default 90
        elif choice == '7':
            show_dept_leaderboard()
        elif choice == '8':
            update_bonus_marks()
        elif choice == '9':
            export_top_students_csv() # Uses default 90
        elif choice == '10':
            print("Exiting program. Goodbye!") [cite: 39]
            break
        else:
            print("Invalid choice. Please try again.") [cite: 40]

if __name__ == "__main__":
    main()