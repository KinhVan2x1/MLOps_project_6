import pandas as pd 
import yaml
import logging
import os
from typing import List, Dict


# Setting logging directory:
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Setting up logger:
logger = logging.getLogger('options_payoff_cal')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(log_dir, 'options_payoff_cal.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class Option_Payoff:
    def _to_float(self, value, name):
       try:
              return float(value)
       except (TypeError, ValueError):
              raise ValueError(f"{name} must be a numeric value, got {value}")
    
    def __init__(self, X = ["Strike Price", float],
                  ST = ["Underlying asset's price", float],
                  C = ["Call Premium", float],
                  CR = ["Conversion rate", float],
                  NC = ["Number of options", float]):
        self.X = X
        self.ST = ST
        self.C = C
        self.CR = CR
        self.NC = NC
    
    def calculate_payoff(self):
       """Calculate the payoff of the options from existing data"""
       self.pay_off = (max(0, (self.ST - self.X)) - self.C)*self.NC*self.CR
       return self.pay_off
    
    def display_payoff(self, code):
       headers = [
              "Code",
              "X (Strike Price)",
              "ST (Market Price at T)",
              "C (Call Premium)",
              "CR (Conversion Ratio)",
              "NC (No. Call Options)",
              "Payoff"
       ]

       def fmt(x):
       # Format numbers with commas, keep floats clean
          if isinstance(x, (int, float)):
              return f"{x:,.2f}".rstrip('0').rstrip('.')
          return str(x)

       row = [
              code,
              fmt(self.X),
              fmt(self.ST),
              fmt(self.C),
              fmt(self.CR),
              fmt(self.NC),
              fmt(self.pay_off)
       ]

       col_widths = [
              max(len(headers[i]), len(row[i])) + 2
              for i in range(len(headers))
       ]

       def format_row(values):
              return "|" + "|".join(
              f" {values[i]:<{col_widths[i]-1}}"
              for i in range(len(values))
              ) + "|"

       separator = "+" + "+".join("-" * w for w in col_widths) + "+"

       print(separator)
       print(format_row(headers))
       print(separator)
       print(format_row(row))
       print(separator)


#TEST

# Input values
X = 30000
ST = 38000
C = 860
CR = 1/3
NC = 2000000

opt_payoff = Option_Payoff(X = X,
                           ST = ST,
                           C = C,
                           NC = NC,
                           CR = CR)

opt_payoff.calculate_payoff()
opt_payoff.display_payoff('CVPB2604')
