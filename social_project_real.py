#SUBMITTED BY:
# CHIRANJIV DUTT (2019CSB1083)
# GAUTAM MANOCHA (2019CSB1086)
# KSHITIZ ARORA  (2019CSB1095)

import networkx as nx
import matplotlib.pyplot as plt
import random


def create_graph(num_people,prob_quality_depenent,lst_for_change):
    G=nx.Graph() # creating a directed graph
    G.add_nodes_from([x for x in range(num_people)]); # adding nodes for people
    for i in range(num_people):
        G.nodes[i]['type']='people' # assigning an attribute "type" which would to differentiate later
    # adding two parties initially and assigning thier attribute 
    G.add_node('party1')
    G.add_node('party2')
    G.nodes['party1']['type']='party'
    G.nodes['party2']['type']='party'
    
    # assigning quality factor to the parties(quality factor is higher for a party doing good works)
    G.nodes['party1']['Q-factor']=random.randint(30,50)
    G.nodes['party2']['Q-factor']=random.randint(30,50)
    
    Q1=G.nodes['party1']['Q-factor']
    Q2=G.nodes['party2']['Q-factor']

    lst_for_change['party1'] = Q1/300
    lst_for_change['party2'] = Q2/300
    
    lst_of_parties=['party1','party2'] # a list to maintain active parties
    probabily_first_party=float(Q1)/(Q1+Q2) # probabilty to choose first party
    
    for i in range(num_people): # assigning all teh peolpe one of the parties depending on the probability calculated
        rn1=random.random()
        if rn1<=prob_quality_depenent: # with some probabilty assigning on the basis of Q-factor
            rn=random.random()
            if rn<=probabily_first_party:
                G.add_edge(i,'party1')
                G.nodes[i]['party']='party1'
            else:
                G.add_edge(i,'party2')
                G.nodes[i]['party']='party2'
        else: # randomly choosing one
            ran=random.choice(['party1','party2'])
            G.add_edge(i,ran)
            G.nodes[i]['party']=ran
    # we have got graph with people following parties
    return G,lst_of_parties


def add_frndships(G,lst_of_parties,prob_frndship_inside,prob_frndship_across,num_frndship_within,num_frndship_across,common_friends): # function to add friendships among people
    for i in range(num_frndship_within): # adding friendships among people of same party
        rn1=random.random()
        if rn1<=prob_frndship_inside: # with some probability provided
            party=random.choice(lst_of_parties) # randomly choose one of the parties
            lst_neighbors=list(G.neighbors(party)) # get to know who are followers
            if (len(lst_neighbors) > 0): # if the party has some followers
                # choose two people to make them friends
                per1=random.choice(lst_neighbors)
                per2=random.choice(lst_neighbors)
                if G.has_edge(per1, per2)==0: # if there is no edge initially between them
                    G.add_edge(per1,per2) # add edge between them
                    common_friends[per1][party] = common_friends[per1].get(party, 0)+1 # maintain number of friends for each in this party
                    common_friends[per2][party] = common_friends[per2].get(party, 0)+1
    for i in range(num_frndship_across): # adding friendhips among people of different parties
        rn2=random.random() # with some probability
        if rn2<=prob_frndship_across:
            # choose 2 parties randomly
            party1=random.choice(lst_of_parties)
            party2=random.choice(lst_of_parties)
            if (party1!=party2): # if the chosen ones are different
                if len(list(G.neighbors(party1))) and len(list(G.neighbors(party2))): # and both of them has followers
                    # choosing 2 people randomly one from each
                    per1 = random.choice(list(G.neighbors(party1)))
                    per2 = random.choice(list(G.neighbors(party2)))
                    if G.has_edge(per1, per2)==0: # check if they alresy have any edge between them
                        G.add_edge(per1, per2) # add edge between them
                        common_friends[per1][party2] = common_friends[per1].get(party2, 0)+1 # maintain number of friends for each in these parties
                        common_friends[per2][party1] = common_friends[per2].get(party2, 0)+1
                    


