########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv

#################################################################################

## Change to False to disable Sample
SHOW = False



############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')

        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)", ("1", "test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())


######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)

    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "zhong61/zhong87"
        return gt_username

    # Part a.i Create Tables [2 points]
    def part_ai_1(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER,
            title TEXT,
            score REAL
        );
        """
        ######################################################################

        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = """
        CREATE TABLE IF NOT EXISTS movie_cast (
            movie_id INTEGER,
            cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
            popularity REAL
        );
        """
        ######################################################################

        return self.execute_query(connection, part_ai_2_sql)

    # Part a.ii Import Data [2 points]
    def part_aii_1(self, connection, path):
        movies_path = path  # Path to movies.csv

        with open(movies_path, 'r') as file:
            for line in file:
                line = line.strip()
                first_comma = line.find(',')  # Position of first comma
                last_comma = line.rfind(',')  # Position of last comma

                # Extracting id, title, and score
                if first_comma != -1 and last_comma != -1 and first_comma != last_comma:
                    id = line[:first_comma]
                    title = line[first_comma + 1:last_comma]
                    score = line[last_comma + 1:]
                    connection.execute("INSERT INTO movies (id, title, score) VALUES (?, ?, ?)", (id, title, score))

        connection.commit()

        # Return the count of rows in the movies table
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def part_aii_2(self, connection, path):
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()

                # Find positions of the first two and last two commas
                first_comma = line.find(',')
                second_comma = line.find(',', first_comma + 1)
                last_comma = line.rfind(',')
                second_last_comma = line.rfind(',', 0, last_comma)

                # Extracting movie_id, cast_id, cast_name, birthday, popularity
                if first_comma != -1 and second_comma != -1 and last_comma != -1 and second_last_comma != -1 and second_comma < second_last_comma:
                    movie_id = line[:first_comma]
                    cast_id = line[first_comma + 1:second_comma]
                    cast_name = line[second_comma + 1:second_last_comma]
                    birthday = line[second_last_comma + 1:last_comma]
                    popularity = line[last_comma + 1:]

                    # Handle 'None' value in birthday
                    if birthday == "None":
                        birthday = None

                    connection.execute(
                        "INSERT INTO movie_cast (movie_id, cast_id, cast_name, birthday, popularity) VALUES (?, ?, ?, ?, ?)",
                        (movie_id, cast_id, cast_name, birthday, popularity))

        connection.commit()

        # Return the count of rows in the movie_cast table
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self, connection):
        # Create the cast_bio table
        part_aiii_sql = """
        CREATE TABLE IF NOT EXISTS cast_bio (
            cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
            popularity REAL
        );
        """
        self.execute_query(connection, part_aiii_sql)

        # Insert unique records into cast_bio from movie_cast
        part_aiii_insert_sql = """
        INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity)
        SELECT DISTINCT cast_id, cast_name, birthday, popularity 
        FROM movie_cast;
        """
        self.execute_query(connection, part_aiii_insert_sql)

        # Return the count of rows in the cast_bio table
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part b Create Indexes [1 points]
    def part_b_1(self, connection):
        # Create index on the id column in the movies table
        part_b_1_sql = """
        CREATE INDEX IF NOT EXISTS movie_index ON movies (id);
        """
        return self.execute_query(connection, part_b_1_sql)

    def part_b_2(self, connection):
        # Create index on the cast_id column in the movie_cast table
        part_b_2_sql = """
        CREATE INDEX IF NOT EXISTS cast_index ON movie_cast (cast_id);
        """
        return self.execute_query(connection, part_b_2_sql)

    def part_b_3(self, connection):
        # Create index on the cast_id column in the cast_bio table
        part_b_3_sql = """
        CREATE INDEX IF NOT EXISTS cast_bio_index ON cast_bio (cast_id);
        """
        return self.execute_query(connection, part_b_3_sql)

    # Part c Calculate a Proportion [3 points]
    def part_c(self, connection):
        # SQL query to calculate the proportion
        part_c_sql = """
        SELECT 
            printf("%.2f", 
                (SELECT COUNT(*) FROM movies WHERE score BETWEEN 7 AND 20) * 100.0 / COUNT(*)
            ) 
        FROM movies;
        """
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self, connection):
        # SQL query to find the most prolific actors
        part_d_sql = """
        SELECT cast_name, COUNT(*) as appearance_count
        FROM movie_cast
        WHERE popularity > 10
        GROUP BY cast_name
        ORDER BY appearance_count DESC, cast_name
        LIMIT 5;
        """
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self, connection):
        # SQL query to find the highest scoring movies favoring smaller cast size
        part_e_sql = """
        SELECT m.title as movie_title, printf("%.2f", m.score) as score, COUNT(mc.cast_id) as cast_count
        FROM movies m
        JOIN movie_cast mc ON m.id = mc.movie_id
        GROUP BY m.id
        ORDER BY m.score DESC, cast_count ASC, m.title
        LIMIT 5;
        """
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()

    # Part f Get High Scoring Actors [4 points]
    def part_f(self, connection):
        # SQL query to find the top ten cast members with the highest average movie scores
        part_f_sql = """
        SELECT mc.cast_id, mc.cast_name, printf("%.2f", AVG(m.score)) as average_score
        FROM movie_cast mc
        JOIN movies m ON mc.movie_id = m.id
        WHERE m.score >= 25
        GROUP BY mc.cast_id, mc.cast_name
        HAVING COUNT(m.id) >= 3
        ORDER BY average_score DESC, mc.cast_name
        LIMIT 10;
        """
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self, connection):
        # SQL statement to create the good_collaboration view
        part_g_sql = """
        CREATE VIEW IF NOT EXISTS good_collaboration AS
        SELECT 
            mc1.cast_id as cast_member_id1,
            mc2.cast_id as cast_member_id2,
            COUNT(mc1.movie_id) as movie_count,
            AVG(m.score) as average_movie_score
        FROM 
            movie_cast mc1
            JOIN movie_cast mc2 ON mc1.movie_id = mc2.movie_id AND mc1.cast_id < mc2.cast_id
            JOIN movies m ON mc1.movie_id = m.id
        GROUP BY 
            mc1.cast_id, 
            mc2.cast_id
        HAVING 
            COUNT(mc1.movie_id) >= 2 AND 
            AVG(m.score) >= 40;
        """
        return self.execute_query(connection, part_g_sql)

    def part_gi(self, connection):
        # SQL query to find the top 5 cast members with the highest collaboration scores
        part_g_i_sql = """
        SELECT 
            mc.cast_id, 
            mc.cast_name, 
            printf("%.2f", AVG(g.average_movie_score)) as collaboration_score
        FROM 
            (SELECT cast_member_id1 as cast_id, average_movie_score FROM good_collaboration
             UNION ALL
             SELECT cast_member_id2 as cast_id, average_movie_score FROM good_collaboration) as g
        JOIN 
            movie_cast mc ON mc.cast_id = g.cast_id
        GROUP BY 
            mc.cast_id, mc.cast_name
        ORDER BY 
            collaboration_score DESC, mc.cast_name
        LIMIT 5;
        """
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()

    # Part h FTS [4 points]
    def part_h(self, connection, path):
        # Create the movie_overview FTS table using fts4
        part_h_sql = """
        CREATE VIRTUAL TABLE IF NOT EXISTS movie_overview USING fts4(
            id INTEGER,
            overview TEXT
        );
        """
        connection.execute(part_h_sql)

        # Import data into movie_overview from movie_overview.csv
        movie_overview_path = path  # Assuming path is the full path to movie_overview.csv
        with open(movie_overview_path, 'r') as file:
            for line in file:
                id, overview = line.strip().split(',', 1)  # Splitting only on the first comma
                connection.execute("INSERT INTO movie_overview (id, overview) VALUES (?, ?)", (id, overview))

        connection.commit()

        # Count the number of rows in the movie_overview table
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def part_hi(self, connection):
        # Count the number of movies whose overview contains the word 'fight'
        part_hi_sql = """
        SELECT COUNT(*) FROM movie_overview
        WHERE overview MATCH 'fight';
        """
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]

    def part_hii(self, connection):
        # Count the number of movies that contain the terms 'space' and 'program'
        # within no more than 5 intervening terms
        part_hii_sql = """
        SELECT COUNT(*) FROM movie_overview
        WHERE overview MATCH 'space NEAR/5 program';
        """
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":

    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except Exception as e:
        print("Error in Part a.i")
        print(e)

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn, "data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(
            db.part_aii_2(conn, "data/movie_cast.csv")))
    except Exception as e:
        print("Error in part a.ii")
        print(e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except Exception as e:
        print("Error in part a.iii")
        print(e)

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except Exception as e:
        print("Error in part b")
        print(e)

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except Exception as e:
        print("Error in part c")
        print(e)

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0], line[1])
    except Exception as e:
        print("Error in part d")
        print(e)

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part e")
        print(e)

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part f")
        print(e)

    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print("\033[32mRow count for good_collaboration view:\033[m",
              conn.execute("select count(*) from good_collaboration").fetchall()[0][0])
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part g")
        print(e)

    try:
        print('\033[32m' + "part h: " + '\033[m' + str(db.part_h(conn, "data/movie_overview.csv")))
        print('\033[32m' + "Count h.i: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hii(conn)))
    except Exception as e:
        print("Error in part h")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################

