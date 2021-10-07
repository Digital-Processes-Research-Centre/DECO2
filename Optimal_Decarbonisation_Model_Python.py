'''
Created on 6th October 2021

Energy Planning Scenario in Pyomo

This script presents the mathematical formulation for an energy planning 
scenario in a specific geographical region or district. Renewable energy 
sources and fossil-based source such as coal, oil and natural gas, 
each with its respectively energy contribution and carbon intensity make up 
the power generation in a specific region or district. Each period consists 
of its respective energy demand and carbon emission limit. 
NETs are utilised to achieve the emission limit.

@author: Purusothmn, Dr Michael Short

'''
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd
import os
from openpyxl import load_workbook

cwd = os.getcwd()

file = r'Optimal_Decarbonisation_User_Interface.xlsx'
plant_data = pd.read_excel(file, sheet_name = 'PLANT_DATA', index_col = 0, header = 29, nrows = 4).to_dict()
EP_data = pd.read_excel(file, sheet_name = 'EP_DATA', header = 11)
EG_data = pd.read_excel(file, sheet_name = 'ENERGY_DATA', header = 8)
SLD_data = pd.read_excel(file, sheet_name = 'ALT_SOLID', header = 8)
GAS_data = pd.read_excel(file, sheet_name = 'ALT_GAS', header = 8)
CCS_data = pd.read_excel(file, sheet_name = 'CCS_DATA', header = 12)
CI_NET_data = pd.read_excel(file, sheet_name = 'CI_NET_DATA', header = 9)
Cost_NET_data = pd.read_excel(file, sheet_name = 'COST_NET_DATA', header = 9)

s = plant_data.keys()

wb = load_workbook(file)
sheet = wb['PLANT_DATA']
flag = sheet['B27'].value

#Period number
prd = list(EP_data['Period'])

#Energy demand for each period
Demand = list(EP_data['Energy Demand'])

#Emission limit for each period
Limit = list(EP_data['Emission Limit'])

#Budget allocation for each period
Budget = list(EP_data['Budget'])

#Carbon intensity of first choice of compensatory energy for each period
Comp_CI_1 = list(EP_data['CI_COMP_1'])

#Cost of first choice compensatory energy for each period
Cost_Comp_1 = list(EP_data['COST_COMP_1'])

#Carbon intensity of second choice of compensatory energy for each period
Comp_CI_2 = list(EP_data['CI_COMP_2'])

#Cost of second choice compensatory energy for each period
Cost_Comp_2 = list(EP_data['COST_COMP_2'])

#Cost of renewable energy
Cost_REN = list(EG_data['REN'])

#Cost of natural gas
Cost_NG = list(EG_data['NG'])

#Cost of oil
Cost_OIL = list(EG_data['OIL'])

#Cost of coal
Cost_COAL = list(EG_data['COAL'])

#Carbon intensity of biomass tpye 1
SLD_CI_1 = list(SLD_data['SOLID_CI_1'])

#Cost of biomass type 1
SLD_Cost_1 = list(SLD_data['SOLID_COST_1'])

#Carbon intensity of biomass type 2
SLD_CI_2 = list(SLD_data['SOLID_CI_2'])

#Cost of biomass type 2
SLD_Cost_2 = list(SLD_data['SOLID_COST_2'])

#Carbon intensity of biomethane tpye 1
GAS_CI_1 = list(GAS_data['GAS_CI_1'])

#Cost of biomethane type 1
GAS_Cost_1 = list(GAS_data['GAS_COST_1'])

#Carbon intensity of biomethane tpye 2
GAS_CI_2 = list(GAS_data['GAS_CI_2'])

#Cost of biomethane type 2
GAS_Cost_2 = list(GAS_data['GAS_COST_2'])

#Removal ratio of first choice of CCS technology
RR_1 = list(CCS_data['RR_1'])

#Parisitic power loss of first choice of CCS technology
X_1 = list(CCS_data['X_1'])

