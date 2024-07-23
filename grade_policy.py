#grading_methodology
import os 
import csv
import sys
import pandas as pd

X_CITIES: list[str] = ['Kolkata', 'Calcutta']
Y_CITIES: list[str] = ['Asansol','Burdwan' , 'Durgapur', 'Siliguri']
AVG_MPCE_MED_WB_RURAL:float=6529.824
AVG_MPCE_MED_WB_URBAN:float=9480.6
PCI_WB:float=141373
INP_HOSPITAL_COST_RURAL:int=13310
INP_HOSPITAL_COST_URBAN:int=25235
OPD_HOSPITAL_COST_RURAL:int=500
OPD_HOSPITAL_COST_URBAN:int=2700
TOTAL_HCS_WB:int=12000

class Human:
    #this function has the default attributes for a given human who has purchased a particular health insurance plan. the parameters with the default data types will 
    #filled in later on
    def __init__(self) -> None:
        self.age:int=0
        self.gen:str=""
        self.premium:float=0.0
        self.pre_exist:bool=False
        self.relation:str="self" #can later be changed to spouse, parent or child
        self.area_zone:int=0 #1 for tier-1, 2 for tier-2, and so on
        self.plan_type:int=0
        self.base_sum_pers_accident:float=0
        self.plan_fam_cat:str="" #family, family_indiv or floater

class Pers_Accident:
    def __init__(self) -> None:
        #sum insured
        self.min_sum:float=float(input("Enter minimum sum insured="))
        self.max_sum:float=float(input("Enter maximum sum insured="))
        
        #rate per mille on premium per cover
        self.prem_rate_ad:float=float(input("Enter premium rate per mille for accidental death="))
        self.prem_rate_ppd:float=float(input("Enter premium rate per mille for permanent partial disability="))
        self.prem_rate_ptd:float=float(input("Enter premium rate per mille for permanent total disability="))
        self.prem_rate_ttd:float=float(input("Enter premium rate per mille for temporary total disability=")) 
        self.prem_rate_additional:float=float(input("Enter net premium rate per mille for additional covers="))
        
        #net premium for family
        self.total_premium:float=0.0
        
        #policy provisions
        self.max_opd_coverage:float=float(input("Enter the total amount covered for OPD for the base 5lakh/chosen plan="))
        self.daily_hospicash_provision:float=float(input("Enter the amount provided daily as hospital cash for the base 5lakh/chosen plan="))
        self.fracture:str=input("Input whether fractures and broken bones are covered (T/F):")
        self.fracture:bool=self.fracture.lower()=='t' or self.fracture.lower()=='true'
        self.elderly:str=input("Input whether elder care is covered (T/F):")
        self.elderly:bool=self.elderly.lower()=='t' or self.elderly.lower()=='true'
        self.child_edu:str=input("Input whether child's education is covered (T/F):")
        self.child_edu:bool=self.child_edu.lower()=='t' or self.child_edu.lower()=='true'
        self.copayment_discount:float=float(input("Enter copayment discount, if applicable for your chosen plan:"))
        self.loading:float=float(input("Enter loading% on premium if applicable (enter 0 if NA):"))
        self.floater_disc:float=float(input("Enter floater discount%, if applicable for chosen plan:"))
        
        #net score for policy
        self.net_score:float=0.0

class Senior_Citizen:
    def __init__(self) -> None:
        #sum insured
        self.min_sum:float=float(input("Enter the minimum sum insured:"))
        
        #maximum age at entry
        self.max_age:float=int(input("Enter the maximum age at entry:"))
        
        #policy provisions
        self.waiting_per:float=float(input("Enter waiting period for pre-existing diseases for the base plan, if applicable:"))
        self.loading:float=float(input("Enter loading% if applicable (enter 0 if NA):"))
        self.min_copayment:float=float(input("Enter any copayment, if applicable/opted for (enter 0 if NA):"))
        if self.min_copayment!=0.0:
            self.copayment_discount:float=float(input("Enter copayment discount, if applicable (enter 0 if NA):"))
        else:
            self.copayment_discount:float=0.0
        self.floater_disc:float=float(input("Enter floater discount% if applicable:"))
        self.max_postcare_coverage:str=input("Enter amount of postcare costs covered (enter NA if not clear):")
        if self.max_postcare_coverage.lower()=='na':
            self.max_postcare_coverage:int=int(input("Enter no. of days covered:"))
        else:
            self.max_postcare_coverage:float=float(self.max_postcare_coverage)
        self.precare_days:float=float(input("Enter the number of days covered under pre-hospitalization:"))
        self.checkup:str=input("Enter whether multiple health check-ups are covered (in true or false):")
        self.checkup:bool=self.checkup.lower()=='true'
        
        #net premium amount for the chosen family
        self.total_premium:float=0.0
        
        #net score for the policy in question
        self.net_score:float=0.0
        
    #this is only initiated when the plan is specifically for senior citizen care - where all members insured are minimum 60+ 
    #this DOES not include policies that provide cover for senior citizens as an in-built benefit - there are only 15 such plans 

