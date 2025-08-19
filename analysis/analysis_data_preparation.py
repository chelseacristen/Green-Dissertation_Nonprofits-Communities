#AMONG ORGANIZATIONS THAT REGISTER ANY LEVEL OF ASSETS AND INCOME, WHAT EXPLAINS VARIATION ?
yvariable = 'nonzero_assets_adj' #define yvariable
dataset = 'ngos_sheldus' #define dataset
weather='none' #define weather subset
std_errors='cluster'
cluster_category='COGEOID'
directory='your_directory'

import pandas as pd
import os
import researchpy as rp
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
import numpy as np
from statsmodels.tools.tools import add_constant
import re
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Lasso

categorical = ['ntee_complete', 'foundation', 'filing', 'tax_year']
disaster_vars = ['Injuries', 'Fatalities', 'CropDmg_adj2022','Wind','Wind_Records', 'Severe_Storm', 
                 'Severe_Storm_Records','Hurricane', 'Hurricane_Records','Drought','Drought_Records',
 'Wildfire','Wildfire_Records','Flooding', 'Flooding_Records','Heat','Heat_Records','Earthquake',
 'Earthquake_Records','CropIndemnityPayment_adj2022', 'top_1','top_10','top_25']
race_vars = ['white','black','native_1','asian','native_2','other_race','two_races',
 'hispanic']
redlining_vars=['HRS2010']
wealth_vars = ['unemployment','poverty_rate', 'median_inc_ln', 'mean_inc_ln', 'community_inequality']
controls = ['ngo_age']

ngos_sheldus = pd.read_csv(directory+dataset+'.csv')

#Creating new median and mean inc ln variables WITHOUT plus one.
ngos_sheldus = ngos_sheldus.loc[ngos_sheldus['median_inc_adj']>=0]
ngos_sheldus = ngos_sheldus.loc[ngos_sheldus['mean_inc_adj']>=0]
ngos_sheldus['community_inequality']=ngos_sheldus['mean_inc_adj']/ngos_sheldus['median_inc_adj']

ngos_sheldus['median_inc_ln'] = np.log(ngos_sheldus['median_inc_adj'])
ngos_sheldus['mean_inc_ln'] = np.log(ngos_sheldus['mean_inc_adj'])

#only looking at 501 c(3)s
ngos_sheldus= ngos_sheldus.loc[ngos_sheldus['subsection']==3]
ngos_sheldus= ngos_sheldus.drop(['subsection'], axis=1)

if bool(re.search('county', dataset))==True:
    ngos_sheldus = ngos_sheldus.loc[(ngos_sheldus['Addr_type']!='SubAdmin') & (ngos_sheldus['Addr_type']!='Locality') & 
                                    (ngos_sheldus['Addr_type']!='Postal') & (ngos_sheldus['Addr_type']!='StreetName')]
    #ngos_sheldus = ngos_sheldus.loc[(ngos_sheldus['Addr_type']!='SubAdmin') & (ngos_sheldus['Addr_type']!='Locality')]
else:
    ngos_sheldus = ngos_sheldus.loc[(ngos_sheldus['Addr_type']!='SubAdmin') & (ngos_sheldus['Addr_type']!='Locality') & 
                                    (ngos_sheldus['Addr_type']!='Postal') & (ngos_sheldus['Addr_type']!='StreetName')]
    
ngos_sheldus['income_adj_ln']= np.log(ngos_sheldus['income_adj'])
ngos_sheldus['assets_adj_ln']= np.log(ngos_sheldus['assets_adj'])

ngos_sheldus = ngos_sheldus.loc[ngos_sheldus['pf_filing']!=3]

ngos_sheldus['native_area'] = np.where(pd.isnull(ngos_sheldus['NTGEOID']), 0, 1)
ngos_sheldus = ngos_sheldus.drop(['acct_pd', 'tax_month', 'tax_pd', 'original_file', 'rule_y', 'rule_m', 'name', 
                                  'CBSA', 'INTERVAL2010', 'tax_pd_x', 'tax_pd_y', 'Unnamed: 0.2', 'Unnamed: 0.3',
                                   'InjuriesPerCapita', 'FatalitiesPerCapita', 'CropDmgPerCapita_adj2022', 
                                  'PropertyDmgPerCapita_adj2022', 'CropIndemnityPaymentPerCapita_adj2022', 'Unnamed: 0',
                                 'acs_year','avg_2022', 'CropDmg_adj2022_ln', 'bachelors', 'NTGEOID', 'filed_next',
                                 'Match_addr', 'X', 'Y', 'street', 'city', 'state', 'zip', 'geometry', 'mean_inc', 
                                  'Year', 'sort_name', 'assets', 'income', 'filed_prev', 'Unnamed: 0.1', 'renter_occupied', 'female', 
                                  'housing_density', 'CropDmg_adj2022_ln','tot_filings'], 
                                 axis=1, errors='ignore')