#Cost of first choice of CCS technology
Cost_CCS_1 = list(CCS_data['Cost_CCS_1'])

#Removal ratio of second choice of CCS technology
RR_2 = list(CCS_data['RR_2'])

#Parisitic power loss of second choice of CCS technology
X_2 = list(CCS_data['X_2'])

#Cost of second choice of CCS technology
Cost_CCS_2 = list(CCS_data['Cost_CCS_2'])

#Fixed cost of first choice of CCS technology
FX_Cost_CCS_1 = list(CCS_data['FX_Cost_CCS_1'])

#Fixed cost of second choice of CCS technology
FX_Cost_CCS_2 = list(CCS_data['FX_Cost_CCS_2'])

#Carbon intensity of first choice of EP-NET for each period
EP_NET_1_CI = list(CI_NET_data['EP-NETs_1'])

#Carbon intensity of second choice of EP-NET for each period
EP_NET_2_CI = list(CI_NET_data['EP-NETs_2'])

#Carbon intensity of third choice of EP-NET for each period
EP_NET_3_CI = list(CI_NET_data['EP-NETs_3'])

#Cost of first choice of EP-NET for each period
Cost_EP_NET_1 = list(Cost_NET_data['EP-NETs_1'])

#Cost of second choice of EP-NET for each period
Cost_EP_NET_2 = list(Cost_NET_data['EP-NETs_2'])

#Cost of third choice of EP-NET for each period
Cost_EP_NET_3 = list(Cost_NET_data['EP-NETs_3'])

#Carbon intensity of first choice of EC-NET for each period
EC_NET_1_CI = list(CI_NET_data['EC-NETs_1'])

#Carbon intensity of second choice of EC-NET for each period
EC_NET_2_CI = list(CI_NET_data['EC-NETs_2'])

#Carbon intensity of third choice of EC-NET for each period
EC_NET_3_CI = list(CI_NET_data['EC-NETs_3'])

#Cost of first choice EC-NET for each period
Cost_EC_NET_1 = list(Cost_NET_data['EC-NETs_1'])

#Cost of second choice EC-NET for each period
Cost_EC_NET_2 = list(Cost_NET_data['EC-NETs_2'])

#Cost of third choice EC-NET for each period
Cost_EC_NET_3 = list(Cost_NET_data['EC-NETs_3'])

numperiods = len(prd) + 1
period_data_dict = {}

for (i,D,L,B,CI1,CC1,CI2,CC2,CRN,CNG,CO,CCL,SLDI1,SLDC1,SLDI2,SLDC2,GASI1,GASC1,GASI2,GASC2,RR1,X1,CCS1,RR2,X2,CCS2,FCCS1,FCCS2,EP1I,EP2I,EP3I,CEP1,CEP2,CEP3,EC1I,EC2I,EC3I,CEC1,CEC2,CEC3) in zip(prd, Demand, Limit, Budget, Comp_CI_1, Cost_Comp_1, Comp_CI_2, Cost_Comp_2, Cost_REN, Cost_NG, Cost_OIL, Cost_COAL, SLD_CI_1, SLD_Cost_1, SLD_CI_2, SLD_Cost_2, GAS_CI_1, GAS_Cost_1, GAS_CI_2, GAS_Cost_2, RR_1, X_1, Cost_CCS_1, RR_2, X_2, Cost_CCS_2, FX_Cost_CCS_1, FX_Cost_CCS_2, EP_NET_1_CI, EP_NET_2_CI, EP_NET_3_CI, Cost_EP_NET_1, Cost_EP_NET_2, Cost_EP_NET_3, EC_NET_1_CI, EC_NET_2_CI, EC_NET_3_CI, Cost_EC_NET_1, Cost_EC_NET_2, Cost_EC_NET_3):    
    period_data_dict[i]= {'Demand' : D, 
                          'Emission_Limit' : L,
			              'Budget'    : B,
			              'Comp_CI_1' : CI1,
                          'Cost_Comp_1' : CC1,
                          'Comp_CI_2' : CI2,
                          'Cost_Comp_2' : CC2,
                          'Cost_REN' : CRN,
                          'Cost_NG' : CNG,
                          'Cost_OIL' : CO,
                          'Cost_COAL' : CCL,
                          'SLD_CI_1' : SLDI1,
                          'SLD_Cost_1': SLDC1,
                          'SLD_CI_2' : SLDI2,
                          'SLD_Cost_2': SLDC2,
                          'GAS_CI_1' : GASI1,
                          'GAS_Cost_1': GASC1,
                          'GAS_CI_2' : GASI2,
                          'GAS_Cost_2': GASC2,
			              'RR_1' : RR1,
			              'X_1' : X1,
			              'Cost_CCS_1' : CCS1,
			              'RR_2' : RR2,
			              'X_2' : X2,
			              'Cost_CCS_2' : CCS2,
			              'FX_Cost_CCS_1' : FCCS1,
			              'FX_Cost_CCS_2' : FCCS2,
                          'EP_NET_1_CI' : EP1I,
                          'EP_NET_2_CI' : EP2I,
                          'EP_NET_3_CI' : EP3I,
                          'Cost_EP_NET_1' : CEP1,
                          'Cost_EP_NET_2' : CEP2,
                          'Cost_EP_NET_3' : CEP3,
                          'EC_NET_1_CI' : EC1I,
                          'EC_NET_2_CI' : EC2I,
                          'EC_NET_3_CI' : EC3I,
                          'Cost_EC_NET_1' : CEC1,
                          'Cost_EC_NET_2' : CEC2,
                          'Cost_EC_NET_3' : CEC3}
    
