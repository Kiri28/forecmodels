import numpy as np


class WMA:
    
    def __init__(self, data, M):
        self.data = data
        self.M = M
        
    def fit(self):
        WMA_list = []
        for i in range(self.M, len(self.data)):
            WMA_list.append(np.sum(self.data[i - self.M: i] * np.arange(self.M)) /
                            ((self.M - 1) * (self.M)/2))  
        self.WMA_list = WMA_list
        
    def predict(self, lenn = 0):
        if lenn == 0:
            lenn = len(self.data)
            
        self.lenn = lenn
        
        try:
            return self.WMA_list[:lenn]
        except:
            return "<!-- model not fitted yet! !-->"
        
    def forecast(self, lenn):
        
        forecast_list = self.WMA_list[-self.M:]
        try:
            for i in range(lenn):
                forecast_list.append(np.sum(forecast_list[- self.M: ] * np.arange(self.M)) / 
                                ((self.M - 1) * (self.M)/2))  
            
            return forecast_list[self.M:]
        except:
            return "<!-- too low sample! !-->"
    
    # some statistics
    def stats(self):
        RSS = np.sum((self.WMA_list-self.data[self.M: ])**2)
        MSE = np.mean((self.WMA_list-self.data[self.M: ])**2)
        
        return({"RSS": RSS, "MSE": MSE})