def iterate(G,lst_of_parties,parties_added,const_for_change,num_iterations,num_people,prob_frnd_change,common_friends,lst_for_change,prob_no_change): # Q-factor fluctuations and followers shifting among parties
    # some lists for plotting afterwards
    plot_lst_Q_factors = [[] for p in range(parties_added)]
    plot_lst_degree = [[] for p in range(parties_added)]


    k = 0
    # again for plotting the graph
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
        
        add_frndships(G,lst_of_parties,0.7,0.2,2000,5,common_friends) # add some friends among the people every iteration
        print("=",end="")
        

        for n in range(parties_added): # for fluctuations in Q-factor
            i = 'party'+str(n+1)
            if i in lst_of_parties:
                Q=float(G.nodes[i]['Q-factor'])
                rate_change1=(Q/100)*(100-j)/(const_for_change*100) # rate of change for decreasing 
                rate_change2=(1-(Q/100))*(100-j)/(const_for_change*100) # rate of change for increasing
                range_change=[Q-(rate_change1*Q),Q+(rate_change2*Q)] # range for change
                rn=random.random()
                rn1=0
                # we tried to keep the random number generated for probabilty of change to be same for most of the times so that there should be more of increase if increasing and vice versa
                if rn<=0.02: # if we need to change the probability of change 
                    rn1=random.random()
                    lst_for_change[i]=rn1 # maintaining list of previous random number
                else:
                    rn1=lst_for_change[i]
                if rn1<=Q/100: # it shall decreae
                    G.nodes[i]['Q-factor']=random.uniform(range_change[0],Q)
                else: # it shall increase
                    G.nodes[i]['Q-factor']=random.uniform(Q,range_change[1])

                plot_lst_Q_factors[n].append(G.nodes[i]['Q-factor'])

            
            else:
                plot_lst_Q_factors[n].append(0)


 
        
        party_and_qfac=[] # list for name of party and its q factor
        for i in lst_of_parties:
            party_and_qfac.append([G.nodes[i]['Q-factor'],i])
        party_and_qfac.sort(key=lambda x:x[0],reverse=True) # sorted
        party_and_change={x[1]:(10+party_and_qfac[0][0]-x[0])/100 for x in party_and_qfac} # probabilty for each person to change from this party to some other
        top_parties=[x[1] for x in party_and_qfac[:min(3,len(party_and_qfac))]] # list for top 3 parties
        prob_top=[]
        sum_qfac=0
        partial_sum_qfac=0
        # finding sum and partial sums for knowing the probabiltiy of going into which of the top 3 parties
        for i in top_parties:
            sum_qfac+=G.nodes[i]['Q-factor']
        for i in top_parties:
            partial_sum_qfac+=G.nodes[i]['Q-factor']
            prob_top.append(partial_sum_qfac/sum_qfac)
        

        for i in range(num_people): # shuffle the people
            rn1 = random.random()
            if rn1<prob_frnd_change: # this is probabiltiy to change on the basisi of friendships and Q-factor
                P = G.nodes[i]['party']
                Q = G.nodes[P]['Q-factor']
                for p in lst_of_parties: # go to all the parties and check if you wanna go there
                    if p!=G.nodes[i]['party']:
                        if Q*(common_friends[i].get(P,1)) < (G.nodes[p]['Q-factor']-Q-20)*(common_friends[i].get(p,0)): # getting to know if person will go to this party of not
                            P = p
                            Q = G.nodes[p]['Q-factor']
                
                shift(G, i, common_friends, G.nodes[i]['party'], P) # shifting to new party

            elif rn1<(1-prob_no_change): # with very less probability going to top three parties
                rn=random.random()
                if (rn<=party_and_change[G.nodes[i]['party']]):
                    prev_party = G.nodes[i]['party']
                    rn1=random.random()
                    if rn1<prob_top[0]:
                        G.nodes[i]['party']=top_parties[0]
                    elif prob_top[0]<=rn1<prob_top[1] and len(top_parties)>1:
                        G.nodes[i]['party']=top_parties[1]
                    elif prob_top[1]<=rn1<1 and len(top_parties)>2:
                        G.nodes[i]['party']=top_parties[2]
                    new_party = G.nodes[i]['party']
                    shift(G, i, common_friends, prev_party, new_party) # shifting to new party
        ind = 0
        for n in range(parties_added):
            i = 'party'+str(n+1)
            if i in lst_of_parties:
                plot_lst_degree[n].append(G.degree(i)/100)
            else:
                plot_lst_degree[n].append(0)
            ind+=1
    print()
    party_and_followers=[[x,len(list(G.neighbors(x)))] for x in lst_of_parties]
    rulling_party=max(party_and_followers,key=lambda x:x[1])
    
    print("Rulling Party:",rulling_party[0],"Top Parties",top_parties) # rulling party is the one which has maximum followers adn top parties will be the ones with maximum Q-factor

    return G, plot_lst_Q_factors, plot_lst_degree