def EP_Period(plant_data,period_data): 
    model = pyo.ConcreteModel()
    model.S = plant_data.keys()
    model.plant_data = plant_data
    model.period_data = period_data
       
    #LIST OF VARIABLES
    
    #This variable determines the deployment of energy sources in power plant s
    model.energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of power plant s with CCS deployment type 1 for each period
    model.CI_RET_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of power plant s with CCS deployment type 2 for each period
    model.CI_RET_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #Binary variable for CCS deployment type 1 in power plant s for each period
    model.B = pyo.Var(model.S, domain = pyo.Binary)
    
    #Binary variable for CCS deployment type 2 in power plant s for each period
    model.C = pyo.Var(model.S, domain = pyo.Binary)
    
    #This variable represents the total extent of CCS retrofit in power plant s for each period
    model.CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the extent of CCS retrofit type 1 in power plant s for each period
    model.CCS_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals) 
    
    #This variable represents the extent of CCS retrofit type 2 in power plant s for each period
    model.CCS_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals) 
    
    #This variable determines the net energy available from power plant s without CCS deployment for each period
    model.net_energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with CCS deployment for each period
    model.net_energy_CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with CCS deployment type 1 for each period
    model.net_energy_CCS_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with CCS deployment type 2 for each period
    model.net_energy_CCS_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the first choice of EP_NETs for each period 
    model.EP_NET_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the second choice of EP_NETs for each period 
    model.EP_NET_2 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the third choice of EP_NETs for each period 
    model.EP_NET_3 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the first choice of EC_NETs for each period 
    model.EC_NET_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the second choice of EC_NETs for each period 
    model.EC_NET_2 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the third choice of EC_NETs for each period 
    model.EC_NET_3 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of first choice of renewable compensatory energy for each period
    model.comp_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of second choice of renewable compensatory energy for each period
    model.comp_2 = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the final total CO2 emission after energy planning for each period
    model.new_emission = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the total energy cost for each period
    model.energy_cost = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the total cost for each period
    model.sum_cost = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of solid fuel 1 for coal-based plants
    model.solid_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of solid fuel 2 for coal-based plants
    model.solid_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of gas fuel 1 for natural gas-based plants
    model.gas_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of gas fuel 2 for natural gas-based plants
    model.gas_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
       
    #OBJECTIVE FUNCTION
    
    #The objective function minimises the cumulative extent of CCS retrofit, thus minimising the NET requirement
    if flag == 'min_budget':
        model.obj = pyo.Objective(expr = model.sum_cost, sense = pyo.minimize)
    else:
        model.obj = pyo.Objective(expr = model.new_emission, sense = pyo.minimize)
   
    #CONSTRAINTS
    
    model.cons = pyo.ConstraintList()

    model.cons.add(sum(model.energy[s] for s in model.S) == model.period_data['Demand'])
    
    for s in model.S:
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
        model.cons.add((model.plant_data[s]['CI'] * (1 - model.period_data['RR_1']) / (1 - model.period_data['X_1'])) == model.CI_RET_1[s])
        
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
        model.cons.add((model.plant_data[s]['CI'] * (1 - model.period_data['RR_2']) / (1 - model.period_data['X_2'])) == model.CI_RET_2[s])
        
        #The deployment of energy source in power plant s should at least satisfy the lower bound
        model.cons.add(model.energy[s] >= model.plant_data[s]['LB'])
        
        #The deployment of energy source in power plant s should at most satisfy the upper bound
        model.cons.add(model.energy[s] <= model.plant_data[s]['UB'])
        
        #The total extent of CCS retrofit in power plant s should be equal to summation of deployment of individual types of  CCS technology
        model.cons.add(model.CCS_1[s] + model.CCS_2[s] ==  model.CCS[s])
    
        #The total extent of CCS retrofit in power plant s should never exceed the available energy
        model.cons.add(model.CCS[s] <= model.energy[s])
        
        #Determine the net energy available from power plant s with CCS retrofit type 1
        model.cons.add(model.CCS_1[s] * (1 - model.period_data['X_1']) == model.net_energy_CCS_1[s])
        
        #Determine the net energy available from power plant s with CCS retrofit type 2
        model.cons.add(model.CCS_2[s] * (1 - model.period_data['X_2']) == model.net_energy_CCS_2[s])
        
	    #If selected, the exent of CCS retrofit type 1 for power plant s is limited by the upper bound of the energy output 
        model.cons.add(model.CCS_1[s] <= model.plant_data[s]['UB'] * model.B[s])

    	#If selected, the exent of CCS retrofit type 2 for power plant s is limited by the upper bound of the energy output
        model.cons.add(model.CCS_2[s] <= model.plant_data[s]['UB'] * model.C[s])        

    	#Determine the net energy available from power plant s with CCS retrofit
        model.cons.add(model.net_energy_CCS_1[s] + model.net_energy_CCS_2[s] == model.net_energy_CCS[s])
        
        #The summation of energy contribution from each source with and without CCS retrofit must equal to individual energy contribution
        if 'REN' in model.plant_data[s].values():
            model.cons.add(model.net_energy[s] == model.energy[s])
        elif 'NG' in model.plant_data[s].values():
            model.cons.add(model.net_energy[s] + model.CCS_1[s] + model.CCS_2[s] + model.gas_1[s] + model.gas_2[s] == model.energy[s])
        elif 'COAL' in model.plant_data[s].values():
            model.cons.add(model.net_energy[s] + model.CCS_1[s] + model.CCS_2[s] + model.solid_1[s] + model.solid_2[s] == model.energy[s])
        else:
            model.cons.add(model.net_energy[s] + model.CCS_1[s] + model.CCS_2[s] == model.energy[s])
    
        if 'REN' in model.plant_data[s].values():
            model.CCS_1[s].fix(0)
            model.CCS_2[s].fix(0)       
        
    #Total energy contribution from all energy sources to satisfy the total demand
    model.cons.add(sum(((model.net_energy[s]) + model.net_energy_CCS_1[s] + model.net_energy_CCS_2[s] + model.solid_1[s] + model.solid_2[s] + model.gas_1[s] + model.gas_2[s]) for s in model.S) + model.comp_1 + model.comp_2 + model.EP_NET_1 + model.EP_NET_2 + model.EP_NET_3 == model.period_data['Demand'] + model.EC_NET_1 + model.EC_NET_2 + model.EC_NET_3) 
    
    #The total CO2 load contribution from all energy sources must satisfy most the CO2 emission limit after energy planning 
    model.cons.add(sum((model.net_energy[s] * model.plant_data[s]['CI']) + (model.net_energy_CCS_1[s] * model.CI_RET_1[s]) + (model.net_energy_CCS_2[s] * model.CI_RET_2[s]) + (model.solid_1[s] * model.period_data['SLD_CI_1']) + (model.solid_2[s] * model.period_data['SLD_CI_2']) + (model.gas_1[s] * model.period_data['GAS_CI_1']) + (model.gas_2[s] * model.period_data['GAS_CI_2']) for s in model.S)
               + (model.EC_NET_1 * model.period_data['EC_NET_1_CI'])
               + (model.EC_NET_2 * model.period_data['EC_NET_2_CI'])
               + (model.EC_NET_3 * model.period_data['EC_NET_3_CI'])
               + (model.EP_NET_1 * model.period_data['EP_NET_1_CI'])
               + (model.EP_NET_2 * model.period_data['EP_NET_2_CI'])
               + (model.EP_NET_3 * model.period_data['EP_NET_3_CI'])
               + (model.comp_1 * model.period_data['Comp_CI_1'])
               + (model.comp_2 * model.period_data['Comp_CI_2']) == model.new_emission)
    
    energy_cost = 0
    for s in model.S:
        if 'REN' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_REN'])
        elif 'NG' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_NG'])
        elif 'OIL' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_OIL'])
        else:
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_COAL'])
            
    #The summation of cost for each power plant s should equal to the total cost of each period
    model.cons.add(sum((model.net_energy_CCS_1[s] * model.period_data['Cost_CCS_1']) + (model.net_energy_CCS_2[s] * model.period_data['Cost_CCS_2']) + (model.period_data['FX_Cost_CCS_1'] * model.B[s]) + (model.period_data['FX_Cost_CCS_2'] * model.C[s]) + (model.solid_1[s] * model.period_data['SLD_Cost_1']) + (model.solid_2[s] * model.period_data['SLD_Cost_2']) + (model.gas_1[s] * model.period_data['GAS_Cost_1']) + (model.gas_2[s] * model.period_data['GAS_Cost_2']) for s in model.S)
               + (model.EC_NET_1 * model.period_data['Cost_EC_NET_1'])
               + (model.EC_NET_2 * model.period_data['Cost_EC_NET_2'])
               + (model.EC_NET_3 * model.period_data['Cost_EC_NET_3'])
               + (model.EP_NET_1 * model.period_data['Cost_EP_NET_1'])
               + (model.EP_NET_2 * model.period_data['Cost_EP_NET_2'])
               + (model.EP_NET_3 * model.period_data['Cost_EP_NET_3'])
               + (model.comp_1 * model.period_data['Cost_Comp_1'])
               + (model.comp_2 * model.period_data['Cost_Comp_2'])
               + energy_cost == model.sum_cost) 
    
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    if flag == 'min_budget':
        model.cons.add(model.new_emission == model.period_data['Emission_Limit'])
    else:
        model.cons.add(model.sum_cost <= model.period_data['Budget'])

    return model

