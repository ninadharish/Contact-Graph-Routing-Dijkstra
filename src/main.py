from contactnode import ContactNode
from queue import PriorityQueue


def createContactGraph(ContactList_data):
    """Creates a List of all the Contact Nodes

    Args:
        ContactList_data (str): Address of the '.txt' file with information about all the Contact Nodes

    Returns:
        G (list): List with all the Contact Nodes
    """

    # Initialize Empty List
    G = []

    # Read Contact List Text file line by line
    with open(ContactList_data) as f:
        for line in f:
            node_atts = line.split()
            # Use each attribute to create a Contact Node and append in G
            id = int(node_atts[0])
            start = float(node_atts[1])
            end = float(node_atts[2])
            snd = int(node_atts[3])
            rec = int(node_atts[4])
            owlt = float(node_atts[5])

            G.append(ContactNode(id, start, end, snd, rec, owlt))

    return G



def CGR(G, C_root, dst, q):
    """Contact Graph Dijkstra Search

    Args:
        G (list): List with all the Contact Nodes
        C_root (ContactNode): Root Contact Node
        dst (int): Destination Network Node
        q (PriorityQueue): Priority Queue for Dijkstra's Algorithm

    Returns:
        C_fin (ContactNode): Final Contact Node
        BDT (float): Best-case Delivery Time
    """

    # Initialize Best-case Delivery Time, Final Contact Node and Current Contact Node 
    BDT = float('inf')
    C_fin = None
    C_curr = C_root

    while True:

        C_fin, BDT = CRP(G, C_curr, C_fin, dst, BDT, q)
        C_curr = CSP(G, BDT, q)

        # Exit the loop if there is no node under consideration
        if (C_curr == None):
            break

    return C_fin, BDT



def CRP(G, C_curr, C_fin, dst, BDT, q):
    """Contact Review Procecure

    Args:
        G (list): List with all the Contact Nodes
        C_curr (ContactNode): Current Contact Node under Consideration
        C_fin (ContactNode): Final Contact Node
        dst (int): Destination Network Node
        BDT (float): Best-case Delivery Time
        q (PriorityQueue): Priority Queue for Dijkstra's Algorithm

    Returns:
        C_fin (ContactNode): Updated Final Contact Node
        BDT (float): Updated Best-case Delivery Time
    """

    # Loop over each Contact Node
    for C in G:
        # Consider only those nodes whose sender is not the current node's receiver, end time is greater than current node's arrival time, is not visited and is not present on the current path
        if ((C.snd != C_curr.rec) or (C.end < C_curr.arr_time) or (C.visited) or (C.rec in C_curr.visited_n)):
            continue

        # Update arrival time
        arr_time = max(C_curr.arr_time, C.start) + C.owlt

        # If arrival time is less than the node's arrival time, update attributes
        if (arr_time < C.arr_time):
            C.arr_time = arr_time
            C.pred = C_curr
            C.visited_n = C_curr.visited_n + [C.rec]
            # Push the node into the Priority Queue using its arrival time as the key
            q.put((C.arr_time, C.id))

            # If the node's receiver is the destination, update BDT and final contact node
            if ((C.rec == dst) and (C.arr_time < BDT)):
                BDT = C.arr_time
                C_fin = C

    # Set the visited flag of the current node to be True
    C_curr.visited = True

    return C_fin, BDT



def CSP(G, BDT, q):
    """Contact Selection Procedure

    Args:
        G (list): List with all the Contact Nodes
        BDT (float): Best-case Delivery Time
        q (PriorityQueue): Priority Queue for Dijkstra's Algorithm

    Returns:
        C_curr (ContactNode): Updated Current Contact Node under Consideration
    """

    # If queue is empty, no nodes are considered
    if (q.empty()):
        return None

    C_curr = None

    # Pop elements until the queue is either empty or the first is not visited
    while((not q.empty()) and (G[q.queue[0][1]-1].visited)):
        # If the first element's arrival time is greater than BDT, means all other elements' arrival time is also greater than BDT and hence no element is considered
        if ((G[q.get()[1] - 1]).arr_time > BDT):
            return None
    
    # Set C_curr to be the top element of the Priority Queue with the minimum arrival time
    C_curr = G[q.get()[1] - 1]

    return C_curr


def BackTrack(C_fin):
    """Backtracking after Reaching the Destination

    Args:
        C_fin (ContactNode): Final Contact Node

    Returns:
        network_node_list (list): List of Network Nodes on the Best Path
        contact_node_list (list): List of Contact Nodes on the Best Path
    """

    # Initialize Lists
    network_node_list = []
    contact_node_list = []

    C = C_fin

    # Backtrack until the Root element is reached and append to the lists
    while (C.pred != None):
        
        network_node_list.append(C.rec)
        contact_node_list.append(C.id)

        C = C.pred

    network_node_list.append(C.rec)
    contact_node_list.append(C.id)

    # Reverse List to represend Source to Destination
    network_node_list.reverse()
    contact_node_list.reverse()

    return network_node_list, contact_node_list



def dijkstra_plan(src, dst, ContactList_data):
    """Plan Path from Source to Destination using Dijkstra's Search Algorithm

    Args:
        src (int): Source Network Node
        dst (int): Destination Network Node
        ContactList (str): Address of the '.txt' file with information about all the Contact Nodes

    Returns:
        network_node_list (list): List of Network Nodes on the Best Path
        contact_node_list (list): List of Contact Nodes on the Best Path
        BDT (float): Best-case Delivery Time
    """

    # Create Contact Graph
    G = createContactGraph(ContactList_data)

    # Initialize Root Node with Arrival time = 0
    C_root = ContactNode(0, 0, float('inf'), src, src, 0)
    C_root.arr_time = 0

    # Initialize Priority Queue
    q = PriorityQueue()

    # Contact Graph Dijkstra Search
    C_fin, BDT = CGR(G, C_root, dst, q)

    print('Path Found', '\n')

    # BackTrack
    node_list, contact_list = BackTrack(C_fin)

    return node_list, contact_list, BDT




if __name__ == "__main__":

    src = 1
    dst = 12
    ContactList_path = '../data/ContactList.txt'

    print('Source Network Node:', src)
    print('Destination Network Node:', dst, '\n')

    node_list, contact_list, BDT = dijkstra_plan(src, dst, ContactList_path)


    print('Contact Node List IDs:', contact_list, '\n')

    print('Network Node List:', node_list, '\n')

    print('Best-case Delivery Time:', BDT)