ngos_sheldus['ntee1']= np.where(ngos_sheldus['ntee1'].isnull(), 'Z', ngos_sheldus['ntee1'])
ngos_sheldus['foundation']= np.where(ngos_sheldus['foundation'].isnull(), 'NA', ngos_sheldus['foundation'])
ngos_sheldus = ngos_sheldus[ngos_sheldus['tax_year']!=2020]

ngos_sheldus['top_1'] = np.where(ngos_sheldus['PropertyDmg_adj2022']>=ngos_sheldus.PropertyDmg_adj2022.quantile(.99), 1, 0)
ngos_sheldus['top_10'] = np.where(ngos_sheldus['PropertyDmg_adj2022']>=ngos_sheldus.PropertyDmg_adj2022.quantile(.9), 1, 0)
ngos_sheldus['top_25'] = np.where(ngos_sheldus['PropertyDmg_adj2022']>=ngos_sheldus.PropertyDmg_adj2022.quantile(.75), 1, 0)
ngos_sheldus = ngos_sheldus.drop(['PropertyDmg_adj2022', 'PropertyDmg_adj2022_ln'], axis=1)
ngos_sheldus = ngos_sheldus.drop(['Score'], axis=1)

if weather!="none":
    ngos_sheldus = ngos_sheldus.loc[ngos_sheldus[weather]>0]
    #ngos_sheldus[weather+'_ln'] = np.log((ngos_sheldus[weather]))
    #ngos_sheldus = ngos_sheldus.drop([weather], axis=1)

if (yvariable=='income_adj_ln') | (yvariable=='assets_adj_ln'):
    ngos_sheldus = ngos_sheldus.loc[(ngos_sheldus['assets_adj']!=0) & (ngos_sheldus['income_adj']!=0)]
    ngos_sheldus = ngos_sheldus.drop(['income_adj', 'assets_adj'], axis=1)
    
if yvariable=='nonzero_assets_adj':
    #Create nonzero assets and nonzero income variable:
    new=[]
    for row in ngos_sheldus['assets_adj']:
        if np.isnan(row):
            new.append(np.nan)
        elif row==0:
            new.append(0)
        else:
            new.append(1)
    ngos_sheldus['nonzero_'+'assets_adj']=new
    ngos_sheldus = ngos_sheldus.drop(['income_adj', 'assets_adj'], axis=1)

####MERGING IN GOVERNMENT GRANT CONTRIBUTIONS DATA:
#create a redlined and ngos_sheldus version with grants data included:
gov = pd.read_csv(os.path.join(directory, 'gov_grants_combined.csv'))
ngos_gov = ngos_sheldus.merge(gov, on=['ein', 'tax_year'], how='inner')
ngos_gov = ngos_gov.drop(['Unnamed: 0'], axis=1)
#which organizations are getting the most government grants?
#ngos_gov[['ein', 'tax_year', 'gov_grants']].groupby('gov_grants')['gov_grants'].sort_values(ascending=True)

#ngos_sheldus['gov_grants_ln']= np.log(ngos_sheldus['gov_grants'])
ngos_gov.to_csv(os.path.join(directory, dataset+'_gov.csv'))

#Merge in more detailed activity codes.
ntee = pd.read_csv(os.path.join(directory, 'ntee_complete.csv'))
ngos_sheldus.ein = ngos_sheldus.ein.astype(int)
ntee.ein = ntee.ein.astype(int)
ngos_sheldus.tax_year = ngos_sheldus.tax_year.astype(int)
ntee.tax_year = ntee.tax_year.astype(int)

ngos_sheldus = ngos_sheldus.merge(ntee[['tax_year', 'ein', 'ntee_complete']], on=['ein', 'tax_year'], how='left')
del(ntee)

#Make dummy variables for some of the categorical NGO-related variables. 
dummies = pd.get_dummies(ngos_sheldus[categorical], columns=categorical, dtype=int)
variables = []
for d in dummies.columns:
    if(re.match('.*\.0$', d)):
        variables.append(re.findall('[a-z]+_[0-9]{1,2}', d)[0])
    else:
        variables.append(d)

dummies.columns = variables
variables.extend(['pf_filing','ngo_age'])
controls = controls+ variables
ngos_sheldus = pd.concat([ngos_sheldus, dummies],axis=1)
del(dummies)