def shift(G, i, common_friends, prev_party, new_party): # for shifting to new party basically maintaining the frndships in each party
    if new_party!=prev_party:
        if G.has_edge(i,prev_party):
            G.remove_edge(i,prev_party)
        G.add_edge(i,new_party)
        G.nodes[i]['party'] = new_party
        for fr in G.neighbors(i): # go to neighbor of person and change their status of friendships in those parties
            if G.nodes[fr]['type'] == 'people':
                common_friends[fr][prev_party]-=1
                common_friends[fr][new_party]=common_friends[fr].get(new_party,0)+1



def add_party(G, lst_of_parties, parties_added, num_people, num_random_shift, common_friends, lst_for_change): # adding a new party

    new_party = 'party'+str(parties_added+1)
    G.add_node(new_party)
    G.nodes[new_party]['type'] = 'party'
    G.nodes[new_party]['Q-factor'] = random.uniform(30+(parties_added-1)*2, 40+(parties_added-1)*2) # assigning Q-factor to it which keeps on oncreasing for successive parties
    Q1 = G.nodes[new_party]['Q-factor']
    lst_for_change[new_party] = Q1/300
    lst_of_parties.append(new_party)

    
    people_random_shift = random.sample(list(i for i in range(num_people)), num_random_shift) # taking a subset of people
    for i in people_random_shift: # shifting them to new party
        shift(G, i, common_friends, G.nodes[i]['party'], new_party)


    for i in range(num_people): # check for rest of them if they would go or not
        if G.nodes[i]['party'] != new_party:
            P = G.nodes[i]['party']
            Q = G.nodes[P]['Q-factor']
            if Q*(common_friends[i].get(P,1)) < G.nodes[new_party]['Q-factor']*(common_friends[i].get(new_party,1)):
                P = new_party
                Q = G.nodes[new_party]['Q-factor']
    
            shift(G, i, common_friends, G.nodes[i]['party'], P)

    return G, lst_of_parties

def delete_party(G, lst_of_parties, num_people, prev_record, present_record, common_friends): # deleting a party
    to_be_deleted = []
    # check for their previous 3 tenure records if they have followers less than a particular threshold in all of them delete it
    for i in lst_of_parties:
        
        if (i in prev_record) and (len(prev_record[i])>2):
            
            if max(prev_record[i][0], prev_record[i][1], prev_record[i][2], present_record[i]) < 500:
                to_be_deleted.append(i)
            else: # maintaining the record
                
                prev_record[i][0] = prev_record[i][1]
                prev_record[i][1] = prev_record[i][2]
                prev_record[i][2] = present_record[i]
                
        else:
            
            if i not in prev_record:
                prev_record[i] = [present_record[i]]
            
            else:
                prev_record[i].append(present_record[i])
    new_lst_of_parties = [x for x in lst_of_parties if x not in to_be_deleted]
    for p in to_be_deleted: # shifting the people of party which is deleting
        
        followers = list(G.neighbors(p))
        
        for i in followers:
            
            com_frnd_lst=[[common_friends[i].get(j,0),j] for j in new_lst_of_parties]
            new_party=max(com_frnd_lst,key=lambda x:x[0])[1] # shifting to the party where they hve most of their friends
            shift(G, i, common_friends, p, new_party)
    if len(to_be_deleted):
        print("Parties Resigned:",to_be_deleted)
    return G, new_lst_of_parties

