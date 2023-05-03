class ContactNode:
    """Class used to represent a Contact Node

    Attributes:
        id (int): ID of the Contact Node
        start (float): Start Time
        end (float): End Time
        snd (int): Sender Network Node
        rec (int): Receiver Network Node
        owlt (float): Transmission Delay
        arr_time (float): Arrival Time
        pred (ContactNode): Predecessor Contact Node
        visited_n (list): List of all the visited nodes along the path
        visited (bool): Flag to distinguish between visited and unvisited contacts
    """
    def __init__(self, id, start, end, snd, rec, owlt):
        self.id = id
        self.start = start
        self.end = end
        self.snd = snd
        self.rec = rec
        self.owlt = owlt
        self.arr_time = float('inf')
        self.pred = None
        self.visited_n = []
        self.visited = False