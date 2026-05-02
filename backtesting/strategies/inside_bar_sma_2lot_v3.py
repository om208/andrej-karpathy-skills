import pandas as pd
import numpy as np
import sys
sys.path.append('/home/user/andrej-karpathy-skills/backtesting')
from strategy_base import Strategy

class InsideBarSMA2LotV3Strategy(Strategy):
    """
    2-Lot Inside Bar + SMA(196) Strategy - FIXED VERSION

    Uses EXACT entry logic from working 319-trade strategy
    Only changes exit management to 2-lot system

    Rules:
    1. Entry: Inside bar + SMA(196) touch + Volume(1.5x)
    2. Position: 2 LOTS
       - Lot 1: Exit at +250 pips OR at 159 minutes
       - Lot 2: Exit at 159 minutes (NO stop loss)
    3. Track market movement after exit
    """

    def __init__(self, df, initial_capital=100, risk_per_trade=7, max_loss=10,
                 sma_period=196, touch_threshold=0.02, exit_minutes=159,
                 lot1_tp_pips=250, volume_threshold=0.0):
        super().__init__(df, initial_capital, risk_per_trade, max_loss)
        self.sma_period = sma_period
        self.touch_threshold = touch_threshold
        self.exit_minutes = exit_minutes
        self.lot1_tp_pips = lot1_tp_pips
        self.volume_threshold = volume_threshold

    def _is_inside_bar(self, idx):
        """Check if current bar is inside the previous bar"""
        if idx < 1:
            return False
        curr = self.df.iloc[idx]
        prev = self.df.iloc[idx - 1]
        is_inside = (curr['high'] < prev['high']) and (curr['low'] > prev['low'])
        return is_inside

    def _sma_touches_candle(self, idx):
        """Check if SMA touches the candle"""
        if idx < self.sma_period:
            return False, None
        curr = self.df.iloc[idx]
        sma = curr[f'sma_{self.sma_period}']
        candle_range = curr['high'] - curr['low']
        threshold = candle_range * self.touch_threshold
        touches = (curr['low'] - threshold <= sma <= curr['high'] + threshold)
        return touches, sma

    def _check_market_movement_after_exit(self, entry_idx, exit_idx):
        """Check how far market moved after position closed"""
        if exit_idx >= len(self.df) - 160:
            return None, None

        entry_price = self.df.iloc[entry_idx]['close']
        future_range = min(160, len(self.df) - exit_idx)
        future_high = self.df.iloc[exit_idx:exit_idx + future_range]['high'].max()
        future_low = self.df.iloc[exit_idx:exit_idx + future_range]['low'].min()

        positive_move = ((future_high - entry_price) / entry_price) * 100
        negative_move = ((future_low - entry_price) / entry_price) * 100

        return positive_move, negative_move

    def generate_signals(self):
        df = self.df.copy()

        df[f'sma_{self.sma_period}'] = df['close'].rolling(window=self.sma_period).mean()
        if self.volume_threshold > 0:
            df['volume_ma'] = df['volume'].rolling(20).mean()

        self.df = df
        self.signals = df
        return df

    def backtest(self):
        df = self.signals.copy()
        trades = []
        position = None

        for idx in range(1, len(df)):
            current = df.iloc[idx]

            if position is None:
                # Check entry conditions (EXACT same as working 319-trade strategy)
                is_inside = self._is_inside_bar(idx)
                sma_touch, sma_val = self._sma_touches_candle(idx)

                # Volume check only if threshold > 0
                if self.volume_threshold > 0:
                    volume_ratio = current['volume'] / (current['volume_ma'] + 1)
                    has_volume = volume_ratio > self.volume_threshold
                else:
                    has_volume = True
                    volume_ratio = 0

                # Entry: inside bar AND SMA touch (volume optional)
                if is_inside and sma_touch and has_volume:
                    entry_price = current['close']
                    position_size = self.calculate_position_size(entry_price)

                    if position_size > 0:
                        lot1_size = position_size / 2
                        lot2_size = position_size / 2
                        lot1_tp = entry_price + (self.lot1_tp_pips * 0.01)

                        position = {
                            'entry_idx': idx,
                            'entry_time': current['datetime'],
                            'entry_price': entry_price,
                            'lot1_size': lot1_size,
                            'lot2_size': lot2_size,
                            'total_size': position_size,
                            'lot1_tp': lot1_tp,
                            'sma_value': sma_val,
                            'volume_ratio': volume_ratio,
                            'inside_bar_range': current['high'] - current['low'],
                            'prev_bar_range': df.iloc[idx-1]['high'] - df.iloc[idx-1]['low'],
                            'lot1_exited': False,
                            'lot2_exited': False,
                            'lot1_exit_price': None,
                            'lot2_exit_price': None
                        }
            else:
                # Manage position
                minutes_held = idx - position['entry_idx']
                high = current['high']
                close = current['close']

                # LOT 1: Exit at +250 pips OR 159 minutes (whichever first)
                if not position['lot1_exited']:
                    if high >= position['lot1_tp']:
                        position['lot1_exit_price'] = position['lot1_tp']
                        position['lot1_exit_reason'] = 'take_profit_250pips'
                        position['lot1_exited'] = True
                    elif minutes_held >= self.exit_minutes:
                        position['lot1_exit_price'] = close
                        position['lot1_exit_reason'] = 'time_exit_159min'
                        position['lot1_exited'] = True

                # LOT 2: Exit ONLY at 159 minutes (NO stop loss)
                if not position['lot2_exited']:
                    if minutes_held >= self.exit_minutes:
                        position['lot2_exit_price'] = close
                        position['lot2_exit_reason'] = 'time_exit_159min'
                        position['lot2_exited'] = True

                # Record trade when both lots are exited
                if position['lot1_exited'] and position['lot2_exited']:
                    lot1_pnl = (position['lot1_exit_price'] - position['entry_price']) * position['lot1_size']
                    lot2_pnl = (position['lot2_exit_price'] - position['entry_price']) * position['lot2_size']
                    total_pnl = lot1_pnl + lot2_pnl

                    pos_move, neg_move = self._check_market_movement_after_exit(position['entry_idx'], idx)

                    trade = {
                        'entry_idx': position['entry_idx'],
                        'exit_idx': idx,
                        'entry_time': position['entry_time'],
                        'exit_time': current['datetime'],
                        'entry_price': position['entry_price'],
                        'lot1_exit_price': position['lot1_exit_price'],
                        'lot2_exit_price': position['lot2_exit_price'],
                        'lot1_size': position['lot1_size'],
                        'lot2_size': position['lot2_size'],
                        'lot1_pnl': lot1_pnl,
                        'lot2_pnl': lot2_pnl,
                        'total_pnl': total_pnl,
                        'win': total_pnl > 0,
                        'lot1_exit_reason': position['lot1_exit_reason'],
                        'lot2_exit_reason': position['lot2_exit_reason'],
                        'minutes_held': minutes_held,
                        'sma_value': position['sma_value'],
                        'volume_ratio': position['volume_ratio'],
                        'inside_bar_range': position['inside_bar_range'],
                        'prev_bar_range': position['prev_bar_range'],
                        'positive_move_after_159min': pos_move,
                        'negative_move_after_159min': neg_move,
                        'risk_reward': 1.0
                    }
                    trades.append(trade)
                    position = None

        self.trades = trades
        return trades
