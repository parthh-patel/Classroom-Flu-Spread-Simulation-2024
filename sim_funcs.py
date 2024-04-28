import pandas as pd
import numpy as np
import random
import time

import plot_helper as plot


def run_sim (n_kids = 31, p_infection = 0.02, recovery_days = 3, reps = 1000, seed = None, print_debug = False, plot_each_day = False):

    print("Pandemic Flu Spread Simulation | Only 1 Infected Kid on Day 1")
    print("- Number of students:", n_kids)
    print("- Probability of infection:", p_infection*100, "%")
    print("- Recovery days before immunity:", recovery_days, "\n")

    if reps is None:
        print("-> Running simulation with default reps:", reps, "\n")
    elif reps <= 5:
        plot_each_day = True
        print("-> Running simulation with supplied reps:", reps)
        print("-> Plotting pandemic flu evolution graph for each rep since reps <= 5\n")
    else:
        print("-> Running simulation with supplied reps:", reps, "\n")


    #   DOESNT WORK, CAUSES ISSUES WITH RANDOM NUM FUNCTION AND GIVES SAME VALUES FOR EVERY DAY. DONT NEED IT ANYWAYS
    # if seed is None:
    #     seed = int(random.random() * time.time())
    #     print("-> Using generated random seed:", seed)
    # else:
    #     print("-> Using supplied seed:", seed)
        
    combined_df = pd.DataFrame()
    results = {}  
 
    #loading library to reduce print statements to console
    from tqdm import tqdm
    
    for run_i in tqdm(range(1, reps + 1), desc = "Running simulation", unit = "rep"):

        # start the df with all kids initially not infected
        df_int = pd.DataFrame({"Kid": range(0, n_kids + 1), 
                               "Infected": False, 
                               "Immune": False, 
                               "Infected_Duration": 0})

        # set Tommy, kid 0, to be patient zero :(
        df_int.loc[df_int["Kid"] == 0, "Infected"] = True

        result_df = run_rep(n_kids, p_infection, recovery_days,
                            df_int, seed, print_debug, plot_each_day, run_i)

        # print("\n--> Running rep", "-=-" * 7, run_i,"-=-" * 7, "Days Lasted:", result_df.iloc[-1]["Day"])

        results[run_i] = result_df

    return results


def run_rep (n_kids = 31, p_infection = 0.02, recovery_days = 3, df_int = pd.DataFrame, seed = None, print_debug = False, plot_each_day = False, run_i = 1):
    
    #initialize rep 
    day_count = 1
    df = df_int.copy()
    rep_report = pd.DataFrame({"Day": [0], 
                               "Healthy": [0],
                               "Num_Infected": [0], 
                               "Num_Immune": [0]})

    #run the loop while at least 1 kid is infected
    while df["Infected"].any():
        if (print_debug):
            print("_"*20)
            print("\nDAY:", day_count)

        #updates df for everyday the pandemic is still ongoing
        df = run_day_in_rep(n_kids, p_infection, recovery_days,
                            df, seed = seed, print_debug = print_debug)

        num_infected = len(df[df["Infected"]])
        num_immune = len(df[df["Immune"]])

        day_update = {"Day": day_count, 
                      "Healthy": (len(df["Kid"])-1) - num_infected - num_immune, 
                      "Num_Infected": num_infected, 
                      "Num_Immune": num_immune}
        
        #update the report w/ days results
        rep_report = pd.concat([rep_report, pd.DataFrame(day_update, index=[0])], ignore_index=True)    
        day_count += 1
    
    #if reps are small, everydays results can be plotted.
    if (plot_each_day):
        plot.pandemic_evolution_plot(rep_report, run_i)
        
    return rep_report


