#EXPLAINING OUTCOME VARIABLE:
yvariable = 'nonzero_assets_adj' #define yvariable
dataset = 'ngos_sheldus' #define dataset
weather='none' #define weather subset
std_errors='cluster'
cluster_category='COGEOID'
directory='your_directory'

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
