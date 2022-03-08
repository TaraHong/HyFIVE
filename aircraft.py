import params
import math

class Aircraft():
    """ Creating a HyFIVE aircraft """
    '''
    So far, I implemented the followings:
    - Jet Fuel Usage (kg)
    - Hydrogen Fuel Usage (kg)
    - CO2 Reduction (%)
    - Reliability Utility (0-1)
    - Payload (kg)

    #TODO
    - Calculate PAX (DONE)
    - Calculate PAX Utility (DONE)
    - Calculate Range (DONE)
    - Calculate Total Utility (DONE)
    - Calculate AVG TRL (DONE)
    - There is a bug in EXCEL model to calculate jet_range (FIXED)
    - For a few architectural decisions, create a scatter plot with Utility vs AVG TRL (DONE)
    
    '''

    #attributes
    def __init__(self, name):
        #"F3C5H3L3"
        self.name = name
        self.config = name[2:4]
        self.fcs = name[0:2]
        self.hex = name[4:6]
        self.location = name[6:8]



    #methods
    def calc_jet_fuel(self):
        #print("Calculate Jet Fuel Usage")
        config = self.config
        match config:
            case "C1":
                jet_fuel = params.JET_FUEL_MAX * params.LANDING_RATIO
                #print("Jet Fuel Usage:", jet_fuel ," kg")
                return jet_fuel
            case "C2":
                jet_fuel = params.JET_FUEL_MAX * params.LANDING_RATIO * params.BATTERY_BUFFER
                #print("Jet Fuel Usage:", jet_fuel ," kg")
                return jet_fuel
            case "C3":
                jet_fuel = 0
                #print("Jet Fuel Usage:", jet_fuel ," kg")
                return jet_fuel
            case "C4":
                jet_fuel = 0 
                #print("Jet Fuel Usage:", jet_fuel ," kg")
                return jet_fuel
            case "C5":
                jet_fuel = params.JET_FUEL_MAX
                #print("Jet Fuel Usage:", jet_fuel ," kg")
                return jet_fuel
    
    def calc_LH2_fuel(self):
        #print("Calculate LH2 Fuel Usage")
        config = self.config
        match config:
            case "C1":
                LH2_fuel = params.JET_FUEL_MAX * params.CRUISE_RATIO * params.MASS_RATIO_J_H
                #print("LH2 Fuel Usage:", LH2_fuel ," kg")
                return LH2_fuel
            case "C2":
                LH2_fuel = params.JET_FUEL_MAX * params.CRUISE_RATIO * params.MASS_RATIO_J_H
                #print("LH2 Fuel Usage:", LH2_fuel ," kg")
                return LH2_fuel
            case "C3":
                LH2_fuel = params.JET_FUEL_MAX * params.FULL_ELECTRIC_RATIO * params.MASS_RATIO_J_H - params.JET_FUEL_MAX * params.LANDING_RATIO * params.MASS_RATIO_J_H * params.FULL_ELECTRIC_RATIO * (1-params.BATTERY_BUFFER)
                #print("LH2 Fuel Usage:", LH2_fuel ," kg")
                return LH2_fuel
            case "C4":
                LH2_fuel = params.JET_FUEL_MAX * params.FULL_ELECTRIC_RATIO * params.MASS_RATIO_J_H
                #print("LH2 Fuel Usage:", LH2_fuel ," kg")
                return LH2_fuel
            case "C5":
                LH2_fuel = 0
                #print("LH2 Fuel Usage:", LH2_fuel ," kg")
                return LH2_fuel

    def calc_co2_reduction(self):    
        jet_fuel_reduction = params.JET_FUEL_MAX - self.calc_jet_fuel()
        CO2_emission_redution = jet_fuel_reduction/params.JET_FUEL_MAX * 100 #%
        #print("CO2 reduction:", CO2_emission_redution, "%")
        return CO2_emission_redution

    def utility_co2(self):
        CO2_utility = self.calc_co2_reduction()*0.01 
        #print("CO2 Utility: ", CO2_utility )
        return CO2_utility    


    def calc_reliability(self):
        aircraft_type = self.fcs + self.config
        match aircraft_type:
            case "F1C1":
                rel = 0.85
                #print("Reliability Utility: ", rel)
                return rel
            case "F1C2":
                rel = 0.9
                #print("Reliability Utility: ", rel)
                return rel
            case "F1C3":
                rel = 0.75
                #print("Reliability Utility: ", rel)
                return rel  
            case "F1C4":
                rel = 0.7
                #print("Reliability Utility: ", rel)
                return rel 
            case "F2C1":
                rel = 0.95
                #print("Reliability Utility: ", rel)
                return rel
            case "F2C2":
                rel = 1
                #print("Reliability Utility: ", rel)
                return rel
            case "F2C3":
                rel = 0.9
                #print("Reliability Utility: ", rel)
                return rel
            case "F2C4":
                rel = 0.85
                #print("Reliability Utility: ", rel)
                return rel
            case "F3C5":
                rel = 0.9
                #print("Reliability Utility: ", rel)
                return rel



    def calc_payload(self): 
        if self.hex == 'H1':
            hex_weight = params.H1_MASS
        elif self.hex == 'H2':
            hex_weight = params.H2_MASS
        else:
            hex_weight = 0 

        fuel_weight = self.calc_jet_fuel() + self.calc_LH2_fuel()

        aircraft_type = self.fcs + self.config     
        match aircraft_type:
            case "F1C1":
                fcs_weight = params.FCS_MASS               
                baseline_change = fcs_weight + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F1C2":
                fcs_weight = params.FCS_MASS + params.BATTERY_MASS
                baseline_change = fcs_weight + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F1C3": #All electric, no gas engine 
                fcs_weight = params.FCS_MASS + params.BATTERY_MASS - params.PW_127 * params.ENGINE_MASS_PENALTY
                electric_premium = hex_weight * (params.HEX_PREMIUM_FE-1)
                baseline_change = fcs_weight + electric_premium + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F1C4":
                fcs_weight = params.FCS_MASS - params.PW_127 * params.ENGINE_MASS_PENALTY
                electric_premium = hex_weight * (params.HEX_PREMIUM_FE-1)
                baseline_change = fcs_weight + electric_premium + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F2C1":
                fcs_weight = params.FCS2_MASS
                fc2_premium = hex_weight * (params.HEX_PREMIUM_F2-1)
                baseline_change = fcs_weight + fc2_premium + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F2C2":
                fcs_weight = params.FCS2_MASS + params.BATTERY_MASS
                fc2_premium = hex_weight * (params.HEX_PREMIUM_F2-1)
                baseline_change = fcs_weight + fc2_premium + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F2C3":
                fcs_weight = params.FCS2_MASS + params.BATTERY_MASS - params.PW_127 * params.ENGINE_MASS_PENALTY
                #print(fcs_weight)
                fc2_premium = hex_weight * (params.HEX_PREMIUM_F2-1)
                #print(fc2_premium)
                electric_premium = (fc2_premium + hex_weight) * (params.HEX_PREMIUM_FE-1)
                #print(electric_premium)
                baseline_change = fcs_weight + fc2_premium + electric_premium + hex_weight
                #print(baseline_change)
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F2C4":
                fcs_weight = params.FCS2_MASS - params.PW_127 * params.ENGINE_MASS_PENALTY
                fc2_premium = hex_weight * (params.HEX_PREMIUM_F2-1)
                electric_premium = (fc2_premium + hex_weight) * (params.HEX_PREMIUM_FE-1)
                baseline_change = fcs_weight + fc2_premium + electric_premium + hex_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.SUPPORTING_SYS + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload
            case "F3C5":
                fcs_weight = 0
                baseline_change = fcs_weight
                payload = params.MTOW - (fuel_weight + baseline_change + params.OWE)
                #print("Payload: ", payload, "kg")
                return payload

    def calc_PAX(self):
        payload = self.calc_payload() 
        jet_usage = self.calc_jet_fuel() 
        LH2_usage = self.calc_LH2_fuel()
        jet_vol = jet_usage * 1000/840/1000
        LH2_vol = LH2_usage * 1000/70.8/1000
        total_fuel_vol = jet_vol + LH2_vol
        extra_storage_needed = total_fuel_vol - params.BASELINE_TANK
        
        location = self.location 
        if location == "L3":
            vol_remaining = params.BASELINE_FUS_VOL - extra_storage_needed
        else: 
            vol_remaining = params.BASELINE_FUS_VOL
        
        pax_volume = vol_remaining / params.V_PER_PERSON
        pax_weight = payload / params.M_PER_PERSON
        pax = math.floor(min(pax_volume, pax_weight))
        #print("PAX: ", pax)
        return pax
    
    def calc_pax_utility(self):
        pax = self.calc_PAX()
        pax_processed = math.floor(pax * (32/22))
        if pax_processed <= 8:
            pax_utility = 0
            #return pax_utility
        elif pax_processed >= 30:
            pax_utility = 1
            #return pax_utility
        else:
            pax_utility = -0.0012 * pax_processed**2 + 0.092 * pax_processed - 0.6909
        return pax_utility

    def calc_lift_to_drag(self):
        payload = self.calc_payload() 
        jet_usage = self.calc_jet_fuel() 
        LH2_usage = self.calc_LH2_fuel()
        jet_vol = jet_usage * 1000/840/1000
        LH2_vol = LH2_usage * 1000/70.8/1000
        total_fuel_vol = jet_vol + LH2_vol
        extra_storage_needed = total_fuel_vol - params.BASELINE_TANK
        storage_multiplier = total_fuel_vol/params.BASELINE_TANK
        
        location = self.location
        if location == "L3":
            lift_to_drag_multiplier = 1
            lift_to_drag_premium = 1 
        elif location == "L2":
            lift_to_drag_multiplier = 0.5
            lift_to_drag_premium = (storage_multiplier - params.STORAGE_MIN)/(params.STORAGE_MAX - params.STORAGE_MIN) * lift_to_drag_multiplier + 1

        else: #L1 
            lift_to_drag_multiplier = 0.5
            lift_to_drag_premium = ((storage_multiplier - params.STORAGE_MIN)/(params.STORAGE_MAX - params.STORAGE_MIN) * lift_to_drag_multiplier + 1) * 1.05

        return lift_to_drag_premium


    def calc_range(self): 
        config = self.config
        lift_to_drag_premium = self.calc_lift_to_drag()
        jet_usage = self.calc_jet_fuel() 
        LH2_usage = self.calc_LH2_fuel()
        jet_fuel_reserve = params.JET_FUEL_RESERVE
        jet_fuel_takeoff = params.JET_FUEL_TAKEOFF
        LH2_fuel_reserve = params.LH2_FUEL_RESERVE
        LH2_fuel_takeoff = params.LH2_FUEL_TAKEOFF
        if ((config == "C3") or (config == "C4")): #Full Electric
            jet_fuel_reserve = 0
            jet_fuel_takeoff = 0 
        else: #hybrid
            LH2_fuel_reserve = 0
            LH2_fuel_takeoff = 0

        weight_initial_jet = params.MTOW - jet_fuel_takeoff
        weight_final_jet = weight_initial_jet - (jet_usage - jet_fuel_takeoff) + jet_fuel_reserve
        log_weight_jet = math.log(weight_initial_jet/weight_final_jet)
        ### This jet_range equation is wrong - need to follow fc_range equation (dividing by L/D premium)
        if ((config == "C1") or (config == "C2") or (config == "C5")): #Hybrid
            #jet_range = (params.VELOCITY * lift_to_drag_premium * params.LIFT_TO_DRAG * log_weight_jet)/(10**-6 * params.SFC_JET * params.GRAVITY)/1000
            jet_range = (params.VELOCITY * params.LIFT_TO_DRAG/lift_to_drag_premium * log_weight_jet)/(10**-6 * params.SFC_JET * params.GRAVITY)/1000
            params.LH2_FUEL_RESERVE = 0 
        else: #Full Electric
            jet_range = 0
        
        weight_initial_hybrid = weight_final_jet - LH2_fuel_takeoff      
        weight_final_hybrid = weight_initial_hybrid - (LH2_usage - LH2_fuel_takeoff) + LH2_fuel_reserve
        log_weight_hybrid = math.log(weight_initial_hybrid/weight_final_hybrid)        
        fc_range = (params.VELOCITY * params.LIFT_TO_DRAG/lift_to_drag_premium * log_weight_hybrid)/(10**-6 * params.SFC_HYBRID * params.GRAVITY)/1000
        if ((config == "C2") or (config == "C3")):
            electric_range = (jet_range + fc_range) * 0.05
        else:
            electric_range = 0

        range = jet_range + fc_range + electric_range    
        return range

    def calc_range_utility(self):
        range = self.calc_range()
        range_utility = range/params.BASELINE_RANGE
        return range_utility


    def calc_AVG_TRL(self):
        #TRL
        trl = params.trl
        fcs = self.fcs
        config = self.config
        hex = self.hex
        location = self.location

        fcs_trl = trl[fcs]
        config_trl = trl[config]
        hex_trl = trl[hex]
        location_trl = trl[location]

        avg_trl = 0.2 * fcs_trl + 0.25 * config_trl + 0.2 * hex_trl + 0.25 * location_trl
        return avg_trl





