import scipy.stats as stats

class Reduction():
    
    def __init__(self, mean, std_dev, target_survival_probability):
        self.mean = mean
        self.std_dev = std_dev
        self.target_survival_probability = target_survival_probability
        
    def calculate(self):
        # Calculate the Z-score corresponding to the target survival probability
        target_z_score = stats.norm.ppf(1 - self.target_survival_probability)
        
        # Calculate the new threshold value based on the target Z-score
        new_threshold = self.mean + target_z_score * self.std_dev * self.mean
        
        # Calculate the reduction factor
        reduction_factor = new_threshold / self.mean
        
        return reduction_factor
