import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

class SARIMA_estim():
    
    def __init__(self, X,
                 order = (1,1,1), 
                 seasonal_order = (0, 0, 0, 0)):
        
        self.seasonal_order = seasonal_order
        self.order = order
        self.X = X
        #self.seasonal_order = seasonal_order
        
    def concating(Y, l, S = 1, PQ = 0):

        result = []
        if S > 1:
            Y = np.concatenate((np.zeros(1000), Y))
            neww = np.concatenate((np.zeros(1000), Y))
            result = np.hstack([np.array(Y[l-k:-k]).reshape(-1,1) for k in range(1,l+1)])[1000-l:]
            #print(len(result))
            for pq in range(1, PQ+1):
                result = np.column_stack((result, np.array(neww[1000 - S*pq+l:-S*pq]).reshape(-1,1)[1000-l:]))

        else:
            Y = np.concatenate((np.zeros(1000), Y))
            result = np.hstack([np.array(Y[l-k:-k]).reshape(-1,1) for k in range(1, l+1)])[1000 - l:]

        return result
        

    def fit(self):

        def reverse_difference(data, default_mass, d):
        
            for j in range(d):
                data = np.append(np.diff(default_mass,d-j-1)[0], data)
                for i in range(1, len(np.diff(default_mass,d-j-1))):
                    data[i]+=np.diff(default_mass,d-j-1)[i-1]

            return data
        
        
        if self.seasonal_order != (): # Добавлять в матрицу сдвиги! на длину S*P
            P = self.seasonal_order[0]
            D = self.seasonal_order[1] # вычитаю из текущего то что было S значений назад.
            Q = self.seasonal_order[2]
            S = self.seasonal_order[3]
        
    
        
        p = self.order[0]
        d = self.order[1]
        q = self.order[2]     
        p+=d
    
        # ............
        # Надо доделать сезонное дифференцирование D
        # ............
        
        tss = TimeSeriesSplit(n_splits=5)
        
        Data = np.diff(self.X, d)
        #Data = self.X
        
        if p > 0:
            model = LinearRegression()
            X_01 = SARIMA_estim.concating(Data, p, S, P)
            #print(X_01)
            model.fit(X_01, Data)
            self.AR_params = [*model.coef_]
            self.AR_p = model.intercept_
            AR = model.predict(X_01)
            self.AR = AR
        
        else:
            self.AR = Data
            

        if q > 0:
            model_ma = LinearRegression()
            MA_X = SARIMA_estim.concating(Data-self.AR, q, S, Q)
            model_ma.fit(MA_X, Data-AR)
            self.MA_params = [*model_ma.coef_]
            self.MA_p = model_ma.intercept_
            #mse = -np.mean(cross_val_score(model_ma, MA_X, Data[p+q:], scoring='neg_mean_squared_error', cv=tss)) # Это надо убрать!
            arma = model_ma.predict(MA_X)
        
        else:
            arma = np.zeros(len(AR))
            self.MA_params = []
            self.MA_p = 0
        
        #self.result = np.hstack((AR[:q], arma))
        
        #self.result = AR[q:] + arma
        self.result = reverse_difference(AR + arma, self.X[-len(AR + arma):], d)

            
        #self.result_1 = get_fitted_values(Data, P, D, Q, S)

        return [p, d, q, 1]
    
    
    def predict(self, lenn = None):
        
        if lenn == None:
            lenn = len(self.result)
            
        return self.result[:lenn]
    
    def forecast(self, horizon):
        ress_ar = list(self.X[-(len(self.AR_params) + len(self.MA_params)):]) # Делаем кусок от уже зафиченного ряда
        #vv = self.X - self.AR
        ress_ma = list(self.X[-(len(self.AR_params) + len(self.MA_params)):])
        ress = list(self.X[-(len(self.AR_params) + len(self.MA_params)):])
        for _ in range(horizon):
            # Добавляем параметры авторегрессии
            ress_ar.append(np.sum([ress_ar[-k]*self.AR_params[k-1] for k in range(1,len(self.AR_params)+1)])+self.AR_p)

            # И скользящего среднего как авторегрессии на остатки, тоесть авторегеррсии на то что получилось.
            ress_ma.append(np.sum([ress_ma[-k]*self.MA_params[k-1] for k in range(1,len(self.MA_params)+1)])+self.MA_p)
            
            #ress[-1] += np.sum([ress[-k-1]*self.MA_params[k-1] for k in range(1, len(self.MA_params)+1)])+self.MA_p
            ress.append(ress_ma[-1] + ress_ar[-1])
            
        return ress[len(self.AR_params) + len(self.MA_params):]
