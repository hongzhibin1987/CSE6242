import http.client
import json
import csv
import requests

class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={self.api_key}&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return []  # or handle the error as needed

        credits_data = response.json()['cast']

        if vote_avg_threshold is not None:
            credits_data = [
                credit for credit in credits_data
                if credit.get('vote_average') is not None and credit['vote_average'] >= vote_avg_threshold
            ]

        # Restructure the data to include only 'id', 'title', and 'vote_average'
        credits_data = [
            {'id': credit['id'],
             'title': credit['title'],
             'vote_avg': credit['vote_average']}
            for credit in credits_data
            if ('id' in credit and 'title' in credit and 'vote_average' in credit and
                credit['vote_average'] >= vote_avg_threshold)
        ]

        return credits_data

    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:
        # get the exclude_ids list!!!!
        # get the exclue_ids!!!!!!

        # Correct URL with dynamic movie_id
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.api_key}&language=en-US"

        response = requests.get(url)
        if response.status_code != 200:
            return []

        full_cast_data = response.json()['cast']

        # Apply exclude_ids filter
        if exclude_ids:
            full_cast_data = [member for member in full_cast_data if member['id'] not in exclude_ids]

        # If limit is specified, apply it
        if limit is not None:
            full_cast_data = [member for member in full_cast_data if member['order'] <= limit]

        # Restructure the data to include specified fields
        cast_data = [
            {
                'movie_id': movie_id,
                'id': member['id'],
                'name': member['name'],
                'cast_id': member['cast_id'],
                'order': member['order']
            }
            for member in full_cast_data
        ]

        return cast_data


def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    GTUsername = 'zhong61/zhong87'
    return GTUsername

# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

class Graph:
    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        Initialize a Graph object.
        """
        self.nodes = []
        self.edges = []

        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str) -> None:
        """
        Add a node to the graph if it does not already exist.
        """
        if not any(node[0] == id for node in self.nodes):
            self.nodes.append((id, name))

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        """
        if source != target and (source, target) not in self.edges and (target, source) not in self.edges:
            self.edges.append((source, target))

    def total_nodes(self) -> int:
        """
        Return the total number of nodes in the graph.
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Return the total number of edges in the graph.
        """
        return len(self.edges)

    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree.
        """
        degree_count = {node[0]: 0 for node in self.nodes}
        for edge in self.edges:
            degree_count[edge[0]] += 1
            degree_count[edge[1]] += 1

        max_degree = max(degree_count.values())
        return {node: degree for node, degree in degree_count.items() if degree == max_degree}

    def print_nodes(self):
        """
        Print all nodes. Used for debugging.
        """
        print(self.nodes)

    def print_edges(self):
        """
        Print all edges. Used for debugging.
        """
        print(self.edges)

    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        Write all edges out as .csv.
        """
        with open(path, 'w', encoding='utf-8') as edges_file:
            edges_file.write("source,target\n")
            for e in self.edges:
                edges_file.write(f"{e[0]},{e[1]}\n")

    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        Write all nodes out as .csv.
        """
        with open(path, 'w', encoding='utf-8') as nodes_file:
            nodes_file.write("id,name\n")
            for n in self.nodes:
                nodes_file.write(f"{n[0]},{n[1]}\n")

# comment the original section out:

if __name__ == "__main__":
    person_id = '2975'
    actor_name = 'Laurence Fishburne'
    vote_avg_threshold = 8.0
    credit_limit = 2
    tmdb_api_utils = TMDBAPIUtils(api_key='14386f6d2560c16967a0141156e72327')
    graph = Graph()

    exclude_ids = {}
    # Add the initial actor
    graph.add_node(person_id, actor_name)
    actors_to_process = set([person_id])

    # Perform iterations
    for _ in range(3):  # Two additional iterations
        new_actors_to_process = set()

        for actor_id in actors_to_process:
            movie_credits = tmdb_api_utils.get_movie_credits_for_person(actor_id, vote_avg_threshold)

            for movie in movie_credits:
                movie_id = str(movie['id'])
                cast_data = tmdb_api_utils.get_movie_cast(movie_id, credit_limit)

                for cast_member in cast_data:
                    cast_member_id = str(cast_member['id'])

                    if cast_member_id != actor_id:
                        if cast_member_id not in [node[0] for node in graph.nodes]:
                            graph.add_node(cast_member_id, cast_member['name'])
                            new_actors_to_process.add(cast_member_id)

                        if not any(edge in [(actor_id, cast_member_id), (cast_member_id, actor_id)] for edge in graph.edges):
                            graph.add_edge(actor_id, cast_member_id)

        actors_to_process = new_actors_to_process

    # Print and write final graph
    print("Final Nodes:")
    for node in graph.nodes:
        print(f"{node[0]}, {node[1]}")
    print("\nFinal Edges:")
    for edge in graph.edges:
        print(f"{edge[0]}, {edge[1]}")

    graph.write_edges_file()
    graph.write_nodes_file()






################################### exclude movie id works, exclude staff is not
import http.client
import json
import csv
import requests

class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={self.api_key}&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return []  # or handle the error as needed

        credits_data = response.json()['cast']

        if vote_avg_threshold is not None:
            credits_data = [
                credit for credit in credits_data
                if credit.get('vote_average') is not None and credit['vote_average'] >= vote_avg_threshold
            ]

        # Restructure the data to include only 'id', 'title', and 'vote_average'
        credits_data = [
            {'id': credit['id'],
             'title': credit['title'],
             'vote_avg': credit['vote_average']}
            for credit in credits_data
            if ('id' in credit and 'title' in credit and 'vote_average' in credit and
                credit['vote_average'] >= vote_avg_threshold)
        ]

        return credits_data

    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:
        # get the exclude_ids list!!!!
        # get the exclue_ids!!!!!!

        # Correct URL with dynamic movie_id
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.api_key}&language=en-US"

        response = requests.get(url)
        if response.status_code != 200:
            return []

        full_cast_data = response.json()['cast']

        # Apply exclude_ids filter
        if exclude_ids:
            full_cast_data = [member for member in full_cast_data if member['id'] not in exclude_ids]

        # If limit is specified, apply it
        if limit is not None:
            full_cast_data = [member for member in full_cast_data if member['order'] <= limit]

        # Restructure the data to include specified fields
        cast_data = [
            {
                'movie_id': movie_id,
                'id': member['id'],
                'name': member['name'],
                'cast_id': member['cast_id'],
                'order': member['order']
            }
            for member in full_cast_data
        ]

        return cast_data


def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    GTUsername = 'zhong61/zhong87'
    return GTUsername

# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

class Graph:
    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        Initialize a Graph object.
        """
        self.nodes = []
        self.edges = []

        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str) -> None:
        """
        Add a node to the graph if it does not already exist.
        """
        if not any(node[0] == id for node in self.nodes):
            self.nodes.append((id, name))

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        """
        if source != target and (source, target) not in self.edges and (target, source) not in self.edges:
            self.edges.append((source, target))

    def total_nodes(self) -> int:
        """
        Return the total number of nodes in the graph.
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Return the total number of edges in the graph.
        """
        return len(self.edges)

    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree.
        """
        degree_count = {node[0]: 0 for node in self.nodes}
        for edge in self.edges:
            degree_count[edge[0]] += 1
            degree_count[edge[1]] += 1

        max_degree = max(degree_count.values())
        return {node: degree for node, degree in degree_count.items() if degree == max_degree}

    def print_nodes(self):
        """
        Print all nodes. Used for debugging.
        """
        print(self.nodes)

    def print_edges(self):
        """
        Print all edges. Used for debugging.
        """
        print(self.edges)

    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        Write all edges out as .csv.
        """
        with open(path, 'w', encoding='utf-8') as edges_file:
            edges_file.write("source,target\n")
            for e in self.edges:
                edges_file.write(f"{e[0]},{e[1]}\n")

    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        Write all nodes out as .csv.
        """
        with open(path, 'w', encoding='utf-8') as nodes_file:
            nodes_file.write("id,name\n")
            for n in self.nodes:
                nodes_file.write(f"{n[0]},{n[1]}\n")

