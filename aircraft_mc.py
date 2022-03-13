#%%
from distribution import Variable
from aircraft import Aircraft
from main import create_aircrafts
import params
import numpy as np
from random import random,uniform,triangular,betavariate,expovariate,seed
from random import gammavariate,gauss,lognormvariate,normalvariate,vonmisesvariate
from random import paretovariate, weibullvariate
import matplotlib.pyplot as plt
import pandas as pd
from main import create_aircrafts, plot_tradespace

# 1. Drag
# 2. Hydrogen SFC
# 3. Mission Profile (Take off & Landing) %
# 4. Fuel Cell mass
# 5. Reliability

lift_to_drag_det = params.LIFT_TO_DRAG
SFC_hybrid_det = params.SFC_HYBRID
mission_profile_det = params.LANDING_RATIO
fc_mass_det = params.FCS_MASS
print("FCS Mass Det: ", fc_mass_det)

fleet = ['F2C4H2L1', 'F1C3H1L2', 'F2C2H1L1', 'F2C3H2L3', 'F1C3H1L3', 'F1C1H2L3', 'F1C1H2L2', 'F3C5H3L3']#List 
det = create_aircrafts(fleet)
print(det)

#det_mod_total_utility = aircraft_mc.calc_total_utility()

#%%
def fc_mass_pdf(dist, *args):
    fc_mass_mc = Variable(dist, *args)
    fc_mass_distribution = []
    for i in range(10000):
        fc_mass_distribution.append(fc_mass_mc())
    plt.hist(fc_mass_distribution,bins=100)
    plt.xlabel('Fuel Cell Mass MC')
    plt.ylabel('PDF')
    plt.show()
    return fc_mass_mc #return a list of RVs

def lift_to_drag_pdf(dist, *args):
    lift_to_drag_mc = Variable(dist, *args)
    lift_to_drag_distribution = []
    for i in range(10000):
        lift_to_drag_distribution.append(lift_to_drag_mc())
    plt.hist(lift_to_drag_distribution,bins=100)
    plt.xlabel('Lift to Drag (L/D) MC')
    plt.ylabel('PDF')
    plt.show()
    return lift_to_drag_mc #return a list of RVs

def SFC_hybrid_pdf(dist, *args):
    SFC_hybrid_mc = Variable(dist, *args)
    SFC_hybrid_distribution = []
    for i in range(10000):
        SFC_hybrid_distribution.append(SFC_hybrid_mc())
    plt.hist(SFC_hybrid_distribution,bins=100)
    plt.xlabel('SFC_hybrid_mc MC')
    plt.ylabel('PDF')
    plt.show()
    return SFC_hybrid_mc #return a list of RVs

def mission_profile_pdf(dist, *args):
    mission_profile_mc = Variable(dist, *args)
    mission_profile_distribution = []
    for i in range(10000):
        mission_profile_distribution.append(mission_profile_mc())
    plt.hist(mission_profile_distribution,bins=100)
    plt.xlabel('Mission Profile MC')
    plt.ylabel('PDF')
    plt.show()
    return mission_profile_mc #return a list of RVs

def trl_pdf(dist, *args):
    trl_mc = Variable(dist, *args)
    trl_distribution = []
    for i in range(10000):
        trl_distribution.append(trl_mc())
    plt.hist(trl_distribution,bins=100)
    plt.xlabel('TRL MC')
    plt.ylabel('PDF')
    plt.show()
    return trl_mc
#%%
def battery_pdf(dist, *args):
    battery_mc = Variable(dist, *args)
    battery_distribution = []
    for i in range(10000):
        battery_distribution.append(battery_mc())
    plt.hist(battery_distribution,bins=100)
    plt.xlabel('Battery MC')
    plt.ylabel('PDF')
    plt.show()
    return battery_mc

def hex_pdf(dist, *args):
    hex_mc = Variable(dist, *args)
    hex_distribution = []
    for i in range(10000):
        hex_distribution.append(hex_mc())
    plt.hist(hex_distribution,bins=100)
    plt.xlabel('Heat Exchanger MC')
    plt.ylabel('PDF')
    plt.show()
    return hex_mc

#%%
#RUN SIMULATIONS
#SET DISTRIBUTION and PARAMETERS
#DECIDE SIMULATION ITERATIONS
seed(1)

#L4 -> L/D = 14
decisions = {k: Aircraft(k) for k in fleet}
aircraft_mc = Aircraft('F1C1H1L2')
aircraft_mc_utility_results =[]
aircraft_mc_trl_results = []
model_results = pd.DataFrame()

hex_mc_h1 = hex_pdf(normalvariate, 600, 10)
hex_mc_h2 = hex_pdf(normalvariate, 300, 50) #bigger uncertainties 
battery_mass_mc = battery_pdf(triangular, 500, 800, 750)
fc_mass_mc = fc_mass_pdf(triangular, 1100, 1400, 1300) #optimisitc fc mass decrease over time
mission_profile_mc = mission_profile_pdf(gauss, 0.34,.07)
# lift_to_drag_mc_L1 = lift_to_drag_pdf(triangular, 0,22,14)
# lift_to_drag_mc_L2 = lift_to_drag_pdf(triangular, 0,18,14)
lift_to_drag_mc_L1 = lift_to_drag_pdf(triangular, 7,14,12) #Fuselage: more drag, lower L/D 
lift_to_drag_mc_L2 = lift_to_drag_pdf(triangular, 9,14,13) #Wing: less drag, higher L/D
#lift_to_drag_mc_L3 = lift_to_drag_pdf(triangular, 13.5,14.5,14)
lift_to_drag_mc_L3 = lift_to_drag_pdf(gauss, 14,0.2) #more determinisitc - existing design
SFC_hybrid_mc = SFC_hybrid_pdf(triangular, 11, 16, 14.75) #futurisitc
f_trl_mc = trl_pdf(triangular, 5,8,6)
h_trl_mc = trl_pdf(triangular, 7,8,7.5)
c_trl_mc_hybrid = trl_pdf(triangular, 5,9,6)
c_trl_mc_electric = trl_pdf(triangular, 3,8,6)
l1_trl_mc = trl_pdf(triangular, 2, 5, 4)
l2_trl_mc = trl_pdf(triangular, 2, 6, 4 )
#l3_trl_mc = trl_pdf(triangular, 7.5, 8, 7)