class Criti_Care:
    def __init__(self) -> None:
        #sum insured
        self.min_sum:float=float(input("Enter the minimum sum insured:"))
        self.max_sum:float=float(input("Enter maximum sum ensured under the plan:")) #compare this value with the average cost required for comprehensive health care for procedures related to critical care illnesses 
        self.sum_insured:float=float(input("Enter sum insured for your chosen plan:"))
        
        #premium rate per mille on the base sum insured
        self.rate_permille:float=float(input("Enter rate per mille on your base sum insured to calculate your premium:"))
        
        #policy provisions
        self.floater_disc:float=float(input("Enter floater discount, if applicable (enter 0 if NA):"))
        self.disease_cov:float=int(input("Enter the total number of critical care illnesses and procedures that are covered:"))
        self.voluntary_ded_disc:float=float(input("Enter the deductible discount, if opted for (enter 0 if NA):"))
        self.min_copayment:float=float(input("Enter any copayment, if applicable/opted for (enter 0 if NA):"))
        if self.min_copayment!=0.0:
            self.copayment_discount:float=float(input("Enter copayment discount, if applicable (enter 0 if NA):"))
        else:
            self.copayment_discount:float=0.0
        self.loading:float=float(input("Enter loading on premium if applicable (enter 0 if NA):"))
        self.precare_days:float=float(input("Enter the number of days covered under pre-hospitalization:"))
        self.max_postcare_coverage:str=input("Enter amount of postcare costs covered (enter NA if not clear):")
        if self.max_postcare_coverage.lower()=='na':
            self.max_postcare_coverage:int=int(input("Enter no. of days covered:"))
        else:
            self.max_postcare_coverage:float=float(self.max_postcare_coverage)
        self.waiting_per:int=int(input("Enter waiting period for pre-existing diseases (in months):"))
        
        #net premium for the chosen family for the policy in question
        self.total_premium:float=0.0
        
        #net score for the policy in question 
        self.net_score:float=0.0 
        
        

class Top_Up:
    def __init__(self) -> None:
        #deductible and copayment
        self.min_deductible:float=float(input("Enter the base aggregate deductible for the base plan:")) #usually top_up plans have deductibles - so the lowest aggregate deductible. The lower the deductible amount, the higher the score
        self.voluntary_ded_disc:float=float(input("Enter the deductible discount% on premium, if applicable (enter 0 if NA):"))
        self.min_copayment:float=float(input("Enter any copayment, if applicable/opted for (enter 0 if NA):"))
        if self.min_copayment!=0.0:
            self.copayment_discount=float(input("Enter copayment discount, if applicable (enter 0 if NA):"))
        else:
            self.copayment_discount:float=0.0 
        
        #policy provisions
        self.family_mem_cov:int=int(input("Enter the maximum number of family members who can be covered by the plan:"))
        self.floater_disc:float=float(input("Enter floater discount% on premium, if applicable:"))
        self.load_prem:float=float(input("Enter loading% on premium if applicable (enter 0 if NA):")) 
        self.waiting_per:float=int(input("Enter waiting period for pre-existing diseases in months:"))
        self.max_opd_cost:float=float(input("Enter maximum amount of OPD costs that are covered:"))
        self.precare_days:float=float(input("Enter the number of days covered under pre-hospitalization:"))
        self.max_postcare_coverage:str=input("Enter amount of postcare costs covered (enter NA if not clear):")
        if self.max_postcare_coverage.lower()=='na':
            self.max_postcare_coverage:int=int(input("Enter no. of days covered:"))
        else:
            self.max_postcare_coverage:float=float(self.max_postcare_coverage)
        self.hosp_net:int=int(input("Enter total number of hospitals covered:"))
        
        #net score for the chosen policy
        self.net_score:float=0.0
        
        #net premium for the family in question for the chosen policy
        self.total_premium:float=0.0

