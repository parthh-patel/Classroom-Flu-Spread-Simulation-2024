import pandas as pd

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

def prob_distr (X, pmf):
    
    output_notebook()  # use to display the plot in the jupyter Notebook
    
    source = ColumnDataSource(data = dict(x = X, top = pmf))
    tooltips = [("Value", "@x"), 
                ("Probability", "@top")]
    hover = HoverTool(tooltips = tooltips)

    p = figure(title = "Probability Distribution of Kids Infected on Day 1",
            x_axis_label = "Number of Infected Kids",
            y_axis_label = "Probability",
            tools = [hover])

    p.vbar(x = "x", 
           top = "top", 
           width = 0.8, 
           source = source,
           color = "navy")
    
    p.title.align = "center"
    p.title.text_font_size = "13pt"
    p.axis.axis_label_text_font_size = "15px"
    p.axis.axis_label_text_font_style = "bold"

    show(p)

def pandemic_evolution_plot(report = pd.DataFrame, run_i = 1):

    days = report["Day"].tolist()
    healthy = report["Healthy"].tolist()
    infected = report["Num_Infected"].tolist()
    immune = report["Num_Immune"].tolist()

    tooltips = [
        ("Day", "@days"), 
        ("> Healthy", "@healthy"),
        ("> Infected", "@infected"),
        ("> Immune", "@immune")
        ]

    p = figure(title = f"Pandemic Flu Evolution - Rep {run_i}", 
            x_axis_label = "Day #", 
            y_axis_label = "Population", 
            tooltips = tooltips,
            tools = [""])

    p.vbar_stack(["healthy", "infected", "immune"], 
                x = "days", 
                width = 0.5, 
                color = ["dodgerblue", "indianred", "forestgreen"], 
                source = {"days": days, "healthy": healthy, "infected": infected, "immune": immune}, 
                legend_label = ["Healthy", "Infected", "Immune"])
    
    p.title.align = "center"
    p.legend.location = "top_right"  
    p.legend.click_policy = "hide"  
    
    p.title.text_font_size = "13pt"
    p.axis.axis_label_text_font_size = "15px"
    p.axis.axis_label_text_font_style = "bold"

    output_notebook()

    show(p)

def expected_num_infected_per_day (df = pd.DataFrame):
    average_infected = df.groupby("Day")["Num_Infected"].mean()

    source = ColumnDataSource(data = dict(
        x = average_infected.index,
        y = average_infected.values))

    tooltips = [("Day", "@x"), 
                ("Avg Infected", "@y")]
    hover1 = HoverTool(tooltips = tooltips)

    # histogram for average number of infected kids by day
    p = figure(title = "Estimated Expected Number of Infected Kids by Day", 
               x_axis_label = "Day", 
               y_axis_label = "Expected Number of Infected Kids", 
               tools = [hover1])
    
    p.title.align = "center"
    p.title.text_font_size = "13pt"
    p.axis.axis_label_text_font_size = "15px"
    p.axis.axis_label_text_font_style = "bold"

    p.vbar(x = "x", 
           top = "y", 
           width = 0.5, 
           source = source, 
           color = "crimson")

    show(p)


import matplotlib.pyplot as plt

def pandemic_lengths_histogram(pandemic_data, half_immune = False):
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))

    pandemic_lengths = []
    pandemic_lengths_excluding_day_3 = []

    for run_id, dataframe in pandemic_data.items():
        
        # -1 because the last day is just checking if there are any more infected left and no new infections occur
        pandemic_length = dataframe["Day"].max() - 1 
        pandemic_lengths.append(pandemic_length)

        if pandemic_length != 3:
            pandemic_lengths_excluding_day_3.append(pandemic_length)

    bins = range(min(pandemic_lengths), max(pandemic_lengths) + 2)
    bins_excluding_day_3 = range(min(pandemic_lengths_excluding_day_3), max(pandemic_lengths_excluding_day_3) + 2)

    axs[0].hist(pandemic_lengths,
                bins = bins,
                align = "left",
                rwidth = 0.5,
                color = "royalblue")
    axs[0].set_xlabel("Pandemic Length")
    axs[0].set_ylabel("Frequency")
    axs[0].set_title("Histogram of Pandemic Lengths")

    axs[1].hist(pandemic_lengths_excluding_day_3,
                bins = bins_excluding_day_3,
                align = "left",
                rwidth = 0.5,
                color = "royalblue")
    axs[1].set_xlabel("Pandemic Length")
    axs[1].set_ylabel("Frequency")
    axs[1].set_title("Histogram of Pandemic Lengths Excluding Day 3")

    for ax in axs:
        ax.set_xticks(range(min(pandemic_lengths), max(pandemic_lengths) + 2, 2))
        ax.grid(axis = "y", alpha = 0.75)
        ax.set_axisbelow(True)


    # use this to fit distributions using Arena. 
    # if more time, look into fitting using SciPy or NumPy. 
    if half_immune:
        with open("half_immune_pan_lens.dst", "w") as file:
            for length in pandemic_lengths:
                file.write(str(length) + "\n")

        with open("half_immune_pan_len_excld_day3.dst", "w") as file:
            for length in pandemic_lengths_excluding_day_3:
                file.write(str(length) + "\n")
    else:
        with open("pan_len.dst", "w") as file:
            for length in pandemic_lengths:
                file.write(str(length) + "\n")
            
        with open("pan_len_excld_day3.dst", "w") as file:
            for length in pandemic_lengths_excluding_day_3:
                file.write(str(length) + "\n")


    plt.tight_layout()
    plt.show()


def num_immune_histogram(num_immune_day1):
    bins = range(min(num_immune_day1), max(num_immune_day1) + 2)

    plt.hist(num_immune_day1, 
             bins = bins, 
             align = "left", 
             rwidth = 0.5,
             color = "green")

    plt.xlabel("Number of Immune Kids")
    plt.ylabel("Frequency")
    plt.title("Histogram of Number of Immune Kids on Day 1")

    plt.xticks(range(min(num_immune_day1), max(num_immune_day1) + 2))
    plt.gca().set_axisbelow(True)
    plt.grid(axis = "y", alpha = 0.75)

    plt.show()