#Creating a list with 3 strings
block_sets = list(range(1, numperiods, 1))

#Adding the models to a dictionary to be accessed inside the function
EP = dict()
for i in range(1, numperiods, 1):
    EP[block_sets[i-1]] = EP_Period(plant_data, period_data_dict[i])

Full_model = pyo.ConcreteModel()

'''
This function defines each block - the block is model m containing all equations and variables
It needs to be put in the right set (block_sets) with objective function turned off
'''
def build_individual_blocks(model, block_sets):
    model = EP[block_sets]
    model.obj.deactivate()
    model.del_component(model.obj)
    return model

#Defining the pyomo block structure with the set block sets and rule to build the blocks
Full_model.subprobs = pyo.Block(block_sets, rule = build_individual_blocks)

'''
The blocks are linked such that the extent of CCS retrofit on source i at period t + 1
should at least match the extent of CCS retrofit on source i at period t
'''

def linking_blocks_1(model, block_sets, s):
    if block_sets == len(prd):
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].CCS_1[s] >=  Full_model.subprobs[block_sets].CCS_1[s]
    
def linking_blocks_2(model, block_sets, s):
    if block_sets == len(prd):
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].CCS_2[s] >=  Full_model.subprobs[block_sets].CCS_2[s]
        
Full_model.Cons1 = pyo.Constraint(block_sets, s, rule = linking_blocks_1)
Full_model.Cons2 = pyo.Constraint(block_sets, s, rule = linking_blocks_2)