class Policy:
    def __init__(self) -> None:
        #sum insured
        self.lowest_sum:float=float(input("Enter lowest base sum insured:"))
        
        #loading
        self.loading:float=float(input("Enter loading% on premium if applicable (enter 0 if NA):"))
        
        #applicable discounts
        self.floater_disc:float=float(input("Enter floater discount, if applicable:"))
        self.family_disc:float=float(input("Enter additional applicable family discount (enter 0 if NA):"))
        self.deductible_discount:float=float(input("Enter aggregate deductible discount, if applicable (enter 0 if NA):"))
        self.disc_gen:float=float(input("Enter discount based on gender, if applicable (enter 0 if NA):"))
        self.disc_age:float=float(input("Enter discount based on age of insured if applicable (enter 0 if NA):"))
        if self.disc_age!=0.0:
            self.inner_lim_age:int=int(input("Enter minimum age for the age discount to apply, if applicable for taken plan:"))
        else:
            self.inner_lim_age:int=0
        self.disc_relation_spouse:float=float(input("Enter discount% for spouse, if applicable (enter 0 if NA):"))
        self.disc_relation_child:float=float(input("Enter discount% for child, if applicable (enter 0 if NA):"))
        
        self.opd_yn:str=input("Enter whether OPD costs are covered (T/F):")
        self.opd_yn:bool=self.opd_yn.lower()=='t'or self.opd_yn.lower()=='true'
        if self.opd_yn:
            self.opd_coverage:float=float(input("Enter cost of OPD that is covered, if applicable and present:"))
        else:
            self.opd_coverage:float=0.0
            
        #other policy provisions
        self.family_mem_cov:int=int(input("Enter maximum number of family members who can be covered under the plan:"))
        self.hosp_net:int=int(input("Enter the total number of hospitals covered by the insurer in your area:"))
        self.waiting_per:int=int(input("Enter the waiting for pre-existing diseases in months:"))
        self.auto_resto:str=input("Enter whether provision for auto restoration of sum insured is present (T/F):")
        self.auto_resto:bool=self.auto_resto.lower()=='t' or self.auto_resto.lower()=='true'
        
        #net premium for the family for the chosen policy
        self.net_prem:float=0.0
        
        #net score for the chosen policy
        self.net_score:float=0.0
        
def members_input():
    global family
    family=[]
    num=int(input("Enter number of family members:"))
    for i in range(num):
        family.append(Human())

def weightage_input(weightage):
    weightage_importance: dict[int, float]={1:0.26, 2:0.22, 3:0.18, 4:0.14, 5:0.10, 6:0.06, 7:0.04}
    print("Rank each category in importance to you/your family, from 1-7")
    for i in weightage.keys():
        weightage[i]=int(input(f'Enter the rank for {i}:'))
        weightage[i]=weightage_importance.get(weightage[i], 0.01)
    return weightage

def prem_ratio(cost):
    if family[0].area_zone==1 or family[0].area_zone==2:
        med_expend=AVG_MPCE_MED_WB_URBAN*len(family)
    else:
        med_expend=AVG_MPCE_MED_WB_RURAL*len(family)
    if cost>=med_expend:
        return 0
    else:
        return (cost/med_expend)

def lowest_sum(min_sum):
    if min_sum>500000:
        print("The starting premium will be higher than the govt. sector plans.") 
        return 0
    else: 
        return 1

def opd_coverage(max_opd_coverage):
    if max_opd_coverage==0.0:
        return 0
    else:
        if (family[0].area_zone!=1 and family[0].area_zone!=2):
            if max_opd_coverage<=OPD_HOSPITAL_COST_RURAL:
                return 0
            else:
                return 100*((max_opd_coverage/OPD_HOSPITAL_COST_RURAL)-1) 
        else: 
            if max_opd_coverage<=OPD_HOSPITAL_COST_URBAN:
                return 0
            else:
                return 100*((max_opd_coverage/OPD_HOSPITAL_COST_URBAN)-1)
        
