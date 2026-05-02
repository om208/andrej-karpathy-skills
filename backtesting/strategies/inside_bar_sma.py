import pandas as pd
import numpy as np
import sys
sys.path.append('/home/user/andrej-karpathy-skills/backtesting')
from strategy_base import Strategy

class InsideBarSMAStrategy(Strategy):
    """
    Inside Bar Pattern with SMA Touch Strategy

    Rules:
    1. Detect inside bar pattern (high < prev_high, low > prev_low)
    2. 96-period SMA must touch the inside bar
    3. Entry: When SMA touches the inside bar
    4. Exit: After 159 minutes OR on stop loss/take profit
    5. Market expects drastic move after SMA touch
    """

    def __init__(self, df, initial_capital=100, risk_per_trade=7, max_loss=10,
                 sma_period=96, touch_threshold=0.02, exit_minutes=159,
                 tp_pips=150, sl_pips=50):
        super().__init__(df, initial_capital, risk_per_trade, max_loss)
        self.sma_period = sma_period
        self.touch_threshold = touch_threshold  # % threshold for touch detection
        self.exit_minutes = exit_minutes
        self.tp_pips = tp_pips
        self.sl_pips = sl_pips

    def _is_inside_bar(self, idx):
        """Check if current bar is inside the previous bar"""
        if idx < 1:
            return False

        curr = self.df.iloc[idx]
        prev = self.df.iloc[idx - 1]

        # Inside bar: curr_high < prev_high AND curr_low > prev_low
        is_inside = (curr['high'] < prev['high']) and (curr['low'] > prev['low'])
        return is_inside

    def _sma_touches_candle(self, idx):
        """Check if SMA touches the candle (within threshold)"""
        if idx < self.sma_period:
            return False, None

        curr = self.df.iloc[idx]
        sma = curr['sma_96']

        candle_range = curr['high'] - curr['low']
        threshold = candle_range * self.touch_threshold

        # SMA touches if it's within the candle or very close
        touches = (curr['low'] - threshold <= sma <= curr['high'] + threshold)

        return touches, sma

    def _check_drastic_move(self, entry_idx, current_idx):
        """Check if there's drastic move (for analysis purposes)"""
        entry_price = self.df.iloc[entry_idx]['close']
        current_price = self.df.iloc[current_idx]['close']
        move = abs(current_price - entry_price)
        move_percent = (move / entry_price) * 100
        return move_percent

    def generate_signals(self):
        df = self.df.copy()

        # Calculate 96-period SMA
        df['sma_96'] = df['close'].rolling(window=self.sma_period).mean()
        self.df = df  # Update self.df with SMA values

        # Detect inside bars
        df['is_inside_bar'] = [self._is_inside_bar(i) for i in range(len(df))]

        # Check if SMA touches
        sma_touches = []
        for i in range(len(df)):
            touches, sma_val = self._sma_touches_candle(i)
            sma_touches.append(touches)
        df['sma_touches'] = sma_touches

        # Entry signal: inside bar AND SMA touches
        df['entry_signal'] = df['is_inside_bar'] & df['sma_touches']

        self.signals = df
        return df

    def backtest(self):
        df = self.signals.copy()
        trades = []
        position = None

        for idx in range(self.sma_period + 1, len(df)):
            current = df.iloc[idx]

            if position is None:
                # Check for entry signal
                if current['entry_signal']:
                    entry_price = current['close']
                    position_size = self.calculate_position_size(entry_price)

                    if position_size > 0:
                        # Calculate stop loss and take profit
                        stop_loss = entry_price - (self.sl_pips * 0.01)
                        take_profit = entry_price + (self.tp_pips * 0.01)

                        position = {
                            'entry_idx': idx,
                            'entry_time': current['datetime'],
                            'entry_price': entry_price,
                            'position_size': position_size,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'sma_value': current['sma_96'],
                            'entry_candle_high': current['high'],
                            'entry_candle_low': current['low'],
                            'prev_candle_high': df.iloc[idx-1]['high'],
                            'prev_candle_low': df.iloc[idx-1]['low']
                        }
            else:
                # Check exit conditions
                minutes_held = idx - position['entry_idx']
                high = current['high']
                low = current['low']
                close = current['close']

                # Exit reasons (in priority order)
                sl_hit = low <= position['stop_loss']
                tp_hit = high >= position['take_profit']
                time_exit = minutes_held >= self.exit_minutes

                if sl_hit or tp_hit or time_exit:
                    if sl_hit:
                        exit_price = position['stop_loss']
                        exit_reason = 'stop_loss'
                    elif tp_hit:
                        exit_price = position['take_profit']
                        exit_reason = 'take_profit'
                    else:
                        exit_price = close
                        exit_reason = 'time_exit'

                    pnl = (exit_price - position['entry_price']) * position['position_size']
                    drastic_move = self._check_drastic_move(position['entry_idx'], idx)

                    risk_reward = abs((position['take_profit'] - position['entry_price']) /
                                     (position['entry_price'] - position['stop_loss'])) if position['entry_price'] != position['stop_loss'] else 0

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
                        'minutes_held': minutes_held,
                        'sma_value': position['sma_value'],
                        'drastic_move_percent': drastic_move,
                        'entry_candle_high': position['entry_candle_high'],
                        'entry_candle_low': position['entry_candle_low'],
                        'prev_candle_high': position['prev_candle_high'],
                        'prev_candle_low': position['prev_candle_low'],
                        'inside_bar_range': position['entry_candle_high'] - position['entry_candle_low'],
                        'prev_bar_range': position['prev_candle_high'] - position['prev_candle_low'],
                        'risk_reward': risk_reward
                    }
                    trades.append(trade)
                    position = None

        self.trades = trades
        return trades