# comment the original section out:

if __name__ == "__main__":
    person_id = '2975'  # Laurence Fishburne
    actor_name = 'Laurence Fishburne'
    vote_avg_threshold = 8.0
    credit_limit = 2
    tmdb_api_utils = TMDBAPIUtils(api_key='14386f6d2560c16967a0141156e72327')
    graph = Graph()

    # Define movie IDs to exclude
    exclude_movie_ids = [603]  # Add movie IDs to exclude
    excluded_actors = set()  # Set to store actors from excluded movies

    # Add the initial actor
    graph.add_node(person_id, actor_name)
    actors_to_process = set([person_id])

    # Perform iterations
    for iteration in range(3):  # Two additional iterations
        new_actors_to_process = set()
        # print(f"\nIteration {iteration + 1}:")

        for actor_id in actors_to_process:
            movie_credits = tmdb_api_utils.get_movie_credits_for_person(actor_id, vote_avg_threshold)

            for movie in movie_credits:
                movie_id = movie['id']
                if movie_id in exclude_movie_ids:
                    # Fetch cast and add to excluded_actors
                    cast_data = tmdb_api_utils.get_movie_cast(str(movie_id), None)
                    for cast_member in cast_data:
                        excluded_actors.add(cast_member['id'])
                    continue  # Skip further processing of this movie

                # print(f"Actor ID: {actor_id}, Movie ID: {movie_id}, Title: {movie['title']}")
                cast_data = tmdb_api_utils.get_movie_cast(str(movie_id), credit_limit)

                for cast_member in cast_data:
                    cast_member_id = cast_member['id']
                    if cast_member_id != actor_id and cast_member_id not in excluded_actors:
                        if str(cast_member_id) not in [node[0] for node in graph.nodes]:
                            graph.add_node(str(cast_member_id), cast_member['name'])
                            new_actors_to_process.add(str(cast_member_id))

                        if not any(edge in [(str(actor_id), str(cast_member_id)), (str(cast_member_id), str(actor_id))] for edge in graph.edges):
                            graph.add_edge(str(actor_id), str(cast_member_id))

        actors_to_process = new_actors_to_process

    # Print and write final graph
    print("\nFinal Nodes:")
    for node in graph.nodes:
        print(f"{node[0]}, {node[1]}")
    print("\nFinal Edges:")
    for edge in graph.edges:
        print(f"{edge[0]}, {edge[1]}")

    graph.write_edges_file()
    graph.write_nodes_file()



