def hospicash(daily_hospicash_provision):
    if daily_hospicash_provision==0.0:
        return 0
    else:
        if (family[0].area_zone!=1 and family[0].area_zone!=2):
            if daily_hospicash_provision>INP_HOSPITAL_COST_RURAL:
                return 1
            else: 
                return 100*(1-(daily_hospicash_provision/INP_HOSPITAL_COST_RURAL))
                
        else:
            if daily_hospicash_provision>INP_HOSPITAL_COST_URBAN:
                return 1
            else: 
                return 100*(1-(daily_hospicash_provision/INP_HOSPITAL_COST_URBAN))

def pre_post_cost_status(precare_days, max_postcare_coverage):
    pre_hospitalization_days = lambda precare_days: 0 if precare_days<30 else 0.5 if precare_days==30 else 1   
    def post_hosp_costs():
        if type(max_postcare_coverage) is int: 
            if max_postcare_coverage>=100:
                return 1
            elif max_postcare_coverage>=60:
                return 0.75
            elif max_postcare_coverage>=30:
                return 0.5
            else:
                return 0
        else: 
            if family[0].area_zone!=1 and family[0].area!=2:
                if max_postcare_coverage>=AVG_MPCE_MED_WB_RURAL:
                    return 1
                else:  
                    return (max_postcare_coverage/AVG_MPCE_MED_WB_RURAL)
            else:
                if max_postcare_coverage>=AVG_MPCE_MED_WB_URBAN:
                    return 1
                else: 
                    return (max_postcare_coverage/AVG_MPCE_MED_WB_URBAN)
    
    return 0.5*pre_hospitalization_days(precare_days)+0.5*post_hosp_costs()

def wait_period(waiting_per):
    flag=0
    for person in family:
        if person.pre_exist:
            flag=1
            break
    if flag==1 and waiting_per>=24:
        return 0
    elif flag==0 and waiting_per>=24:
        return 0.5
    else:
        return 1

def final_scoring(copy_params, weightage):
    print(copy_params)
    sum=0.0
    counter=0
    for i in weightage.keys(): 
        sum+=copy_params[counter]*weightage[i]
        print(sum)
        counter+=1
    return sum

def usual_policy():
    policy=Policy()
    weightage={'premium_cost':0, 'lowest_base_sum_insured':0, 'max_family_members_insured':0, 
        'presence_of_opd_coverage':0, 'wait_period':0, 'auto_restoration':0, 'hospital_coverage':0}
    for i in weightage.keys():
        print(i)
    weightage=weightage_input(weightage)

    def premium_calc_per_member(copy_person):
        load_amt=policy.loading/100*copy_person.premium
        floater_disc_amt=policy.floater_disc/100*copy_person.premium
        deductible_disc=(policy.deductible_discount/100)*copy_person.premium
        additional_fam_disc=(policy.family_disc/100)*copy_person.premium
        if copy_person.gen.lower()=="female" and policy.disc_gen!=0.0:
            gen_disc_amt=policy.disc_gen/100.0*copy_person.premium
        else:
            gen_disc_amt=0.0
        if copy_person.age>=policy.inner_lim_age and policy.disc_age!=0.0:
            age_disc=policy.disc_age/100.0*copy_person.premium
        else:
            age_disc=0.0
        if copy_person.relation!="self" and copy_person.relation!='parent':
            relation_disc_amt=(policy.disc_relation_spouse+policy.disc_relation_child)/100.0*copy_person.premium
        else:
            relation_disc_amt=0.0
        return copy_person.premium+load_amt-(floater_disc_amt+gen_disc_amt+relation_disc_amt+deductible_disc+additional_fam_disc)

    for person in family: 
        policy.net_prem+=premium_calc_per_member(person)
    
    #lambda functions:
    score_auto_resto = lambda x:1 if x else 0
    score_hosp_cov = lambda x: (x/TOTAL_HCS_WB) if x<TOTAL_HCS_WB else 1
    family_coverage = lambda x:1 if x>=len(family) else 0
    
    scores=[prem_ratio(policy.net_prem), lowest_sum(policy.lowest_sum), family_coverage(policy.family_mem_cov), 
            opd_coverage(policy.opd_coverage), wait_period(policy.waiting_per), score_auto_resto(policy.auto_resto), score_hosp_cov(policy.hosp_net)]
    policy.net_score=final_scoring(scores, weightage)
  
    return policy.net_score
        
