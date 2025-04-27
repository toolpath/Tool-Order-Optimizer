import numpy as np
from scipy.optimize import dual_annealing
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
    """Total weighted circular distance cost for a node→position map."""
    total = 0.0
    for u, v, w in edges:
        total += w * circ_dist(mapping[u], mapping[v], M)
    return total

def extract_circular_nodes_edges(
    seq: List[Any]
) -> Tuple[List[Any], List[Edge]]:
    """
    From a visit sequence on a ring, returns:
      - nodes : unique nodes in first-seen order
      - edges : undirected (u, v, weight) counts including wrap-around
    """
    seen = {}
    nodes = []
    for x in seq:
        if x not in seen:
            seen[x] = True
            nodes.append(x)
    # build wrap-around pairs
    rotated = seq[1:] + seq[:1]
    pairs = list(zip(seq, rotated))
    # canonicalize undirected edges and count
    canon = [(u, v) if u <= v else (v, u) for u, v in pairs]
    counts = Counter(canon)
    edges = [(u, v, w) for (u, v), w in counts.items()]
    return nodes, edges

def solve_with_scipy_annealing(
    nodes: List[Any],
    edges: List[Edge],
    M: int,
    maxiter: int = 1000
) -> Tuple[Dict[Any,int], float]:
    """
    Uses scipy.optimize.dual_annealing to find an injective node→position map.
    """
    k = len(nodes)
    bounds = [(0, M-1)] * k
    # max edge weight for penalty scaling
    max_w = max((w for _,_,w in edges), default=1.0)

    def objective(x):
        # round to integer slots & clip
        xi = np.round(x).astype(int)
        xi = np.clip(xi, 0, M-1)
        # penalty for duplicates
        uniq = np.unique(xi)
        penalty = (k - len(uniq)) * M * max_w
        mapping = {node: pos for node, pos in zip(nodes, xi)}
        return cost_mapping(mapping, edges, M) + penalty

    result = dual_annealing(objective, bounds, maxiter=maxiter)
    x_best = np.round(result.x).astype(int)
    x_best = np.clip(x_best, 0, M-1)
    best_map = {node: pos for node, pos in zip(nodes, x_best)}
    best_cost = cost_mapping(best_map, edges, M)
    return best_map, best_cost

# --- example usage ---
if __name__ == "__main__":
    TOOL_SEQUENCE = [1,13,1,35,17,33,31,29,34,1,37,13,30,8,1,13,8,15]
    M = 28  # your plate size

    # extract nodes & weighted wrap-around edges
    nodes, edges = extract_circular_nodes_edges(TOOL_SEQUENCE)

    # solve via SciPy's dual_annealing
    mapping, cost = solve_with_scipy_annealing(nodes, edges, M, maxiter=5000)

    # display results
    # print("Node→slot mapping:", mapping)
    print("Total circular cost:", cost)

    # derive the circular visitation order
    circ_order = [node for node, _ in sorted(mapping.items(), key=lambda kv: kv[1])]
    print("Order around ring:", circ_order)