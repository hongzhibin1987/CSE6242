import http.client
import json
import csv
import requests

class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.api_key}&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return []

        cast_data = response.json()['cast']

        # Apply exclude_ids filter
        if exclude_ids:
            cast_data = [member for member in cast_data if member['id'] not in exclude_ids]

        # Apply limit
        if limit is not None:
            cast_data = cast_data[:limit]

        return cast_data

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, with each dict having 'id', 'title', and 'vote_avg' keys, 
            one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        return NotImplemented

def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return NotImplemented


# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.




class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
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
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        return NotImplemented


    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        return NotImplemented


    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return NotImplemented


    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return NotImplemented


    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        return NotImplemented


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


if __name__ == "__main__":

    person_id = '2975'
    person_name = 'Laurence Fishburne'
    graph = Graph()
    graph.add_node(person_id, person_name)
    tmdb_api_utils = TMDBAPIUtils(api_key='14386f6d2560c16967a0141156e72327')
    movie_credits = tmdb_api_utils.get_movie_credits_for_person(person_id)
    for credit in movie_credits:
        print(credit)
    # call functions or place code here to build graph (graph building code not graded)

    # Suggestion: code should contain steps outlined above in BUILD CO-ACTOR NETWORK

    #graph.write_edges_file()
    #graph.write_nodes_file()

    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    # graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")