'''
Creating a new objective function for the new model
The objective minimises the cumulative extent of CCS retrofit from all fossil-based sources
'''
TCOST = 0
TEMIS = 0
for i in range(1, numperiods, 1):
    TCOST = TCOST + Full_model.subprobs[i].sum_cost
    TEMIS = TEMIS + Full_model.subprobs[i].new_emission
    
if flag == 'min_budget':
    Full_model.obj = pyo.Objective(expr = TCOST, sense = pyo.minimize)
else:
    Full_model.obj = pyo.Objective(expr = TEMIS, sense = pyo.minimize)

#Using octeract engine solver to solve the energy planning model
opt = SolverFactory('octeract-engine')
results = opt.solve(Full_model)
print(results)
'''
Creating a fuction to publish the results energy planning scenario for a single period

Args:
    source_data = The energy and carbon intensity for [Period Number] 
    period_data = The energy planning data for [Period Number]
    period = Time period involved ('P1' or 'P2' or 'P3')
    
returns:
    the results from variables in the energy planning model, 
    a data table with the energy and emission contribution from each energy source,
    and energy planning pinch diagram
'''

def EP_Results(plant_data, period_data, period):
    model = Full_model.subprobs[period]    
    
    energy_planning = pd.DataFrame()

    for s in plant_data.keys():
        energy_planning.loc[s, 'Fuel'] = plant_data[s]['Fuel']
        energy_planning.loc[s, 'Energy'] = round(model.energy[s](), 2)
        energy_planning.loc[s, 'CI'] = plant_data[s]['CI']
        #energy_planning.loc[s, 'CCS_1 CI'] = round(model.CI_RET_1[s](), 3)
        #energy_planning.loc[s, 'CCS_2 CI'] = round(model.CI_RET_2[s](), 3)
        energy_planning.loc[s, 'CCS_1 Selection'] = model.B[s]()
        energy_planning.loc[s, 'CCS_2 Selection'] = model.C[s]()
        energy_planning.loc[s, 'CCS_1 Ret'] = round(model.CCS_1[s](), 2) 
        energy_planning.loc[s, 'CCS_2 Ret'] = round(model.CCS_2[s](), 2)       
        #energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[s](), 2)
        #energy_planning.loc[s, 'Net Energy w CCS'] = round(model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'SOLID_1'] = round(model.solid_1[s](), 2)
        energy_planning.loc[s, 'SOLID_2'] = round(model.solid_2[s](), 2)
        energy_planning.loc[s, 'GAS_1'] = round(model.gas_1[s](), 2)
        energy_planning.loc[s, 'GAS_2'] = round(model.gas_2[s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[s]() + model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[s]() * plant_data[s]['CI']) + (model.net_energy_CCS_1[s]() * model.CI_RET_1[s]()) + (model.net_energy_CCS_2[s]() * model.CI_RET_2[s]()), 2)
        
    energy_planning.loc['EP_NET_1', 'Fuel'] = 'EP_NET_1'
    energy_planning.loc['EP_NET_2', 'Fuel'] = 'EP_NET_2'
    energy_planning.loc['EP_NET_3', 'Fuel'] = 'EP_NET_3'
    energy_planning.loc['EC_NET_1', 'Fuel'] = 'EC_NET_1'
    energy_planning.loc['EC_NET_2', 'Fuel'] = 'EC_NET_2' 
    energy_planning.loc['EC_NET_3', 'Fuel'] = 'EC_NET_3' 
    energy_planning.loc['EP_NET_1', 'CI'] = model.period_data['EP_NET_1_CI']
    energy_planning.loc['EP_NET_2', 'CI'] = model.period_data['EP_NET_2_CI']
    energy_planning.loc['EP_NET_3', 'CI'] = model.period_data['EP_NET_3_CI']
    energy_planning.loc['EC_NET_1', 'CI'] = model.period_data['EC_NET_1_CI']
    energy_planning.loc['EC_NET_2', 'CI'] = model.period_data['EC_NET_2_CI'] 
    energy_planning.loc['EC_NET_3', 'CI'] = model.period_data['EC_NET_3_CI']        
    energy_planning.loc['EP_NET_1', 'Net Energy'] = round(model.EP_NET_1(), 2)
    energy_planning.loc['EP_NET_2', 'Net Energy'] = round(model.EP_NET_2(), 2)
    energy_planning.loc['EP_NET_3', 'Net Energy'] = round(model.EP_NET_3(), 2)
    energy_planning.loc['EC_NET_1', 'Net Energy'] = round(model.EC_NET_1(), 2)
    energy_planning.loc['EC_NET_2', 'Net Energy'] = round(model.EC_NET_2(), 2)
    energy_planning.loc['EC_NET_3', 'Net Energy'] = round(model.EC_NET_3(), 2)
    energy_planning.loc['EP_NET_1', 'Carbon Load'] = round(model.EP_NET_1() * model.period_data['EP_NET_1_CI'], 2)
    energy_planning.loc['EP_NET_2', 'Carbon Load'] = round(model.EP_NET_2() * model.period_data['EP_NET_2_CI'], 2)
    energy_planning.loc['EP_NET_3', 'Carbon Load'] = round(model.EP_NET_3() * model.period_data['EP_NET_3_CI'], 2)
    energy_planning.loc['EC_NET_1', 'Carbon Load'] = round(model.EC_NET_1() * model.period_data['EC_NET_1_CI'], 2)
    energy_planning.loc['EC_NET_2', 'Carbon Load'] = round(model.EC_NET_2() * model.period_data['EC_NET_2_CI'], 2)
    energy_planning.loc['EC_NET_3', 'Carbon Load'] = round(model.EC_NET_3() * model.period_data['EC_NET_3_CI'], 2)
    energy_planning.loc['COMP_1', 'Fuel'] = 'COMP_1'  
    energy_planning.loc['COMP_2', 'Fuel'] = 'COMP_2'
    energy_planning.loc['COMP_1', 'CI'] = model.period_data['Comp_CI_1']  
    energy_planning.loc['COMP_2', 'CI'] = model.period_data['Comp_CI_2']
    energy_planning.loc['COMP_1', 'Net Energy'] = round(model.comp_1(),2) 
    energy_planning.loc['COMP_1', 'Carbon Load'] = round(model.comp_1() * model.period_data['Comp_CI_1'], 2)
    energy_planning.loc['COMP_2', 'Net Energy'] = round(model.comp_2(),2) 
    energy_planning.loc['COMP_2', 'Carbon Load'] = round(model.comp_2() * model.period_data['Comp_CI_2'], 2)
    energy_planning.loc['TOTAL', 'Carbon Load'] = round(model.new_emission(), 2)
    energy_planning.loc['TOTAL', 'Cost'] = round(model.sum_cost(), 2)
    
    writer = pd.ExcelWriter(file, engine = 'openpyxl', mode = 'a')
    energy_planning.to_excel(writer, sheet_name = 'Results_Period_1')
    writer.save()
    
    return    

for i in range (1, numperiods,1):
    EP_Results(plant_data, period_data_dict[i], i)