def personal_accident():
    policy=Pers_Accident()
    weightage={'premium_cost':0, 'lowest base sum insured':0, 'maximum sum insured (no. of times of monthly income)':0, 
        'provision for fracture':0, 'daily hospital cash provided':0, 'opd coverage':0, 'additional child and elder care benefits':0}
    print("Here are the parameters to be considered.")
    for i in weightage.keys():
        print(i)
    weightage=weightage_input(weightage)
    
    base=float(input("Enter base sum insured for accident for calculation of premium:"))
    for person in family: 
        person.base_sum_pers_accident=base
    
    def premium_calculation(copy_person):
        net_prem=((policy.prem_rate_ad+policy.prem_rate_ppd+policy.prem_rate_ptd+policy.prem_rate_ttd+policy.prem_rate_additional)/1000)*copy_person.base_sum_pers_accident
        gross_prem=policy.loading*net_prem
        return gross_prem
    
    for person in family:
        policy.total_premium+=premium_calculation(person)
    
    #lambda functions:
    additional_benefits = lambda x, y: 1 if x and y else 0.5 if (x and not y) or (not x and y) else 0
    fracture_prov = lambda x: 1 if x else 0
    highest_sum = lambda x: (x/(PCI_WB/12)) if x>PCI_WB else 0
    highest_sum_scoring = lambda x: 0 if highest_sum(x)==0 else 0.33 if highest_sum(x)<144 else 0.67 if highest_sum(x)==144 else 1   

    scores=[prem_ratio(policy.total_premium), lowest_sum(policy.min_sum), highest_sum_scoring(policy.max_sum), fracture_prov(policy.fracture), 
        hospicash(policy.daily_hospicash_provision), opd_coverage(policy.max_opd_coverage), additional_benefits(policy.child_edu, policy.elderly)]
    policy.net_score=final_scoring(scores, weightage)
    return policy.net_score

def senior_citizen_special():
    policy=Senior_Citizen()
    weightage={'premium_cost':0, 'lowest base sum insured for family':0, 'outer limit of the age insured':0, 
        'provision for multiple check-ups':0, 
        'provision of compulsory copayment/deductible':0, 'waiting period':0, 
        'coverage of pre and post-hospitalization costs (including ambulance/conveyance care)':0}
    print("Here are the parameters to be considered.")
    for i in weightage.keys():
        print(i)
    weightage=weightage_input(weightage)
    
    def premium_calculation(copy_person):
        if copy_person.plan_fam_cat=='FL':
            if copy_person.relation!='self':
                net_prem=copy_person.premium+(policy.loading/100*copy_person.premium)-(policy.floater_disc/100*copy_person.premium)-(policy.copayment_discount/100*copy_person.premium)
            else:
                net_prem=copy_person.premium+(policy.loading/100*copy_person.premium)-(policy.copayment_discount/100*copy_person.premium) 
        else: 
            net_prem=copy_person.premium+(policy.loading/100*copy_person.premium)-(policy.copayment_discount/100*copy_person.premium)
        print(net_prem)          
        return net_prem
    
    for person in family:
        policy.total_premium+=premium_calculation(person)
    print(policy.total_premium)
    
    #lambda functions:
    copayment_status = lambda x: 0 if x>=50.0 else 0.33 if x>=30.0 else 0.67 if x>=10.0 else 1
    checkup_present = lambda x:1 if x else 0
    outer_age_limit_atentry = lambda x:0 if x<60 else 0.5 if x<70 else 1
    
    scores=[prem_ratio(policy.total_premium), lowest_sum(policy.min_sum), outer_age_limit_atentry(policy.max_age), 
            checkup_present(policy.checkup), copayment_status(policy.min_copayment), 
            wait_period(policy.waiting_per), pre_post_cost_status(policy.precare_days, policy.max_postcare_coverage)]
    policy.net_score=final_scoring(scores, weightage)
    return policy.net_score

