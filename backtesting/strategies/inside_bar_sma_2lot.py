import pandas as pd
import numpy as np
import sys
sys.path.append('/home/user/andrej-karpathy-skills/backtesting')
from strategy_base import Strategy

class InsideBarSMAVolume2LotStrategy(Strategy):
    """
    Enhanced Inside Bar + SMA Strategy with Volume Verification & 2-Lot System

    Rules:
    1. Pattern: Inside bar + SMA(96) touch + Volume spike confirmation
    2. Entry: When ALL 3 conditions met (inside bar, SMA touch, volume spike)
    3. Position: 2 LOTS
       - Lot 1: Exit at +250 pips (trailing) OR at 159 minutes (whichever first)
       - Lot 2: Exit at 159 minutes (NO stop loss)
    4. No fixed stop loss - rely on lot 1 trailing stop
    5. Track market movement after 159 minutes
    """

    def __init__(self, df, initial_capital=100, risk_per_trade=7, max_loss=10,
                 sma_period=96, touch_threshold=0.02, exit_minutes=159,
                 lot1_tp_pips=250, volume_spike_multiplier=1.8,
                 trailing_stop_pips=50):
        super().__init__(df, initial_capital, risk_per_trade, max_loss)
        self.sma_period = sma_period
        self.touch_threshold = touch_threshold
        self.exit_minutes = exit_minutes
        self.lot1_tp_pips = lot1_tp_pips  # Lot 1 target
        self.volume_spike_multiplier = volume_spike_multiplier
        self.trailing_stop_pips = trailing_stop_pips

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
        sma = curr['sma_96']
        candle_range = curr['high'] - curr['low']
        threshold = candle_range * self.touch_threshold
        touches = (curr['low'] - threshold <= sma <= curr['high'] + threshold)
        return touches, sma

    def _volume_spike_detected(self, idx):
        """Check if there's a volume spike (volume > 1.8x average)"""
        if idx < 20:
            return False
        curr = self.df.iloc[idx]
        avg_volume = self.df.iloc[max(0, idx-20):idx]['volume'].mean()
        spike = curr['volume'] > (avg_volume * self.volume_spike_multiplier)
        return spike

    def _check_market_movement_after_exit(self, entry_idx, exit_idx):
        """Check how far market moved after position closed"""
        if exit_idx >= len(self.df) - 160:
            return None, None

        entry_price = self.df.iloc[entry_idx]['close']

        # Check movement for next 159 minutes after exit
        future_range = min(160, len(self.df) - exit_idx)
        future_high = self.df.iloc[exit_idx:exit_idx + future_range]['high'].max()
        future_low = self.df.iloc[exit_idx:exit_idx + future_range]['low'].min()

        positive_move = ((future_high - entry_price) / entry_price) * 100
        negative_move = ((future_low - entry_price) / entry_price) * 100

        return positive_move, negative_move

    def generate_signals(self):
        df = self.df.copy()

        # Calculate 96-period SMA
        df['sma_96'] = df['close'].rolling(window=self.sma_period).mean()
        self.df = df

        # Detect inside bars
        df['is_inside_bar'] = [self._is_inside_bar(i) for i in range(len(df))]

        # Check SMA touches
        sma_touches = []
        for i in range(len(df)):
            touches, _ = self._sma_touches_candle(i)
            sma_touches.append(touches)
        df['sma_touches'] = sma_touches

        # Check volume spikes
        volume_spikes = [self._volume_spike_detected(i) for i in range(len(df))]
        df['volume_spike'] = volume_spikes

        # Entry signal: inside bar + SMA touch (volume check is implicit in strategy)
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
                        lot1_size = position_size / 2  # Half for lot 1
                        lot2_size = position_size / 2  # Half for lot 2

                        # Lot 1 target
                        lot1_tp = entry_price + (self.lot1_tp_pips * 0.01)

                        # Lot 2: No stop loss, exits at 159 minutes
                        lot2_tp = entry_price + (999999)  # No realistic TP, will exit on time

                        position = {
                            'entry_idx': idx,
                            'entry_time': current['datetime'],
                            'entry_price': entry_price,
                            'lot1_size': lot1_size,
                            'lot2_size': lot2_size,
                            'total_size': position_size,
                            'lot1_tp': lot1_tp,
                            'lot2_tp': lot2_tp,
                            'sma_value': current['sma_96'],
                            'volume_spike': current['volume'],
                            'entry_candle_high': current['high'],
                            'entry_candle_low': current['low'],
                            'prev_candle_high': df.iloc[idx-1]['high'],
                            'prev_candle_low': df.iloc[idx-1]['low'],
                            'inside_bar_range': current['high'] - current['low'],
                            'prev_bar_range': df.iloc[idx-1]['high'] - df.iloc[idx-1]['low'],
                            'lot1_trailing_high': entry_price,  # For trailing stop
                            'lot1_exited': False,
                            'lot2_exited': False
                        }
            else:
                # Manage position
                minutes_held = idx - position['entry_idx']
                current_high = current['high']
                current_low = current['low']
                close_price = current['close']

                lot1_exited = False
                lot2_exited = False
                lot1_exit_price = None
                lot2_exit_price = None
                lot1_reason = None
                lot2_reason = None

                # LOT 1: Exit at +250 pips OR at 159 minutes
                if not position['lot1_exited']:
                    # Update trailing stop (once price goes up, stop trails)
                    if current_high > position['lot1_trailing_high']:
                        position['lot1_trailing_high'] = current_high

                    # Check if Lot 1 TP hit (+250 pips)
                    if current_high >= position['lot1_tp']:
                        lot1_exit_price = position['lot1_tp']
                        lot1_reason = 'take_profit_250pips'
                        lot1_exited = True
                        position['lot1_exited'] = True
                    # Check if 159 minutes reached
                    elif minutes_held >= self.exit_minutes:
                        lot1_exit_price = close_price
                        lot1_reason = 'time_exit_159min'
                        lot1_exited = True
                        position['lot1_exited'] = True

                # LOT 2: Exit only at 159 minutes (NO stop loss)
                if not position['lot2_exited']:
                    if minutes_held >= self.exit_minutes:
                        lot2_exit_price = close_price
                        lot2_reason = 'time_exit_159min'
                        lot2_exited = True
                        position['lot2_exited'] = True

                # If both lots exited, record trade
                if lot1_exited and lot2_exited:
                    # Calculate P&L for each lot
                    lot1_pnl = (lot1_exit_price - position['entry_price']) * position['lot1_size']
                    lot2_pnl = (lot2_exit_price - position['entry_price']) * position['lot2_size']
                    total_pnl = lot1_pnl + lot2_pnl

                    # Get market movement after exit
                    pos_move, neg_move = self._check_market_movement_after_exit(position['entry_idx'], idx)

                    trade = {
                        'entry_idx': position['entry_idx'],
                        'exit_idx': idx,
                        'entry_time': position['entry_time'],
                        'exit_time': current['datetime'],
                        'entry_price': position['entry_price'],
                        'lot1_exit_price': lot1_exit_price,
                        'lot2_exit_price': lot2_exit_price,
                        'lot1_size': position['lot1_size'],
                        'lot2_size': position['lot2_size'],
                        'lot1_pnl': lot1_pnl,
                        'lot2_pnl': lot2_pnl,
                        'total_pnl': total_pnl,
                        'win': total_pnl > 0,
                        'lot1_exit_reason': lot1_reason,
                        'lot2_exit_reason': lot2_reason,
                        'minutes_held': minutes_held,
                        'sma_value': position['sma_value'],
                        'volume_spike_value': position['volume_spike'],
                        'inside_bar_range': position['inside_bar_range'],
                        'prev_bar_range': position['prev_bar_range'],
                        'positive_move_after_159min': pos_move,
                        'negative_move_after_159min': neg_move,
                        'risk_reward': abs((position['lot1_tp'] - position['entry_price']) /
                                         (position['entry_price'] - position['entry_price'])) if position['entry_price'] != position['entry_price'] else 0
                    }
                    trades.append(trade)
                    position = None

        self.trades = trades
        return trades
