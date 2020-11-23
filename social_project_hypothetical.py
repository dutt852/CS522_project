#SUBMITTED BY:
# CHIRANJIV DUTT (2019CSB1083)
# GAUTAM MANOCHA (2019CSB1086)
# KSHITIZ ARORA  (2019CSB1095)

import networkx as nx
import random
import matplotlib.pyplot as plt

def create_graph(num_people,prob_quality_depenent): # to create a graph
    G=nx.Graph()
    G.add_nodes_from([x for x in range(num_people)]); # adding people to the graph
    for i in range(num_people):
        G.nodes[i]['type']='people' # assigning type to people
    # adding two parties initially
    G.add_node('party1')
    G.add_node('party2')
    # assigning them types
    G.nodes['party1']['type']='party'
    G.nodes['party2']['type']='party'
    
    # assigning Quality factor to them
    G.nodes['party1']['Q-factor']=random.randint(40,50)
    G.nodes['party2']['Q-factor']=random.randint(40,50)
    
    Q1=G.nodes['party1']['Q-factor']
    Q2=G.nodes['party2']['Q-factor']
    
    lst_of_parties=['party1','party2']
    probabily_first_party=float(Q1)/(Q1+Q2) # probability to go to first party
    
    for i in range(num_people): # assigning people to one of the parties
        rn1=random.random()
        if rn1<=prob_quality_depenent: # depending on quality factor
            rn=random.random()
            if rn<=probabily_first_party:
                G.add_edge(i,'party1')
                G.nodes[i]['party']='party1'
            else:
                G.add_edge(i,'party2')
                G.nodes[i]['party']='party2'
        else: # randomly
            ran=random.choice(['party1','party2'])
            G.add_edge(i,ran)
            G.nodes[i]['party']=ran
    return G,lst_of_parties

def iterate(G,num_iterations,lst_of_parties,parties_added,const_for_change,num_people): # varying Q-factor and choices of people
    
    plot_lst_Q_factors = [[] for p in range(parties_added)]

    plot_lst_degree = [[] for p in range(parties_added)]

    lst_for_change=[G.nodes[x]['Q-factor']/100 for x in lst_of_parties] # initial change probability

    k = 0
    
    for n in range(parties_added):
        i = 'party'+str(n+1)
        if i in lst_of_parties:
            plot_lst_Q_factors[k].append(G.nodes[i]['Q-factor'])
            plot_lst_degree[k].append(G.degree(i)/100)
        else:
            plot_lst_Q_factors[k].append(0)
            plot_lst_degree[k].append(0)
        k+=1


    for j in range(num_iterations): 
        print("=",end="")
        ind=0 # to know which party is it
        for n in range(parties_added): # go to each party 
            i = 'party'+str(n+1)
            if i in lst_of_parties:
                Q=float(G.nodes[i]['Q-factor'])
                rate_change=((min(Q/100,(1-Q/100)))*(100-j))/(const_for_change*100) # rate of change 
                range_change=[Q-(rate_change*100),Q+(rate_change*100)]  # range for change
                rn=random.random()
                rn1=0
                if rn<=0.02: # if we need to change the probability of change 
                    rn1=random.random()
                    lst_for_change[ind]=rn1
                else:
                    rn1=lst_for_change[ind]
                if rn1<=Q/100: # it shall decrease
                    G.nodes[i]['Q-factor']=random.uniform(range_change[0],Q)
                else: # it shall increase
                    G.nodes[i]['Q-factor']=random.uniform(Q,range_change[1])


                plot_lst_Q_factors[n].append(G.nodes[i]['Q-factor'])
                ind+=1

            else:
                plot_lst_Q_factors[n].append(0)

        

        party_and_qfac=[] # list for name of party and its q factor
        for i in lst_of_parties:
            party_and_qfac.append([G.nodes[i]['Q-factor'],i])
        party_and_qfac.sort(key=lambda x:x[0],reverse=True) # sorted
        party_and_change={x[1]:(10+party_and_qfac[0][0]-x[0])/100 for x in party_and_qfac} # probability for people in that party to change the party 
        top_parties=[x[1] for x in party_and_qfac[:min(3,len(party_and_qfac))]] # getting the top parties depending on the Q-factor of the parties
        prob_top=[]
        sum_qfac=0
        partial_sum_qfac=0
        # calculating sums and partial sums for shuffling people in top 3
        for i in top_parties:
            sum_qfac+=G.nodes[i]['Q-factor']
        for i in top_parties:
            partial_sum_qfac+=G.nodes[i]['Q-factor']
            prob_top.append(partial_sum_qfac/sum_qfac)
        for i in range(num_people): # shuffle the people
            rn=random.random()
            if (rn<=party_and_change[G.nodes[i]['party']]): # shuffle to top three depending on the probbilty assigned above
                G.remove_edge(i,G.nodes[i]['party'])
                rn1=random.random()
                if rn1<prob_top[0]:
                    G.nodes[i]['party']=top_parties[0]
                elif prob_top[0]<=rn1<prob_top[1] and len(top_parties)>1:
                    G.nodes[i]['party']=top_parties[1]
                elif prob_top[1]<=rn1<1 and len(top_parties)>2:
                    G.nodes[i]['party']=top_parties[2]
                G.add_edge(i,G.nodes[i]['party'])
        ind = 0    
        for n in range(parties_added):
            i = 'party'+str(n+1)
            if i in lst_of_parties:
                plot_lst_degree[n].append(G.degree(i)/100)
            else:
                plot_lst_degree[n].append(0)
            ind+=1

    ruling_party = lst_of_parties[0]
    for i in lst_of_parties: # finding the rulling party
        if G.degree(i) > G.degree(ruling_party):
            ruling_party = i
    print()
    print("Ruling Party: ", ruling_party,"Top Parties: ", top_parties)


    return G, plot_lst_Q_factors, plot_lst_degree


