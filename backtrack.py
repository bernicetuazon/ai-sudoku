'''
    File name: backtrack.py
    Author: Bernice Tuazon
    Date created: 4/5/2018
    Date last modified: 4/12/2018
    Python Version: 3.6
'''

#backtrack_util created by Prof. Marie Roch
from csp_lib.backtrack_util import (first_unassigned_variable, 
                                    unordered_domain_values,
                                    no_inference)

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """backtracking_search
    Given a constraint satisfaction problem (CSP),
    a function handle for selecting variables, 
    a function handle for selecting elements of a domain,
    and a set of inferences, solve the CSP using backtrack search
    """

    def backtrack(assignment):
        """Attempt to backtrack search with current assignment
        Returns None if there is no solution.  Otherwise, the
        csp should be in a goal state.
        """
        #check if assignment is complete
        #assignment is complete when every variable is assigned
        #based on code in csp(goal_test)
        if len(assignment) == len(csp.variables):
            return assignment #assignment should be in goal state
        #using first_unassigned- pick the next unassigned variable in the default order
        #using mrv- select unassigned variable with the most constrained value(has smallest domain)
        var = select_unassigned_variable(assignment, csp)  
        #iterate through all values of var
        for val in order_domain_values(var, assignment, csp):   
            #check if val conflicts with any other variable
            if csp.nconflicts(var, val, assignment) == 0:
                #add val to assignment if there are no conflicts
                csp.assign(var, val, assignment)
                #find values that are candidates for removal from domain
                inferences = csp.suppose(var, val)
                #remove all inferences that show to be not consistent
                if inference(csp, var, val, assignment, inferences):
                    csp.assign(var, val, assignment)
                    #check if the current variable is consistent
                    result = backtrack(assignment)
                    if result is not None:
                        return result   #solution has been found
            
            #remove value from assignment since inferences did not work
            csp.unassign(var, assignment)
            #undo all inferences since result returned failure
            csp.restore(inferences)
        return None  #equivalent of returning a failure      
                        
    # Call with empty assignments, variables accessed
    # through dynamic scoping (variables in outer
    # scope can be accessed in Python)
    result = backtrack({})
    #makes sure that complete puzzle is also consistent
    assert result is None or csp.goal_test(result)
    return result
