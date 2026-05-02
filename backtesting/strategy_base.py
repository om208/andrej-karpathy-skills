from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class Strategy(ABC):
    """Base class for all strategies"""

    def __init__(self, df, initial_capital=100, risk_per_trade=7, max_loss=10):
        self.df = df.copy()
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.max_loss = max_loss
        self.name = self.__class__.__name__

        self.trades = []
        self.signals = None

    @abstractmethod
    def generate_signals(self):
        """Generate entry/exit signals. Must return df with 'signal' column"""
        pass

    def calculate_position_size(self, entry_price):
        """Calculate position size based on risk and stop loss"""
        if entry_price <= 0:
            return 0
        price_risk = abs(self.max_loss) / entry_price if self.max_loss > 0 else 0.001
        position_size = self.risk_per_trade / (entry_price * price_risk)
        return position_size

    def run(self):
        """Execute the strategy"""
        self.generate_signals()
        return self.backtest()

    @abstractmethod
    def backtest(self):
        """Execute backtest. Return trades list"""
        pass