def add_party(G, lst_of_parties, parties_added, num_people): # adding a new party in to the system

    new_party = 'party'+str(parties_added+1)
    G.add_node(new_party)
    G.nodes[new_party]['type'] = 'party'
    G.nodes[new_party]['Q-factor'] = random.randint(20, 40) # assigning Q-factor to it
    Q1 = G.nodes[new_party]['Q-factor']
    lst_of_parties.append(new_party)

    for i in range(num_people): # shifting people to new party
        Q2 = G.nodes[G.nodes[i]['party']]['Q-factor']
        prob_for_shift = Q1/(Q1+Q2)*0.2 # probability to shift to the new party
        
        rn1 = random.random()
        if rn1 < prob_for_shift:
            G.remove_edge(i, G.nodes[i]['party'])
            G.nodes[i]['party'] = new_party
            G.add_edge(i, G.nodes[i]['party'])


    return G, lst_of_parties


def delete_party(G, lst_of_parties, num_people, prev_record, present_record): # deleting a party

    to_be_deleted = []
# check for each party for its last 3 tenures if its number of followers were always less than some threshold delete it
    for i in lst_of_parties:
        
        if (i in prev_record) and (len(prev_record[i])>1):
            
            if max(prev_record[i][0], prev_record[i][1], present_record[i]) < 500:
                to_be_deleted.append(i)
            else:
                # maintining the record
                prev_record[i][0] = prev_record[i][1]
                prev_record[i][1] = present_record[i]

        else:

            if i not in prev_record:
                prev_record[i] = [present_record[i]]

            else:
                prev_record[i].append(present_record[i])

    new_lst_of_parties = [x for x in lst_of_parties if x not in to_be_deleted]

    for p in to_be_deleted: # delete the party and assign its followers to others

        followers = list(G.neighbors(p))

        for i in followers:
            G.remove_edge(i, p)
            G.nodes[i]['party'] = random.choice(new_lst_of_parties)
            G.add_edge(i, G.nodes[i]['party'])
    if len(to_be_deleted)>0:
        print("Resigned Parties", to_be_deleted)
    return G, new_lst_of_parties



    




def run_project(total_parties, total_iterations): # Function to run the whole of the code

    num_people = 10000
    num_iter = 100

    G = nx.Graph()
    
    prev_record = {}
    present_record = {}

    parties_added = 0

    G, lst_of_parties = create_graph(num_people, 0.8)
    parties_added+=2

    for p in lst_of_parties:
        present_record[p] = G.degree(p)

    plot_qf = [[] for _ in range(total_parties)]

    plot_deg = [[] for _ in range(total_parties)]

    G, lst_of_parties = delete_party(G, lst_of_parties, num_people, prev_record, present_record)
    G, add_qf, add_deg = iterate(G, num_iter, lst_of_parties, parties_added, 10, num_people)
    for k in range(2):
        plot_qf[k] += add_qf[k]
        plot_deg[k] += add_deg[k]
    for k in range(2, total_parties):
        plot_qf[k] += [0 for _ in range(num_iter)]
        plot_deg[k] += [0 for _ in range(num_iter)]

    for i in range(3, total_iterations):
        if i <= total_parties:
            G, lst_of_parties = add_party(G, lst_of_parties, parties_added, num_people)
            parties_added+=1
        for p in lst_of_parties:
            present_record[p] = G.degree(p)
        G, lst_of_parties = delete_party(G, lst_of_parties, num_people, prev_record, present_record)
        G, add_qf, add_deg = iterate(G, num_iter, lst_of_parties, parties_added, 10, num_people)
        for k in range(min(i, total_parties)):
            plot_qf[k] += add_qf[k]
            plot_deg[k] += add_deg[k]
        for k in range(min(i, total_parties), total_parties):
            plot_qf[k] += [0 for _ in range(num_iter)]
            plot_deg[k] += [0 for _ in range(num_iter)]
    



    G, lst_of_parties = delete_party(G, lst_of_parties, num_people, prev_record, present_record)

    colors = ['green', 'red', 'yellow', 'blue', 'black', 'cyan', 'purple', 'brown', 'pink']

    plt.xlabel('Number of Iterations')
    plt.ylabel('Values')

    for i in range(total_parties):
        plt.plot(plot_qf[i], color = colors[i])
        plt.plot(plot_deg[i], color = colors[i], linestyle = '--')
    
    plt.legend(('Q-factor', 'Followers/100'), loc=0)

    plt.show()

    return 0

run_project(9, 40)
