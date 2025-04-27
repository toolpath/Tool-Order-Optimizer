import unittest 

from tool_ordering import sa_solve, cost_mapping, make_nodes_edges

def is_rotation(seq, target):
    """
    Return True if seq is a rotation of target.
    """
    if len(seq) != len(target):
        return False
    # print("foo")
    doubled = target + target
    # look for seq as a contiguous slice in doubled
    for i in range(len(target)):
        if doubled[i:i+len(seq)] == seq:
            return True
    return False

def is_circular_equivalent(seq, target):
    """
    Return True if seq is either
      - a rotation of target, or
      - a rotation of the reverse of target.
    """
    return is_rotation(seq, target) or is_rotation(seq, target[::-1])


class TestToolOrdering(unittest.TestCase): 


    def test_cost_mapping(self): 

        seq = [1,2,1,3,1,4,1,2]
        edges = [(1, 2, 4), (1, 3, 2), (1, 4, 2)]

        #################################
        # Case 1 -- optimal for M=4
        #################################

        order = [1, 2, 3, 4] 
        mapping = {T:i for (i,T) in enumerate(order)}
        M = 4 # no empty positions
        expected_cost = sum([1,1,2,2,1,1,1,1])
        cost = cost_mapping(mapping, edges, 4)

        M = 5 # 1 empty position 
        expected_cost = sum([1,1,2,2,2,2,1,1])
        cost = cost_mapping(mapping, edges, 5)

        #################################
        # Case 2 -- not optimal for M=4
        #################################

        self.assertEqual(cost, expected_cost)

        M = 4 # no empty positions
        order = [1, 4, 2, 3]
        expected_cost = sum([2,2,1,1,1,1,2,2])
        mapping = {T:i for (i,T) in enumerate(order)}
        cost = cost_mapping(mapping, edges, M)
        self.assertEqual(cost, expected_cost)


        M = 10 # 6 empty positions
        order = [1, 4, 2, 3]
        expected_cost = sum([2,2,3,3,1,1,2,2]) # should not circle around the long way!
        mapping = {T:i for (i,T) in enumerate(order)}
        cost = cost_mapping(mapping, edges, M)
        self.assertEqual(cost, expected_cost)


    def test_full_turret(self): 
        M = 5
        seq = [1,2,1,4]

        cost, order = sa_solve(seq, M, verbose=False)

        expected_order = [4,1,2]

        self.assertEqual(cost, 4)

        self.assertTrue(is_circular_equivalent(order, expected_order))



        M = 4
        seq = [1,2,1,3,1,4,1,2]

        cost, order = sa_solve(seq, M, verbose=False)

        expected_order = [4,1,2]

        # self.assertEqual(cost, 4)

        # self.assertTrue(is_circular_equivalent(order, expected_order))

        print(cost, order)

        mapping = {1: 0, 4: 1, 2: 2, 3: 3}
        edges = [(1, 2, 4), (1, 3, 2), (1, 4, 2)]

        test_cost = cost_mapping(mapping, edges, M)
        print("test_cost: ", test_cost)

if __name__ == "__main__": 
    unittest.main()


    