#get a list of the names of the activity codes dummy variables
ntee_vars =[]
for col in variables:
    if re.match('ntee.*', col):
        ntee_vars.append(re.match('ntee.*', col)[0])

#create a correlation matrix without the activity column dummies in it:
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="white")

d = ngos_sheldus[['income_adj_ln', 'assets_adj_ln', 'nonzero_assets_adj', 'gov_grants', 'ngo_age', 
                  'top_25', 'median_inc_ln',
                  'mean_inc_ln', 'poverty_rate', 'HRS2010', 'white', 'black']]
# Compute the correlation matrix
corr = d.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

#EXPLAINING ASSETS_ADJ_LN:
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.max_rows', 1000)
yvariable = 'assets_adj_ln'
interaction= 'yes'
ngos_sheldus = ngos_sheldus.dropna() 

l1= []
y = ngos_sheldus[[yvariable]]
    
#CONTROLS MODEL: NGO FACTORS ONLY MODEL
X=ngos_sheldus[controls]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

pipeline = Pipeline([
                         ('scaler',StandardScaler()),
                         ('model',Lasso(max_iter = 100000))
    ])

search = GridSearchCV(pipeline,
                          {'model__alpha':np.linspace(.1,.2, 5)},
                          cv = 2, scoring="r2",verbose=3
                          )
search.fit(X_train,y_train.values.ravel())
coefficients = search.best_estimator_.named_steps['model'].coef_
importance = np.abs(coefficients)
print(search.best_params_)

controls2 = pd.concat([pd.DataFrame(list(X.columns)), pd.DataFrame(list(importance))], axis=1)
controls2.columns = ['feature', 'coefficient']
controls2 = controls2.loc[controls2['coefficient']>0]
X = X[controls2.feature.unique()]  
data = pd.concat([X, y], axis=1)
model = yvariable+'~'+'+'.join(X.columns)
if std_errors=='robust':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    data = pd.concat([X, y, geo], axis=1)
    result = smf.ols(model, data).fit(cov_type='cluster', cov_kwds={'groups': data[cluster_category]}) 
if std_errors=='hac':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type="hac", cov_kwds={'maxlags':3})
l1.append([yvariable, 'Controls:', result.rsquared, result.aic, result.bic, int(result.nobs)])
del(X)

#IVS: NATURAL DISASTERS ONLY MODEL
X=ngos_sheldus[disaster_vars]   
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

pipeline = Pipeline([
                         ('scaler',StandardScaler()),
                         ('model',Lasso(max_iter = 100000))
    ])

search = GridSearchCV(pipeline,
                          {'model__alpha':np.linspace(.01,.1, 5)},
                          cv = 2, scoring="r2",verbose=3
                          )
search.fit(X_train,y_train.values.ravel())
coefficients = search.best_estimator_.named_steps['model'].coef_
importance = np.abs(coefficients)
print(search.best_params_)

natural = pd.concat([pd.DataFrame(list(X.columns)), pd.DataFrame(list(importance))], axis=1)
natural.columns = ['feature', 'coefficient']
natural = natural.loc[natural['coefficient']>0]
X = X[natural.feature.unique()]  
data = pd.concat([X, y], axis=1)
model = yvariable+'~'+'+'.join(X.columns)
if std_errors=='robust':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    data = pd.concat([X, y, geo], axis=1)
    result = smf.ols(model, data).fit(cov_type='cluster', cov_kwds={'groups': data[cluster_category]}) 
if std_errors=='hac':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type="hac", cov_kwds={'maxlags':3})
l1.append([yvariable, 'IVs: Natural Disasters', result.rsquared, result.aic, result.bic, int(result.nobs)])
del(X)