def run_project(total_parties, total_iterations): # to run the whole of the code
    print("Some Definitions:")
    print("Rulling Party: This is  the party with maximum number of followers.")
    print("Top Parties: These are the parties with maximum Quality Factor(Directly proportional to good works of party).")

    num_people = 10000
    num_iter = 100

    G = nx.Graph()
    
    prev_record = {}
    present_record = {}

    parties_added = 0

    lst_for_change = {}

    G, lst_of_parties = create_graph(num_people, 0.8, lst_for_change)
    parties_added+=2

    for p in lst_of_parties:
        present_record[p] = G.degree(p)

    plot_qf = [[] for _ in range(total_parties)]

    plot_deg = [[] for _ in range(total_parties)]

    common_friends={i:{} for i in range(num_people)}
    
    add_frndships(G,lst_of_parties,0.7,0.2,5000,50,common_friends)

    prob_frnd_change = 0.595
    prob_no_change = 0.403
    const_for_change = 80


    G, lst_of_parties = delete_party(G, lst_of_parties, num_people, prev_record, present_record, common_friends)
    G, add_qf, add_deg = iterate(G, lst_of_parties, parties_added, const_for_change, num_iter, num_people, prob_frnd_change, common_friends, lst_for_change, prob_no_change)
    for k in range(2):
        plot_qf[k] += add_qf[k]
        plot_deg[k] += add_deg[k]
    for k in range(2, total_parties):
        plot_qf[k] += [0 for _ in range(num_iter)]
        plot_deg[k] += [0 for _ in range(num_iter)]

    num_random_shift = 500

    for i in range(3, total_iterations+1):
        
        if parties_added < (total_parties) and i%2:
            G, lst_of_parties = add_party(G, lst_of_parties, parties_added, num_people, num_random_shift, common_friends, lst_for_change)
            parties_added+=1
        for p in lst_of_parties:
            present_record[p] = G.degree(p)
        G, lst_of_parties = delete_party(G, lst_of_parties, num_people, prev_record, present_record,common_friends)
        G, add_qf, add_deg = iterate(G, lst_of_parties, parties_added, const_for_change, num_iter, num_people, prob_frnd_change, common_friends, lst_for_change, prob_no_change)
        
        for k in range(parties_added):
            plot_qf[k] += add_qf[k]
            plot_deg[k] += add_deg[k]
        for k in range(min(i, total_parties), total_parties):
            plot_qf[k] += [0 for _ in range(num_iter)]
            plot_deg[k] += [0 for _ in range(num_iter)]
    

    G, lst_of_parties = delete_party(G, lst_of_parties, num_people, prev_record, present_record, common_friends)

    colors = ['green', 'red', 'yellow', 'blue', 'black', 'cyan', 'purple', 'brown', 'pink']

    for i in range(total_parties):
        plt.plot(plot_qf[i], color = colors[i])
        plt.plot(plot_deg[i], color = colors[i], linestyle = '--')
        

    plt.xlabel('Number of Iterations')
    plt.ylabel('Values')

    for i in range(total_parties):
        plt.plot(plot_qf[i], color = colors[i])
        plt.plot(plot_deg[i], color = colors[i], linestyle = '--')
    
    plt.legend(('Q-factor', 'Followers/100'), loc=0)

    plt.show()

    return 0

run_project(9, 30)
