import PySimpleGUI as sg, pandas as pd, matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import scraping, ordering_datasets, feature_selec_rnd_forest
import feature_selec_rfe
import cleaning_D1
import cleaning_D2
import feature_selec_rfe
import map
import seaborn as sns
import impact_energy_knn, radiated_energy_xgb
import generate_20_rows, askGPT, sys
import pyttsx3

sg.theme('Dark')

def update_window(window, data):
    data_with_row_numbers = [[i+1] + row for i, row in enumerate(data)]
    window['-TABLE-'].update(values=data_with_row_numbers)

def func(country_name):
    layout0 = [[sg.Text(f'Meteor Impact Analysis for {country_name}.\n', font=('Cooper Black', 30), justification='center', expand_x=True)]]

    layout1 = [
        [
            sg.Table(
                values=[],
                headings=['Row', 'Radius', 'Volume', 'Density', 'Mass', 'Radiated Energy', 'Impact Energy'],
                display_row_numbers=False,
                auto_size_columns=False,  # Set auto_size_columns to False
                justification='center',
                num_rows=10,  # Change the number of rows displayed
                key='-TABLE-',
                size=(10, 14),  # Adjust the size of the table
                col_widths=[4, 6, 6, 6, 6, 13, 12],  # Adjust the column widths
                font=('Helvetica', 13)  # Adjust the font size for the table data
            )
        ], [sg.Button('Generate Data', size=(20,1), font=('Helvetica', 15) )]
    ]

    layout2 = [
        [sg.Frame('', [[sg.Multiline('', key='-DYNAMIC_TEXT-', size=(63, 16), font=('Helvetica', 13))]], font=('Helvetica', 13), pad=(10, 10))],
         [sg.Button('Write Report', size=(20, 1), font=('Helvetica', 15)), sg.Button('Read Report', size=(20, 1), font=('Helvetica', 15))]]

    left_part = layout1 + layout2

    layout3 = [
    [
        sg.Column(
            [
                [sg.Text('Plot 1', font=('Helvetica', 14))],
                [sg.Image(filename='C:/Users/hp/Desktop/uni/sem4/ds_proj/pics/plot1.1.png', size=(550, 260), key='-IMAGE-')],])]]

    layout4 = [
    [
        sg.Column(
            [
                [sg.Text('Plot 2', font=('Helvetica', 14), justification='center')],
                [sg.Image(filename='C:/Users/hp/Desktop/uni/sem4/ds_proj/pics/plot2.1.png', size=(550, 260), key='-IMAGE-')],
                [sg.Button('Explore Plots.', size=(20, 1),font=('Helvetica', 15))]
            ]
        )
    ]
    ]

    right_part = layout3 + layout4

    layout = [
        [sg.Column(layout0, justification='center')],
        [sg.Column(left_part, size=(650, 1000)), sg.VSeparator(), sg.Column(right_part, size=(600, 1200))]
    ]
    window = sg.Window('Analysis', layout, size=(1300,800), location=(350,100))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel.":
            break
        elif event == 'Generate Data':
            data = generate_20_rows.generate()
            data_values = data.values.tolist()  # Convert DataFrame to a list of lists
            update_window(window, data_values)
        elif event == 'Write Report':
            text = "Write a long statistical report(atleast 500 words) on a scenario where a large meteor falls on " + country_name + """. 
            Generate realistic numbers(do not use dummy data, generate real numbers) to make this report seem more realistic, 
            talk about what kind of affects this would have on
            the country mentioned, according to its population density, infrastructure, geography, and emergency response. Mention
            damage, costs incurred, people injured, deaths, and more, as well as providing percentages and statistics to
            better explain the situation."""
            generated_text = askGPT.prompt(text)  # Call a function from another file to get dynamic text
            window['-DYNAMIC_TEXT-'].update(generated_text)
        elif event == 'Read Report':
            engine = pyttsx3.init()
            engine.setProperty('voice', 'english+f3')
            engine.setProperty('rate', 180)
            engine.say(generated_text)
            engine.runAndWait()
        elif event == 'Explore Plots.':
            window.close()
            def plot1():    # Line Graph: Radiated Energy vs features
                df = generate_20_rows.generate()
                
                radiated_energy = df["Radiated Energy"]
                feature_columns = df.columns.drop("Radiated Energy")

                for feature in feature_columns:
                    plt.plot(df[feature], radiated_energy, marker='o', linestyle='-', label=feature)

                plt.xlabel('Feature Value')
                plt.ylabel('Radiated Energy')
                plt.title('Radiated Energy vs Features')

                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()

            def plot5():    # Impact vs Radiated
                df = generate_20_rows.generate()

                impact_energy = df["Impact Energy"]
                radiated_energy = df["Radiated Energy"]

                # Create the bar chart
                plt.bar(df.index, impact_energy, label="Impact Energy")
                plt.bar(df.index, radiated_energy, label="Radiated Energy")

                # Set the labels and title
                plt.xlabel("Index")
                plt.ylabel("Energy")
                plt.title("Impact Energy vs Radiated Energy")

                # Add a legend
                plt.legend()

                # Show the plot
                plt.show()


            def plot4():    # Line Graph: Impact Energy vs features
                df = generate_20_rows.generate()
                
                impact = df["Impact Energy"]
                feature_columns = df.columns.drop("Impact Energy")

                for feature in feature_columns:
                    plt.plot(df[feature], impact, marker='o', linestyle='-', label=feature)

                plt.xlabel('Feature Value')
                plt.ylabel('Impact Energy')
                plt.title('Impact Energy vs Features')

                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()


            def plot3():    # Pair Plot
                df = generate_20_rows.generate()
                
                sns.pairplot(df)
                plt.show()


            def plot2():    # Heatmap
                df = generate_20_rows.generate()
                
                corr_matrix = df.corr()

                plt.figure(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
                plt.title("Correlation Heatmap")
                plt.show()

            layout = [
                [sg.Button('Line: Radiated Energy vs features', key='button1', size=(30, 2))],
                [sg.Button('Heatmap: All Features', key='button2', size=(30, 2))],
                [sg.Button('Bar: Impact vs Radiated Energy', key='button5', size=(30, 2))],
                [sg.Button('Line: Impact Energy vs features', key='button4', size=(30, 2))],
                [sg.Button('Pair Plot: All Features', key='button3', size=(30, 2))],
            ]

            window = sg.Window('Plotting', layout, size=(270,250), location=(850,350))

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == "Cancel.":
                    break
                elif event == 'button1':
                    plot1()
                elif event == 'button2':
                    plot2()
                elif event == 'button3':
                    plot3()
                elif event == 'button4':
                    plot4()
                elif event == 'button5':
                    plot5()

            window.close()

    window.close()

def featureSel():
    rfe_result = feature_selec_rfe.rfe()
    forest_result = feature_selec_rnd_forest.forest()
    message = ""
    message += f"{'Feature':<15}{'RFE':<15}{'Random Forest':<15}\n\n"
    for key in rfe_result.keys() | forest_result.keys():
        rfe_val = rfe_result.get(key, 0.000)
        forest_val = forest_result.get(key, 0.000)
        message += f"{key:<15}{rfe_val:<15.3f}{forest_val:<15.3f}\n"
    sg.PopupScrolled(message, title="Comparison")

layout0 = [
    [
        sg.Text(
            "Welcome to the Impact Analysis Program\n"
        ),
    ],
    [sg.Button("Continue.")]
]

layout1 = [
    [
        sg.Text(
            """Perform preprocessing 
OR jump straight to the impact predictor?"""
        ),
    ],
    [sg.Button("Let's Pre-process!"), sg.Button("Impact Predictor.")]
]

layout2 = [
    [
        sg.Text(
            "We need to scrape some data and make a csv.\n"
        )
    ],
    [sg.Button("Scrape!"), sg.Button("Cancel.")],
]

layout3 = [
    [sg.Text("Time to do some data cleaning! ")],
    [sg.Button("Clean Dataset 1."), sg.Button("Cancel.")],
]

layout4 = [
    [sg.Text("And now clean dataset2... ")],
    [sg.Button("Clean Dataset 2."), sg.Button("Cancel.")],
]

layout5 = [
    [
        sg.Text(
            "The data is clean now, but data ordering is required."
        )
    ],
    [sg.Button("Order Data.")],
    [sg.Button("Cancel.")],
]

layout6 = [
    [
        sg.Text(
            "Now let's use Random Forest Model for feature selection.")],
    [sg.Button("Apply Random Forest."), sg.Button("Random Forest?", font=('Helvetica', 8), button_color=('white', 'black'))],
    [sg.Button("Cancel.")]
]
layout7 = [
    [
        sg.Text(
            "Now let's use Random Forest Model for feature selection.")],
    [sg.Button("Apply Random Forest."), sg.Button("Random Forest?", font=('Helvetica', 8), button_color=('white', 'black'))],
    [sg.Button("Cancel.")]
]
layout8 = [
    [sg.Text("Cross-check it using Reccursive Feature Elimination. ")],
    [sg.Button("Apply RFE.")],
    [sg.Button("Skip.")],
]
layout9 = [
    [sg.Text("Predict Impact Energy using KNN model. ")],
    [sg.Button("Apply KNN.")],
    [sg.Button("Cancel.")],
]

layout10 = [
    [sg.Text("Predict Radiated Energy using Extreme Gradient Boosting model. ")],
    [sg.Button("Apply XGB.")],
    [sg.Button("Cancel.")],
]

layout11 = [
    [sg.Text("Pick a location for impact analysis.", font=('Helvetica', 11))],
    [sg.Button("Lets Go!", font=('Helvetica', 11))],
    [sg.Button("Cancel.", font=('Helvetica', 11))],
]

window0= sg.Window("Welcome!", layout0, size=(450, 100), text_justification='center', element_justification='center', location=(400,300))
window1 = sg.Window("Proceed", layout1, size=(450, 100), text_justification='center', element_justification='center', location=(400,300))
window2 = sg.Window("Scraping", layout2, size=(450, 100), text_justification='center', element_justification='center', location=(400,300))
window3 = sg.Window("Cleaning Dataset1", layout3, size=(450, 100), element_justification='center', location=(400,300))
window4 = sg.Window("Cleaning Dataset2", layout4, size=(450, 100), element_justification='center', location=(400,300))
window5 = sg.Window("Ordering", layout5, size=(450, 100), element_justification='center', location=(400,300))
window6 = sg.Window("Random Forest", layout6, size=(450, 150), element_justification='center', location=(400,300))
window7 = sg.Window("Random Forest", layout7, size=(450, 150), element_justification='center', location=(400,300))
window8 = sg.Window("Comparison", layout8, size=(450, 100), element_justification='center', location=(400,300))
window9 = sg.Window("Impact Energy", layout9, size=(450, 100), element_justification='center', location=(400,300))
window10 = sg.Window("Radiated Energy", layout10, size=(450, 100), element_justification='center', location=(400,300))
window11 = sg.Window("Location", layout11, size=(450, 100), element_justification='center', location=(400,300))

layoutErr = [
                [sg.Text('Pick a valid location!', font=('Helvetica', 15))],
                [sg.Button('OK', font=('Helvetica', 15))]]
windowErr = sg.Window('Invalid Location', layoutErr, location=(500, 300), size=(400,300))

def skip():
    event, values = window11.read()
    if event == sg.WIN_CLOSED or event == "Cancel.":
        window11.close()
    if event == "Lets Go!":
            map.maps()
            name = map.country_name
            sg.PopupScrolled(name, title='Selected Location', font=('Helvetica', 15))
            name = str(name)
            if name == 'None':
                window11.close()
                while True:
                    event, values = windowErr.read()
                    if event == sg.WINDOW_CLOSED or event == 'OK':
                        break
                sys.exit()
            else: 
                func(name)
                sys.exit()

def mainFunc():
    # loop through all the windows and open each one after the previous one is closed
    country_name = ''
    for window in (window0, window1, window2, window3, window4, window5, window6, window8, window9, window10, window11):
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel.":
            for w in (window0, window1, window2, window3, window4, window5, window6, window8, window9, window10, window11, window):
                w.close()
            break
        if event == "Random Forest?":
            rf_text = askGPT.prompt("Briefly explain what random forest model is.")
            sg.popup_scrolled(rf_text, title='Info')
            event, values = window7.read()
            if event == sg.WIN_CLOSED or event == "Cancel.":
                window7.close()
        
        # if event == "RFE?":
        #     rf_text = askGPT.prompt("Briefly explain what recursive feature elimination.")
        #     sg.popup_scrolled(rf_text)
        #     event, values = window7.read()
        #     if event == sg.WIN_CLOSED or event == "Cancel.":
        #         window7.close()

        if event == "Impact Predictor.":
            skip()

        if event == "Scrape!":
            scraping.scrape()

        if event == "Clean Dataset 1.":
            cleaning_D1.clean1()

        if event == "Clean Dataset 2.":
            cleaning_D2.clean2()

        if event == "Order Data.":
            ordering_datasets.order()
        
        if event == "Apply Random Forest.":
            d = feature_selec_rnd_forest.forest()
            message = ""
            for key, value in d.items():
                message += f"{key}: {value:.3f}\n"
            sg.PopupScrolled(message,title= 'Random Forest')
            
        if event == "Apply RFE.":
            featureSel()
            
        if event == "Apply KNN.":
            impact_energy_list = impact_energy_knn.predict_impact_energy()
            message = ""
            message += f"{'Impact Energy':<15}\n"
            for i, value in enumerate(impact_energy_list, start=1):
                message += f"{i}.  {value:.3f}\n"
            sg.PopupScrolled(message, title='Impact Energy')
            
        if event == "Apply XGB.":
            radiated_energy_list = radiated_energy_xgb.predict_radiated_energy()
            message = ""
            message += f"{'Radiated Energy':<15}\n"
            for i, value in enumerate(radiated_energy_list, start=1):
                message += f"{i}.  {value:.3f}\n"
            sg.PopupScrolled(message, title='Radiated Energy')

        if event == "Lets Go!":
            map.maps()
            country_name = map.country_name
            sg.PopupScrolled(country_name, title='Selected Location', font=('Helvetica', 15))
        window.close()
    return country_name


# MAIN

name = mainFunc()
if name == 'None':
    window11.close()
    sys.exit()
else: 
    func(name)

