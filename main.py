import pandas as pd
from aircraft import Aircraft
import params
import plotly.express as px
import plotly
import pandas as pd
import plotly.io as pio
import warnings
warnings.filterwarnings("ignore")
#fleet choice
List_of_AD = params.AD
Subset_AD = params.AD[0:4]

def create_aircrafts(fleet):
    List_of_AD = fleet #List 
    decisions = {k: Aircraft(k) for k in List_of_AD}

    model_results = pd.DataFrame()

    for key in decisions: 
        jet_fuel = decisions[key].calc_jet_fuel()
        LH2_fuel = decisions[key].calc_LH2_fuel()
        CO2_emission_redution = decisions[key].calc_co2_reduction()
        CO2_utility = decisions[key].utility_co2()
        rel = decisions[key].calc_reliability()
        payload = decisions[key].calc_payload()
        PAX = decisions[key].calc_PAX()
        pax_utility = decisions[key].calc_pax_utility()
        range = decisions[key].calc_range()
        range_utility = decisions[key].calc_range_utility()
        total_utility = 0.25 * (CO2_utility + pax_utility + range_utility + rel )
        avg_trl = decisions[key].calc_AVG_TRL()
        
        result = {'Name':key,
            'Jet Fuel Usage [kg]':jet_fuel,
            'LH2 Fuel Usage [kg]': LH2_fuel,
            'CO2 Reduction [%]': CO2_emission_redution,
            'Payload [kg]' : payload,
            'PAX' : PAX,
            'Range [km]' : range,
            'CO2 Utility': CO2_utility,
            'Reliability Utility': rel,
            'PAX Utility': pax_utility,
            'Range Utility': range_utility,
            'Total Utility': total_utility,
            'AVG TRL': avg_trl                       
            }

        model_results = model_results.append(result, ignore_index = True) 

    return model_results

def create_HyFIVE(aircraft_name):
    #aircraft_name = "F2C2H1L3"
    aircraft = Aircraft(aircraft_name)
    return aircraft

def plot_tradespace(tradespace_parameters):
    new_df = tradespace_parameters
    new_df['Location'] = new_df.Name.str[7:9]
    new_df['Config'] = new_df.Name.str[2:4]
    fig = px.scatter(new_df, x="AVG TRL", y="Total Utility", color = "Location", hover_name = new_df.Name, template = 'seaborn')
    fig.update_traces(marker=dict(size=12,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.update_traces(textposition='bottom center')
    fig.show()
    #fig.write_html("Utility_vs_AVGTRL_by_L.html")
    return fig

def main(fleet):
    model_results = create_aircrafts(fleet)
    d328 = create_HyFIVE("F1C1H1L3")
    print(d328.name)
    return model_results



if __name__=="__main__":
    # fleet choice
    # List_of_AD = params.AD
    # Subset_AD = params.AD[0:4]
    # Custom_AD = []
    tradespace_parameters = main(List_of_AD)
    print(tradespace_parameters)
    plot_tradespace(tradespace_parameters)

