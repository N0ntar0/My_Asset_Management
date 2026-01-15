# Default constants (used if not provided)
DEFAULT_LIVING_TARGET = 100000
DEFAULT_BUFFER_TARGET = 500000

def calculate_allocation(surplus_funds: int, current_buffer: int, current_living_expenses: int = 100000,
                        living_target: int = DEFAULT_LIVING_TARGET, buffer_target: int = DEFAULT_BUFFER_TARGET) -> dict:
    """
    Calculates the allocation of surplus funds based on the logic:
    0. Living Expenses Priority (Current Living < Target):
       - Fill Living Expenses up to Target first.
    1. Buffer Recovery Mode (Current Buffer < Target):
       - 50% to Buffer (Sony Bank)
       - 50% to Investment
    2. Normal Investment Mode (Current Buffer >= Target):
       - 100% to Investment
    
    Args:
        surplus_funds (int): The amount of money available for allocation.
        current_buffer (int): Current balance in Sony Bank (Buffer).
        current_living_expenses (int): Current balance in PayPay Bank (Living Expenses).
        living_target (int): Target amount for Living Expenses (default 100,000).
        buffer_target (int): Target amount for Buffer (default 500,000).

    Returns:
        dict: Allocation result {'buffer': int, 'investment': int, 'living_expenses': int, 'mode': str}
    """
    
    remaining_surplus = surplus_funds
    living_expenses_alloc = 0
    
    # Priority 0: Ensure Living Expenses has at least Target
    if current_living_expenses < living_target:
        needed = living_target - current_living_expenses
        alloc = min(remaining_surplus, needed)
        living_expenses_alloc = alloc
        remaining_surplus -= alloc

    if remaining_surplus == 0:
        # Determine mode based on state (for Dashboard display or exhausted funds)
        if current_living_expenses < living_target:
            mode = '生活費補填モード'
        elif current_buffer < buffer_target:
            mode = '予備費補填モード'
        else:
            mode = '余剰金運用モード'

        return {
            'mode': mode,
            'buffer': 0,
            'investment': 0,
            'living_expenses': living_expenses_alloc
        }

    # Remaining logic
    if current_buffer < buffer_target:
        # Buffer Recovery Mode
        needed_for_buffer = buffer_target - current_buffer
        
        # Standard: 50% to Buffer
        tentative_buffer_alloc = remaining_surplus // 2
        
        # Cap logic: Don't exceed target
        if tentative_buffer_alloc > needed_for_buffer:
            buffer_alloc = needed_for_buffer
            # Remaining goes to investment
            investment_alloc = remaining_surplus - buffer_alloc
        else:
            buffer_alloc = tentative_buffer_alloc
            investment_alloc = remaining_surplus - buffer_alloc
        
        mode = '予備費補填モード'
        if living_expenses_alloc > 0:
            mode += ' (生活費充当あり)'
            
        return {
            'mode': mode,
            'buffer': buffer_alloc,
            'investment': investment_alloc,
            'living_expenses': living_expenses_alloc
        }
    else:
        # Normal Investment Mode
        mode = '余剰金運用モード'
        if living_expenses_alloc > 0:
            mode += ' (生活費充当あり)'

        return {
            'mode': mode,
            'buffer': 0,
            'investment': remaining_surplus,
            'living_expenses': living_expenses_alloc
        }