#IVS: RACIAL DEMOGRAPHICS ONLY MODEL
X=ngos_sheldus[race_vars]
if interaction=='yes':
    #adding the race*activity code interaction variables in: 
    counter=1
    for d in ntee_vars:
        if counter!=1:
            df1 = pd.DataFrame(ngos_sheldus[d]*ngos_sheldus['white'])
            df1.columns = [d+'_'+'white']
            df = pd.concat([df, df1], axis=1)
            print(d)
        else:
            df = pd.DataFrame(ngos_sheldus[d]*ngos_sheldus['white'])
            df.columns = [d+'_'+'white']
            print(d)
            counter=counter+1
    X = pd.concat([X, df], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    pipeline = Pipeline([
                         ('scaler',StandardScaler()),
                         ('model',Lasso(max_iter = 100000))
    ])

    search = GridSearchCV(pipeline,
                          {'model__alpha':np.linspace(.01,.1, 5)},
                          cv = 2, scoring="r2",verbose=3
                          )
    search.fit(X_train,y_train.values.ravel())
    coefficients = search.best_estimator_.named_steps['model'].coef_
    importance = np.abs(coefficients)
    print(search.best_params_)

    race = pd.concat([pd.DataFrame(list(X.columns)), pd.DataFrame(list(importance))], axis=1)
    race.columns = ['feature', 'coefficient']
    race = race.loc[race['coefficient']>0]
    X = X[race.feature.unique()] 
        
data = pd.concat([X, y], axis=1)
model = yvariable+'~'+'+'.join(X.columns)
if std_errors=='robust':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    data = pd.concat([X, y, geo], axis=1)
    result = smf.ols(model, data).fit(cov_type='cluster', cov_kwds={'groups': data[cluster_category]}) 
if std_errors=='hac':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type="hac", cov_kwds={'maxlags':3})
l1.append([yvariable, 'IVs: Racial Demographics', result.rsquared, result.aic, result.bic, int(result.nobs)])
del(X)

#IVS: COMMUNITY WEALTH VARIABLES ONLY MODEL
X=ngos_sheldus[wealth_vars]   
data = pd.concat([X, y], axis=1)
model = yvariable+'~'+'+'.join(X.columns)
if std_errors=='robust':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    data = pd.concat([X, y, geo], axis=1)
    result = smf.ols(model, data).fit(cov_type='cluster', cov_kwds={'groups': data[cluster_category]}) 
if std_errors=='hac':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type="hac", cov_kwds={'maxlags':3})
l1.append([yvariable, 'IVs: Community Wealth', result.rsquared, result.aic, result.bic, int(result.nobs)])
del(X)

#IVS: REDLINING ONLY MODEL
X=ngos_sheldus[redlining_vars]   
data = pd.concat([X, y], axis=1)
model = yvariable+'~'+'+'.join(X.columns)
if std_errors=='robust':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    data = pd.concat([X, y, geo], axis=1)
    result = smf.ols(model, data).fit(cov_type='cluster', cov_kwds={'groups': data[cluster_category]}) 
if std_errors=='hac':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type="hac", cov_kwds={'maxlags':3})
l1.append([yvariable, 'IVs: Redlining', result.rsquared, result.aic, result.bic, int(result.nobs)])
del(X)

#IVS + CONTROLS MODEL
X=ngos_sheldus[list(controls2.feature.unique())+list(natural.feature.unique())+ list(race.feature.unique())+ 
               wealth_vars] 
if dataset =='redlined_sheldus':
    X=ngos_sheldus[controls+variables+list(natural.feature.unique())+ race_vars+ wealth_vars+redlining_vars] 
data = pd.concat([X, y], axis=1)
model = yvariable+'~'+'+'.join(X.columns)

if std_errors=='robust':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    data = pd.concat([X, y, geo], axis=1)
    result = smf.ols(model, data).fit(cov_type='cluster', cov_kwds={'groups': data[cluster_category]}) 
if std_errors=='hac':
    data = pd.concat([X, y], axis=1)
    result = smf.ols(model, data).fit(cov_type="hac", cov_kwds={'maxlags':3})
l1.append([yvariable, 'All IVs + Controls', result.rsquared, result.aic, result.bic, int(result.nobs)])

l1 = pd.DataFrame(l1)
l1.columns = ['DV', 'X', 'R2', 'AIC', 'BIC', 'N Obs']
#print(l1.T.to_latex(index=False))   
#l1 = pd.concat([l1,l2])
del(yvariable)
del(X)

#EXPLAINING NONZERO_ASSETS:

ngos_sheldus = ngos_sheldus.dropna() 

l1= []
y = ngos_sheldus[['nonzero_assets_adj']]
    
#CONTROLS MODEL: NGO FACTORS ONLY MODEL
X=ngos_sheldus[controls]

ss = StandardScaler()
X_scaled = pd.DataFrame(ss.fit_transform(X),columns = X.columns)
X_scaled['intercept'] = 1
y.index = X_scaled.index
print('regression ready')
if std_errors=='robust':
    logit_model = sm.Logit(y,X_scaled).fit_regularized(method='l1', maxiter=500, alpha=.2, cov_type='hc1')
if std_errors=='cluster':
    geo = ngos_sheldus[[cluster_category]]
    logit_model = sm.Logit(y,X_scaled).fit_regularized(method='l1', maxiter=500, alpha=.2, cov_type='cluster', 
                                                     cov_kwds={'groups': geo})
summary = logit_model.summary()
summary