def run_day_in_rep(n_kids = 31, p_infection = 0.02, recovery_days = 3, df = pd.DataFrame, seed = None, print_debug = False):

    #   DOESNT WORK, CAUSES ISSUES WITH RANDOM NUM FUNCTION AND GIVES SAME VALUES FOR EVERY DAY. DONT NEED IT ANYWAYS
    # #set seed if provided:
    # if (seed):
    #     np.random.seed(seed)
    # else:
    #     seed = int(random.random() * time.time())
    #     np.random.seed(seed)


    # RANDOM SEED FOR EVERY DAY 
    seed = int(random.random() * time.time())
    np.random.seed(seed)

    if (print_debug):
        print("Random seed for the day:", seed)

    #indices of currently infected kids
    infected_indices = df.loc[df["Infected"] == True].index
    recovered_indices = []

    for ind in infected_indices:
        df.at[ind, "Infected_Duration"] += 1
        
        #if the kid has been infected for 3 days, mark them as immune and not infected
        if df.at[ind, "Infected_Duration"] > recovery_days:

            df.at[ind, "Immune"] = True
            df.at[ind, "Infected"] = False
            recovered_indices.append(ind)


    #updates the indices of currently infected kidsing
    updated_infected_indices = df.loc[df["Infected"]].index

    if (print_debug):
        print("Infected IDs at start of day:", updated_infected_indices.values)
        print("Num of infected:", len(updated_infected_indices))


    # simulate infection spread for each infected kid; every kid interacts with a healthy kid
    for inf_kid in updated_infected_indices:
        
        # kids who can be infected bc they are not infected yet and not immune
        potential_infections = df.loc[(~df["Infected"]) & (~df["Immune"])]
        
        if (print_debug):
            print("Potential Infections for kid", inf_kid, ":", len(potential_infections))

        for kid_id, _ in potential_infections.iterrows():
            infection_result = np.random.choice([False, True], p = [1 - p_infection, p_infection])
        
            if (print_debug):
                print("---> Infected kid:", inf_kid, "w/ Healthy kid:", kid_id, "Result:", "*** Successful Infection ***" if infection_result else "No Infection")
                    
            # updates the df for new infections
            df.loc[df["Kid"] == kid_id, "Infected"] = infection_result
   
    if (print_debug):
        print("Recovered IDs:", recovered_indices)
        print("Num of Recovered:", len(recovered_indices))

    return df


def run_sim_half_immune(n_kids = 31, p_infection = 0.02, recovery_days = 3, reps = 1000, seed = None, print_debug = False, plot_each_day = False):

    print("Pandemic Flu Spread Simulation | 50-50 chance of already being immune")
    print("- Number of students:", n_kids)
    print("- Probability of infection:", p_infection*100, "%")
    print("- Recovery days before immunity:", recovery_days, "\n")

    if reps is None:
        print("-> Running simulation with default reps:", reps, "\n")
    elif reps <= 5:
        plot_each_day = True
        print("-> Running simulation with supplied reps:", reps)
        print("-> Plotting pandemic flu evolution graph for each rep since reps <= 5\n")
    else:
        print("-> Running simulation with supplied reps:", reps, "\n")
   
    combined_df = pd.DataFrame()
    results = {}  

    
    #loading library to reduce print statements to console
    from tqdm import tqdm
    
    for run_i in tqdm(range(1, reps + 1), desc = "Running simulation", unit = "rep"):

        # start the df with all kids initially not infected
        df_int = pd.DataFrame({"Kid": range(0, n_kids + 1), "Infected": False, "Immune": False, "Infected_Duration": 0})

        # set Tommy, kid 0, to be patient zero :(
        df_int.loc[df_int["Kid"] == 0, "Infected"] = True

        ### MAIN CHANGE ###

        #all kids except kid 0, who is infected and shouldn't be immune
        for index, row in df_int.iloc[1:].iterrows():            
            if random.random() < 0.5:  # 50% chance of being immune. can change to test diff values
                df_int.at[index, "Immune"] = True
        
        if (print_debug):
            print("- Number of students already immune:", len(df_int[df_int["Immune"] == True]), "\n")

        result_df = run_rep(n_kids, p_infection, recovery_days,
                            df_int, seed, print_debug, plot_each_day, run_i)

        if (print_debug):
            print("\n--> Finsihed rep", "-=-" * 8, run_i,"-=-" * 8, "Days Lasted:", result_df.iloc[-1]["Day"] - 1)

        results[run_i] = result_df

    return results

