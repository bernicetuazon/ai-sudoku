'''
    File name: constraint_prop.py
    Author: Bernice Tuazon
    Date created: 4/5/2018
    Date last modified: 4/12/2018
    Python Version: 3.6

'''

def AC3(csp, queue=None, removals=None):
    """AC3 constraint propagation based on Figure 6.3 in Russell
        Starts with a queue contained with all the arcs in the CSP.
        Makes every variable arc-consistent with all the other variables by
        analyzing an arc (Xi, Xj) and making Xi arc-consistent with Xj.
        Returns true if game has been solved. Otherwise, returns false if 
        no consistent solution is found.
    """

    #if queue is not user-defined, populate queue
    #initially queue contains all the arcs in csp,
    #where an arc is (xi, xj) and xi and xj represent all the nodes
    if queue is None:
        queue = [(xi, xj) for xi in csp.variables for xj in csp.neighbors[xi]]

    while queue:    #if there are still items in the queue
        (xi, xj) = queue.pop()    #get binary constraint
        if revise(csp, xi, xj, removals):   #check if the domain, Di, has changed
            if not csp.domains[xi]: #check if Di is empty
                #immediately return failure since csp has no consistent solution
                return False    
            else:
                #add all the neighbors of xi as an arc to the queue since it
                #allows further reductions of Dk
                for xk in csp.neighbors[xi]:
                    queue.append((xk, xi))  
        #if Di has not changed, continue with the loop
    
    return True

def revise(csp, xi, xj, removals):
    revised = False   
    csp.support_pruning()   #must be called before pruning   
    for x in csp.curr_domains[xi][:]:
        #check if none of the variables for y in Dj satisfies the constraints for x in Di
        if not any(csp.constraints(xi, x, xj, y) for y in csp.curr_domains[xj][:]):
            csp.prune(xi, x, removals) #remove any x in Di if true
            revised = True #true if the domain, Di, is changed
    return revised