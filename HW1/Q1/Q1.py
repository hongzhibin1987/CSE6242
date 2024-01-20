import http.client
import json
import csv
import requests

class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
            {
      "adult": false,
      "backdrop_path": "/Yotz5R36D7GbELyBQbM7Ot5Ay2.jpg",
      "genre_ids": [
        80,
        18
      ],
      "id": 22073,
      "original_language": "en",
      "original_title": "Hoodlum",
      "overview": "In 1934, the second most lucrative business in New York City was running 'the numbers'. When Madam Queen—the powerful woman who runs the scam in Harlem—is arrested, Ellsworth 'Bumpy' Johnson takes over the business and must resist an invasion from a merciless mobster.",
      "popularity": 14.768,
      "poster_path": "/hZrwqVXLyxxsNJHVc6bJKSUDkXA.jpg",
      "release_date": "1997-08-27",
      "title": "Hoodlum",
      "video": false,
      "vote_average": 6.326,
      "vote_count": 170,
      "character": "Bumpy Johnson",
      "credit_id": "52fe4432c3a368484e015229",
      "order": 0
    },
        :rtype: list
            return a list of dicts, with each dict having 'id', 'title', and 'vote_avg' keys,
            one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
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
        """
               Get the movie cast for a given movie id, with optional parameters to exclude an cast member
               from being returned and/or to limit the number of returned cast members
               documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

               :param string movie_id: a movie_id
               :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
                   e.g., if exclude_ids are [353, 455] then exclude these from any result.
               :param integer limit: maximum number of returned cast members by their 'order' attribute
                   e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
                   If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range).
                   If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
                   If after excluding, the limit is not specified, then return all remaining cast members."
                   e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
                   return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
                   the output is something like this
                {
                  "id": 22073,
                  "cast": [
                    {
                      "adult": false,
                      "gender": 2,
                      "id": 2975,
                      "known_for_department": "Acting",
                      "name": "Laurence Fishburne",
                      "original_name": "Laurence Fishburne",
                      "popularity": 81.012,
                      "profile_path": "/iwx7h0AfWMm9K4sMmhru3ShSra.jpg",
                      "cast_id": 1,
                      "character": "Bumpy Johnson",
                      "credit_id": "52fe4432c3a368484e015229",
                      "order": 0
                    },
                    {
                      "adult": false,
                      "gender": 2,
                      "id": 3129,
                      "known_for_department": "Acting",
                      "name": "Tim Roth",
                      "original_name": "Tim Roth",
                      "popularity": 45.925,
                      "profile_path": "/qSizF2i9gz6c6DbAC5RoIq8sVqX.jpg",
                      "cast_id": 2,
                      "character": "Dutch Schultz",
                      "credit_id": "52fe4432c3a368484e01522d",
                      "order": 1
                    },
                    {
                      "adult": false,
                      "gender": 1,
                      "id": 27011,
                      "known_for_department": "Acting",
                      "name": "Vanessa Williams",
                      "original_name": "Vanessa Williams",
                      "popularity": 53.698,
                      "profile_path": "/30O1Af0wy6UBt8EpVRuq28tTGoT.jpg",
                      "cast_id": 3,
                      "character": "Francine Hughes",
                      "credit_id": "52fe4432c3a368484e015231",
                      "order": 2
                    },
                    {
                      "adult": false,
                      "gender": 2,
                      "id": 1271,
                      "known_for_department": "Acting",
                      "name": "Andy García",
                      "original_name": "Andy García",
                      "popularity": 58.49,
                      "profile_path": "/aRooE4lECWf0YXd2NefeM4Wu4rn.jpg",
                      "cast_id": 4,
                      "character": "Lucky Luciano",
                      "credit_id": "52fe4432c3a368484e015235",
                      "order": 3
                    },
               :rtype: list
                   return a list of dicts, one dict per cast member with the following structure:
                       [{'id': '97909' # the id of the cast member
                       'character': 'John Doe' # the name of the character played
                       'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                       Note that this is an example of the structure of the list and some of the fields returned by the API.
                       The result of the API call will include many more fields for each cast member.
               """
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
            full_cast_data = [member for member in full_cast_data if member['order'] < limit]

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
"""
if __name__ == "__main__":

    person_id = '2975'
    person_name = 'Laurence Fishburne'
    vote_avg_threshold = 8.0
    credit_limit = 2
    graph = Graph()
    graph.add_node(person_id, person_name)
    tmdb_api_utils = TMDBAPIUtils(api_key='14386f6d2560c16967a0141156e72327')
    movie_credits = tmdb_api_utils.get_movie_credits_for_person(person_id, vote_avg_threshold)

    # Print movie credits
    print(f"Movie Credits for Person ID {person_id} (Laurence Fishburne):")
    for credit in movie_credits:
        print(credit)
    print("\n")  # Add a newline for better separation

    # Building the graph
    new_nodes = set()
    for movie in movie_credits:
        movie_id = movie['id']
        cast_data = tmdb_api_utils.get_movie_cast(str(movie_id), credit_limit)

        for cast_member in cast_data:
            if cast_member['id'] != person_id:  # Avoid adding the person of interest to themselves
                graph.add_node(cast_member['id'], cast_member['name'])
                new_nodes.add(cast_member['id'])
                graph.add_edge(person_id, cast_member['id'])

    # Print nodes and edges for debugging
    print("Nodes:")
    for node in graph.nodes:
        print(f"{node[0]}, {node[1]}")
    print("\nEdges:")
    for edge in graph.edges:
        print(f"{edge[0]}, {edge[1]}")

    graph.write_edges_file()
    graph.write_nodes_file()
"""
if __name__ == "__main__":
    person_id = '2975'
    person_name = 'Laurence Fishburne'
    vote_avg_threshold = 8.0
    credit_limit = 2
    graph = Graph()
    tmdb_api_utils = TMDBAPIUtils(api_key='14386f6d2560c16967a0141156e72327')
    movie_credits = tmdb_api_utils.get_movie_credits_for_person(person_id, vote_avg_threshold)

    # Manually add Laurence Fishburne to ensure he is the first node
    graph.add_node(person_id, person_name)

    # Building the graph
    # Iterate through each movie credit
    for movie in movie_credits:
        movie_id = movie['id']  # Get the movie ID
        # Get the cast data for the movie, limited to the specified number of cast members
        cast_data = tmdb_api_utils.get_movie_cast(str(movie_id), credit_limit)

        # Iterate through each cast member
        for cast_member in cast_data:
            cast_member_id = cast_member['id']  # Get the cast member ID

            # Skip adding the node if the cast member ID is the same as the person of interest
            # or if the cast member ID is already a node in the graph
            if cast_member_id == person_id or any(node[0] == cast_member_id for node in graph.nodes):
                continue

            # Add the cast member as a new node
            graph.add_node(cast_member_id, cast_member['name'])

            # Add an edge from the person of interest to the cast member
            # but only if the edge does not already exist in the graph
            # The check for self-referential edges is not necessary here as we continue earlier if IDs match
            if not any(
                    edge == (person_id, cast_member_id) or edge == (cast_member_id, person_id) for edge in graph.edges):
                graph.add_edge(person_id, cast_member_id)

    # Print nodes and edges for debugging
    print("Nodes:")
    for node in graph.nodes:
        print(f"{node[0]}, {node[1]}")
    print("\nEdges:")
    for edge in graph.edges:
        print(f"{edge[0]}|{edge[1]}")

    graph.write_edges_file()
    graph.write_nodes_file()







