import schedule
import time
from trading import run_get_previous_day_high_low, run_get_previous_asia_session_high_low
from session import delete_pending_orders_at_1am, adjust_sl_tp

# Function to schedule tasks
def schedule_tasks(currency_pairs, day_high_low_time, asia_high_low_time, delete_orders_time, lot_size):
    # Schedule get_previous_day_high_low at the specified time
    schedule.every().day.at(day_high_low_time).do(lambda: run_get_previous_day_high_low(currency_pairs, lot_size))

    # Schedule get_previous_asia_session_high_low at the specified time
    schedule.every().day.at(asia_high_low_time).do(lambda: run_get_previous_asia_session_high_low(currency_pairs, lot_size))

    # Schedule delete_pending_orders_at_1am at the specified time
    schedule.every().day.at(delete_orders_time).do(delete_pending_orders_at_1am)

def run_scheduler():
    try:
        while True:
            adjust_sl_tp()
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    finally:
        # Shutdown MetaTrader5 connection
        mt5.shutdown()