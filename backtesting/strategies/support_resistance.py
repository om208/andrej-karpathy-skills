import pandas as pd
import numpy as np
import sys
sys.path.append('/home/user/andrej-karpathy-skills/backtesting')
from strategy_base import Strategy

class SupportResistanceStrategy(Strategy):
    """
    Support/Resistance with Volume Confirmation and RSI

    Entry: Price bounces off support + volume spike + RSI oversold
    Exit: Take profit (strategy-defined), stop loss, or RSI overbought
    """

    def __init__(self, df, initial_capital=100, risk_per_trade=7, max_loss=10,
                 support_lookback=20, volume_threshold=1.5, rsi_oversold=30,
                 rsi_overbought=70, tp_atr_multiplier=1.5):
        super().__init__(df, initial_capital, risk_per_trade, max_loss)
        self.support_lookback = support_lookback
        self.volume_threshold = volume_threshold
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.tp_atr_multiplier = tp_atr_multiplier

    def _calculate_rsi(self, prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100. / (1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down if down != 0 else 0
            rsi[i] = 100. - 100. / (1. + rs)

        return rsi

    def _calculate_atr(self, high, low, close, period=14):
        tr = np.maximum(
            high - low,
            np.maximum(
                abs(high - np.roll(close, 1)),
                abs(low - np.roll(close, 1))
            )
        )
        tr[0] = high[0] - low[0]
        atr = pd.Series(tr).rolling(period).mean().values
        return atr

    def _find_support_level(self, idx):
        if idx < self.support_lookback:
            return self.df['low'].iloc[:idx+1].min()
        return self.df['low'].iloc[idx-self.support_lookback:idx+1].min()

    def generate_signals(self):
        df = self.df.copy()

        close = df['close'].values
        high = df['high'].values
        low = df['low'].values
        volume = df['volume'].values

        df['rsi'] = self._calculate_rsi(close)
        df['atr'] = self._calculate_atr(high, low, close)
        df['volume_ma'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / (df['volume_ma'] + 1)

        self.signals = df
        return df

    def backtest(self):
        df = self.signals.copy()
        trades = []
        position = None

        for idx in range(1, len(df)):
            current = df.iloc[idx]
            prev = df.iloc[idx - 1]

            if position is None:
                support = self._find_support_level(idx)

                is_at_support = abs(current['close'] - support) < (current['close'] * 0.005)
                has_volume = current['volume_ratio'] > self.volume_threshold
                is_oversold = current['rsi'] < self.rsi_oversold

                if is_at_support and has_volume and is_oversold:
                    entry_price = current['close']
                    position_size = self.calculate_position_size(entry_price)

                    if position_size > 0:
                        atr = current['atr']
                        stop_loss = entry_price - (atr * 0.5)
                        take_profit = entry_price + (atr * self.tp_atr_multiplier)

                        position = {
                            'entry_idx': idx,
                            'entry_time': current['datetime'],
                            'entry_price': entry_price,
                            'position_size': position_size,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'support': support,
                            'entry_rsi': current['rsi']
                        }
            else:
                high = current['high']
                low = current['low']
                close = current['close']

                sl_hit = low <= position['stop_loss']
                tp_hit = high >= position['take_profit']
                rsi_exit = current['rsi'] > self.rsi_overbought and close > position['entry_price']

                if sl_hit or tp_hit or rsi_exit:
                    exit_price = close
                    if sl_hit:
                        exit_price = position['stop_loss']
                        exit_reason = 'stop_loss'
                    elif tp_hit:
                        exit_price = position['take_profit']
                        exit_reason = 'take_profit'
                    else:
                        exit_reason = 'rsi_exit'

                    pnl = (exit_price - position['entry_price']) * position['position_size']

                    trade = {
                        'entry_idx': position['entry_idx'],
                        'exit_idx': idx,
                        'entry_time': position['entry_time'],
                        'exit_time': current['datetime'],
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'position_size': position['position_size'],
                        'pnl': pnl,
                        'win': pnl > 0,
                        'exit_reason': exit_reason,
                        'support': position['support'],
                        'risk_reward': abs((position['take_profit'] - position['entry_price']) /
                                         (position['entry_price'] - position['stop_loss'])) if position['entry_price'] != position['stop_loss'] else 0
                    }
                    trades.append(trade)
                    position = None

        self.trades = trades
        return trades
