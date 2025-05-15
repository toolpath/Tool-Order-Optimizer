import itertools
import random
import math
from collections import Counter
from typing import Any, Dict, List, Tuple

Edge = Tuple[Any, Any, float]

def circ_dist(i: int, j: int, M: int) -> int:
    """Circular distance between i and j on a ring of M slots."""
    d = abs(i - j)
    return min(d, M - d)    

def cost_mapping(
    mapping: Dict[Any, int],
    edges: List[Edge],
    M: int
) -> float:
    """
    Given an injective map node→position, compute total weighted
    circular distance cost.
    """
    total = 0.0
    for u, v, w in edges:
        pi, pj = mapping[u], mapping[v]
        total += w * circ_dist(pi, pj, M)
    return total

def brute_force_circular_positions(
    nodes: List[Any],
    edges: List[Edge],
    M: int
) -> Tuple[Dict[Any,int], float]:
    """
    Exact minimum: try every choice of k positions out of M,
    and every assignment of nodes to them.
    Warning: O( (M choose k) * k! ) → only for k<=8, M small.
    """
    k = len(nodes)
    best_map = {}
    best_cost = float('inf')

    for pos_subset in itertools.combinations(range(M), k):
        # for rotational symmetry you could fix nodes[0] at pos_subset[0]
        for perm in itertools.permutations(nodes):
            mapping = {node: pos for node, pos in zip(perm, pos_subset)}
            c = cost_mapping(mapping, edges, M)
            if c < best_cost:
                best_cost, best_map = c, mapping.copy()

    return best_map, best_cost

def simulated_annealing_circular_positions(
    nodes: List[Any],
    edges: List[Edge],
    M: int,
    iterations: int = 100_000,
    t0: float = 1.0,
    alpha: float = 0.9999
) -> Tuple[Dict[Any,int], float]:
    """
    Heuristic: simulated annealing over injective node→position maps.
    Neighbors either swap two nodes’ positions or move one node into
    a free slot.
    """
    # initial random injective mapping
    all_positions = list(range(M))
    chosen = random.sample(all_positions, len(nodes))
    mapping = {node: pos for node, pos in zip(nodes, chosen)}
    best_map = mapping.copy()
    current_cost = cost_mapping(mapping, edges, M)
    best_cost = current_cost
    T = t0

    for _ in range(iterations):
        # pick a neighbor
        if random.random() < 0.5:
            # swap positions of two random nodes
            u, v = random.sample(nodes, 2)
            mapping[u], mapping[v] = mapping[v], mapping[u]
            new_cost = cost_mapping(mapping, edges, M)
            Δ = new_cost - current_cost
            if Δ < 0 or random.random() < math.exp(-Δ / T):
                current_cost = new_cost
                if new_cost < best_cost:
                    best_cost, best_map = new_cost, mapping.copy()
            else:
                # revert swap
                mapping[u], mapping[v] = mapping[v], mapping[u]
        else:
            # move one node into a random free slot
            u = random.choice(nodes)
            occupied = set(mapping.values())
            free = [p for p in all_positions if p not in occupied]
            if not free:
                continue
            old = mapping[u]
            newp = random.choice(free)
            mapping[u] = newp
            new_cost = cost_mapping(mapping, edges, M)
            Δ = new_cost - current_cost
            if Δ < 0 or random.random() < math.exp(-Δ / T):
                current_cost = new_cost
                if new_cost < best_cost:
                    best_cost, best_map = new_cost, mapping.copy()
            else:
                mapping[u] = old

        T *= alpha

    return best_map, best_cost


def make_nodes_edges(sequence): 
    seq = sequence
    nodes = []
    seen = set()
    for x in seq:
        if x not in seen:
            seen.add(x)
            nodes.append(x)
    rot = seq[1:] + seq[:1]
    pairs = list(zip(seq, rot))

    print("pairs: ", pairs)
    canon = [(u,v) if u<=v else (v,u) for u,v in pairs]
    counts = Counter(canon)
    edges = [(u, v, w) for (u, v), w in counts.items()]

    return nodes, edges


def sa_solve(tool_sequence, M, verbose=True): 

    nodes, edges = make_nodes_edges(tool_sequence)

    # exact (if len(nodes)<=8):
    if len(nodes) <= 8:
        bf_map, bf_cost = brute_force_circular_positions(nodes, edges, M)
        if verbose: 
            print("EXACT mapping:", bf_map, "cost:", bf_cost, "edges: ", edges)

    sa_map, sa_cost = simulated_annealing_circular_positions(nodes, edges, M)
    # derive a circular order by sorting nodes by their assigned position:
    circ_order = sorted(sa_map.items(), key=lambda kv: kv[1])
    # print("Approx mapping:", sa_map)
    sa_tool_order = [node for node, _ in circ_order]

    if verbose: 
        print("Cost   :", sa_cost)
        print("Order around ring:", sa_tool_order)

    return sa_cost, sa_tool_order

# --- example usage ---
if __name__ == "__main__":
    #######################################
    # Edit this to match your tool numbers
    #######################################
    # TOOL_SQUENCE = [1, 13, 1, 35, 17, 33, 31, 29, 34, 1, 37, 13, 30, 8, 1, 13, 8, 15]
    TOOL_SQUENCE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 15, 16]
    M = 28  # Number of pockets you have
    

    sa_solve(TOOL_SQUENCE, M)