def critical_care():
    policy=Criti_Care()
    weightage={'premium_cost':0, 'lowest base sum insured':0, 'maximum sum insured':0, 
        'no. of ailments+procedures covered':0, 
        'provision for copayment/deductible (yes if either is compulsory for all claims)':0, 'waiting period for pre-existing diseases':0, 
        'coverage of pre and post-hospitalization costs (including ambulance care)':0}
    print("Here are the parameters to be considered.")
    for i in weightage.keys():
        print(i)
    
    weightage=weightage_input(weightage)
    
    def premium_calculation(copy_person):
        if copy_person.plan_fam_cat=='FL':
            if copy_person.relation!='self':
                net_prem=policy.sum_insured*(policy.rate_permille/1000.0)
                net_prem=net_prem+(policy.loading/100*net_prem)-(policy.copayment_discount/100*net_prem)-(policy.floater_disc/100*net_prem)-(policy.voluntary_ded_disc/100*net_prem)
            else: 
               net_prem=policy.sum_insured*(policy.rate_permille/1000.0)
               net_prem=net_prem+(policy.loading/100*net_prem)-(policy.copayment_discount/100*net_prem)-(policy.voluntary_ded_disc/100*net_prem) 
        else:
            net_prem=policy.sum_insured*(policy.rate_permille/1000.0)
            net_prem=net_prem+(policy.loading/100*net_prem)-(policy.copayment_discount/100*net_prem)-(policy.voluntary_ded_disc/100*net_prem)
      
        return net_prem
    
    for person in family: 
        policy.total_premium+=premium_calculation(person)
    
    #lambda functions:
    criti_max_sum = lambda x: 1 if x>=3000000 else 0.75 if x>=1500000 else 0.50 if x>=700000 else 0.25 if x>=100000 else 0
    criti_disease_cov = lambda x:1 if x>=40 else 0.75 if x>=35 else 0.50 if x>=25 else 0.25 if x>=10 else 0
    copayment_status = lambda x: 0 if x>=50.0 else 0.33 if x>=30.0 else 0.67 if x>=10.0 else 1

    scores=[prem_ratio(policy.total_premium), lowest_sum(policy.min_sum), criti_max_sum(policy.max_sum), 
            criti_disease_cov(policy.disease_cov), copayment_status(policy.min_copayment), wait_period(policy.waiting_per), 
            pre_post_cost_status(policy.precare_days, policy.max_postcare_coverage)]
    policy.net_score=final_scoring(scores, weightage)
    return policy.net_score

def top_up_plan():
    policy=Top_Up()
    weightage={'premium_cost':0, 'minimum deductible offered':0, 'waiting period for pre-existing/mentioned illnesses':0, 
        'hospital coverage':0, 'pre and post hospitalization coverage (including medicinal costs)':0, 'opd (including ambulance and medicinal) coverage':0, 
        'maximum no. of family members who can be covered':0}
    print("Here are the parameters to be considered.")
    for i in weightage.keys():
        print(i)
    weightage=weightage_input(weightage)
    
    def premium_calculation(copy_person):
        if copy_person.plan_fam_cat=='FL':
            if copy_person.relation!='self':
                net_prem=copy_person.premium+(policy.load_prem/100*copy_person.premium)-(policy.voluntary_ded_disc/100*copy_person.premium)-(policy.floater_disc/100*copy_person.premium)-(
            policy.copayment_discount/100*copy_person.premium)
            else: 
                net_prem=copy_person.premium+(policy.load_prem/100*copy_person.premium)-(policy.voluntary_ded_disc/100*copy_person.premium)-(policy.copayment_discount/100*copy_person.premium)
        else: 
            net_prem=copy_person.premium+(policy.load_prem/100*copy_person.premium)-(policy.voluntary_ded_disc/100*copy_person.premium)-(policy.copayment_discount/100*copy_person.premium)    
        return net_prem
    
    for person in family:
        policy.total_premium+=premium_calculation(person)
    
    #lambda functions: 
    deductible_status = lambda x: 1 if x<=100000 else 0.67 if x<=300000 else 0.33 if x<=700000 else 0
    score_hosp_cov = lambda x: (x/TOTAL_HCS_WB) if x<TOTAL_HCS_WB else 1
    family_coverage = lambda x:1 if x>=len(family) else 0
        
    scores=[prem_ratio(policy.total_premium), deductible_status(policy.min_deductible), wait_period(policy.waiting_per), score_hosp_cov(policy.hosp_net), 
            pre_post_cost_status(policy.precare_days, policy.max_postcare_coverage), opd_coverage(policy.max_opd_cost), family_coverage(policy.family_mem_cov)]
    policy.net_score=final_scoring(scores, weightage)
    return policy.net_score 
        