#TODO: For L3, do not use uncertainties for Lift to Drag

for key in decisions:


    for i in range(2000):
        params.H1_MASS = hex_mc_h1()
        params.H2_MASS = hex_mc_h2()
        params.FCS_MASS = fc_mass_mc()      
        params.BATTERY_MASS = battery_mass_mc()  
        params.LANDING_RATIO = mission_profile_mc()
        if decisions[key].location == "L1": #L1 and L2
            params.LIFT_TO_DRAG = lift_to_drag_mc_L1()
        elif decisions[key].location == "L2":
            params.LIFT_TO_DRAG = lift_to_drag_mc_L2()
        else: #L3
            params.LIFT_TO_DRAG = lift_to_drag_mc_L3()
        params.SFC_HYBRID = SFC_hybrid_mc()
        params.trl["F1"] = f_trl_mc()
        params.trl["F2"] = f_trl_mc()
        params.trl["C1"] = c_trl_mc_hybrid()
        params.trl["C2"] = c_trl_mc_hybrid()
        params.trl["C3"] = c_trl_mc_electric()
        params.trl["C4"] = c_trl_mc_electric()
        params.trl["H1"] = h_trl_mc()
        params.trl["H2"] = h_trl_mc()
        params.trl["L1"] = l1_trl_mc()
        params.trl["L2"] = l2_trl_mc()

        #Run Simulations 
        #aircraft_mc_utility_results.append(aircraft_mc.calc_total_utility())
        #aircraft_mc_trl_results.append(aircraft_mc.calc_AVG_TRL())
        
        #aircraft_mc_utility_results.append(decisions[key].calc_total_utility())
        #aircraft_mc_trl_results.append(decisions[key].calc_AVG_TRL())

        result = {'Name':key,
            'Total Utility': decisions[key].calc_total_utility(),
            'AVG TRL': decisions[key].calc_AVG_TRL()                   
            }

        model_results = model_results.append(result, ignore_index = True) 

#aircraft_mc_results

# %%
#Plot Uncertainties on the tradespace
import plotly.express as px
import plotly.graph_objects as go
# result = {'Name':'F1C1H1L2',
#             'Total Utility': aircraft_mc_utility_results,
#             'AVG TRL': aircraft_mc_trl_results                     
#             }
#mc_results = pd.DataFrame(result)
#print(mc_results.head())

#model_results is 10000 by 3 dataframe

#fig = plot_tradespace(model_results, "Name")
new_df = model_results
new_df['Location'] = new_df.Name.str[7:9]
new_df['Config'] = new_df.Name.str[2:4]
#Set the X axis and Y axis range manually without breaking the marginal plots using range_x and range_y
fig = px.scatter(new_df, x="AVG TRL", y="Total Utility", color = "Name", 
                hover_name = new_df.Name, template = 'seaborn',
                marginal_y='histogram', marginal_x='box',  range_x=[3.5, 10.5], range_y = [0.4, 0.9])

fig.update_traces(marker=dict(size=5, opacity = 0.3,
                                line=dict(width=0.5,
                                        color='DarkSlateGrey')),
                    selector=dict(mode='markers'))

#fig.update_xaxes(range=[4, 10.5])
#fig.update_yaxes(range=[0.4, 0.9])
# Add scatter trace with deterministic model results
fig.add_trace(
    go.Scatter(
        mode='markers',
        marker_symbol='diamond',
        x=det['AVG TRL'],
        y=det['Total Utility'],
        marker=dict(
            color=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink'],
            opacity = 1,
            size=10,
            line=dict(
                color='black',
                width=2
            )
        ),
        showlegend=False
    )
)

fig.show()

fig.write_html("tradespace_mc_test_ld_yaxis.html")
#fig.show()








#%%
### Plotting PDF and CDF for specific designs (our preferred concept)
det_F2C3H2L3 = det.loc[det['Name'] == 'F2C3H2L3']
det_util = det_F2C3H2L3['Total Utility']
def plot_mc_results(mc_results, x_label):
    plt.hist(mc_results, bins=100, density=True)
    plt.xlabel(x_label)
    plt.ylabel('PDF')
    plt.show()
    plt.hist(mc_results,bins=1000, density=True,cumulative=True, histtype='step',label = 'Cumulative Distribution')
    plt.xlabel(x_label)
    plt.ylabel('CDF')
    plt.vlines(np.array(mc_results).mean(),0,1,color='r',label='Monte Carlo Average')
    plt.scatter(np.median(np.array(mc_results)),0.5,c='r',label='Monte Carlo Median')
    plt.vlines(det_util,0,1,color='k',linestyle='--',label='Deterministic')
    plt.legend(loc='lower right')
    plt.show()

model_results_F2C3H2L3 = model_results.loc[model_results['Name'] == 'F2C3H2L3']

plot_mc_results(model_results_F2C3H2L3["Total Utility"], 'Total_Utility_MC')
#for key in decisions:
#    plot_mc_results(Aircraft('F1C1H1L2'), aircraft_mc_utility_results, 'Total_Utility_MC')
#    plot_mc_results(Aircraft('F1C1H1L2'), aircraft_mc_trl_results, 'AVG TRL_MC')


# %%
