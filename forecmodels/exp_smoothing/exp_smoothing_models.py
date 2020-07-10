import numpy as np


class HoltWinters:
    
    def __init__(self, data, alpha = 0.5, beta = 0.5, h = 1, seasonal = 0, gamma = 0.5):
        self.data = data
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.h = h
        self.seasonal = seasonal
    
    
    #model fitting
    def fit(self):
        
        
        #Finding trend
        def trend_finding(data, season):
            result = np.mean([data[i + season] - data[i]
                              for i in range(season)])
            return result
        
        
        # Finding seasonal components
        def set_seasons(series, seasonal_lenn):
            seasonals = {}
            season_averages = []
            n_seasons = int(len(series)/seasonal_lenn)
            # вычисляем сезонные средние
            for j in range(n_seasons):
                season_averages.append(sum(series[seasonal_lenn * j:seasonal_lenn * j +
                                                  seasonal_lenn]) / float(seasonal_lenn))
            # вычисляем начальные значения
            for i in range(seasonal_lenn):
                sum_of_vals_over_avg = 0.0
                for j in range(n_seasons):
                    sum_of_vals_over_avg += series[seasonal_lenn * j + i] - season_averages[j]
                seasonals[i] = sum_of_vals_over_avg / n_seasons
            return seasonals
        
        
        smooth = []
        trend = []
        season = []
        self.data_mass = []
        
        for i in range(len(self.data)):
            if i == 0:
                smooth.append(self.data[0])
                if self.seasonal != 0:  # if we want to find the trend...
                    seasonals = set_seasons(self.data, self.seasonal)
                    trend.append(trend_finding(self.data, self.seasonal))
                    season.append(seasonals[i%self.seasonal])
                else:
                    seasonals = [0]*100
                    trend.append(0)
                    self.seasonal = 1
                continue
            
            elif i > 0:
                self.data_mass.append(smooth[-1] + self.h*trend[-1])
                smooth.append(self.alpha*(self.data[i] - seasonals[i%self.seasonal]) +
                              (1 - self.alpha)*(smooth[-1] + trend[-1]))
                trend.append(self.beta*(smooth[-1] - smooth[-2]) + (1 - self.beta)*trend[-1])
                seasonals[i%self.seasonal] = self.gamma*(self.data[i]-smooth[-2] - trend[-2]) + (1-self.gamma)*seasonals[i%self.seasonal]
        
            self.smooth = smooth
            self.trend = trend

    # model prediction
    def predict(self, lenn = 0):
        if lenn == 0:
            lenn = len(self.data)
            
        self.lenn = lenn
        return self.data_mass[:lenn]

    # Forecastiong new values
    def forecast(self, lenn):
        forecasting_arr = [self.data[-1]]
        for i in range(lenn):
            forecasting_arr.append(self.smooth[-1] + self.h*self.trend[-1])
            self.smooth.append(self.alpha*forecasting_arr[-2] +
                               (1 - self.alpha)*(self.smooth[-1] + self.trend[-1]))
            self.trend.append(self.beta*(self.smooth[-1] - self.smooth[-2]) +
                              (1 - self.beta)*self.trend[-1])
        return forecasting_arr[1:]
        
    # some statistics
    def stats(self):
        RSS = np.sum((self.data_mass-self.data[:self.lenn-1])**2)
        MSE = np.mean((self.data_mass-self.data[:self.lenn-1])**2)
            
        return({"RSS": RSS, "MSE": MSE})