def policy_type(output_file) -> None:
    global type_plan
    name=input("Enter name of insurance policy:") 
    type_plan=int(input("Choose 1 for general indemnity-based plans, 2 for personal accident policy, 3 for senior citizen policy, 4 for critical care insurance and 5 for top-up plan:"))
    for i in family:
        i.plan_type=type_plan
    match type_plan:
        case 1:
            score=usual_policy()*100
        case 2:
            score=personal_accident()*100
        case 3: 
            score=senior_citizen_special()*100
        case 4:
            score=critical_care()*100
        case 5: 
            score=top_up_plan()*100
        case _:
            print("Wrong input. Please specify within the items mentioned.")
    print(f'finalscore for {name}={score}')
    grade:str = lambda x: 'A+' if x>=90 else 'A' if x>=80 else 'B' if x>=70 else 'C' if x>=60 else 'D' if x>=50 else 'E' if x>=40 else 'F'
    comment=input("Enter any additional comment to be considered for the policy in question. Enter NA if no comment:")
    file_path=output_file
    fieldnames=['name_of_policy', 'category', 'score', 'additional_comment', 'letter_grade']
    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            writer=csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'name_of_policy':name, 'category':type_plan, 'score':score, 'additional_comment':comment, 'letter_grade':grade(score)})
            print(f'{file_path} has been appended!')
            file.close()
    else:
        with open(file_path, 'w') as file:
            writer=csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'name_of_policy':name, 'category':type_plan, 'score':score, 'additional_comment':comment, 'letter_grade':grade(score)})
            print(f'{file_path} has been appended!')
            file.close()
        
def each_member_input():
    for i in range(len(family)): #modify the iteration to ensure that the input prompts are not repeated for the future members of the family
        print(f"Prompt to enter details for {i+1}th member:")
        family[i].age=int(input("Enter age="))
        family[i].gen=input("Enter gender (male, female, other)=")
        temp_location=input("Enter your town/city=")
        if temp_location in X_CITIES:
            family[i].area_zone=1
        elif temp_location in Y_CITIES:
            family[i].area_zone=2
        else:
            family[i].area_zone=3
        family[i].premium=float(input("Enter the base amount of premium for the given plan for your age, gender and residence (write 0 if not known/NA)="))
        #family[i].disc_gen=float(input("Enter discount% based on gender, if there are any="))
        #family[i].disc_age=float(input("Enter discount% based on age, if there are any="))
        pre_exist_temp=input("Enter if you have pre-existing diseases - answer in Yes/No:")
        if pre_exist_temp.lower()=='yes':
            family[i].pre_exist=True
        family[i].relation=str(input("Enter the relation of the person being insured (self, spouse, parent or child)=")).lower()
        if i==0:
            family[i].plan_fam_cat=input("Enter the family category you are entering - individual, family individual or floater (write as I, FI or FL):")
        else: 
            family[i].plan_fam_cat=family[0].plan_fam_cat

def check_policy(output_file):
    if os.path.exists(output_file):
        df=pd.read_csv(output_file)
        mod_df=df[(df['letter_grade']=='A+' or df['letter_grade']=='A')]
        if mod_df.empty:
            print("Keep checking more policies that are suited to your needs!")
        else:
            print(mod_df)
    else:
        print("No policies have been added yet, please create the file!")

def main(output_file):
    query1:str=input("Do you want to check existing policies, or add a new policy? Answer in T/F (true to add policy, false to check policy):").strip().lower()
    query1:bool=query1=='t' or query1=='true'
    if query1:
        members_input()
        each_member_input()
        policy_type(output_file)
    else:
        check_policy(output_file)

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python_script.py <output_file>")
        sys.exit(1)
        
    output_file=sys.argv[1]
    main(output_file) # type: ignore    
