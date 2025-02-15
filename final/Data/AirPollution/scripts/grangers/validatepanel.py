import pandas as pd

def validate_panel_data(df, time_var='Year', entity_var='City'):
    """Validate balanced panel structure and data completeness"""
    # Check basic structure
    if not isinstance(df.index, pd.MultiIndex):
        print("Data should have MultiIndex (entity, time)")
        return False
    
    # Check balance
    time_counts = df.groupby(entity_var)[time_var].nunique()
    balance_check = {
        'is_balanced': time_counts.nunique() == 1,
        'time_period_counts': time_counts,
        'time_range_consistency': df.groupby(entity_var)[time_var].agg([min, max]).nunique() == 1
    }
    
    # Check completeness
    completeness_check = {
        'missing_values': df.isna().sum(),
        'zero_values': (df == 0).sum()
    }
    
    # Temporal consistency
    time_gaps = df.groupby(entity_var)[time_var].apply(
        lambda x: x.sort_values().diff().value_counts().idxmax()
    )
    
    return {
        'balance_check': balance_check,
        'completeness_check': completeness_check,
        'temporal_consistency': {
            'consistent_time_gaps': time_gaps.nunique() == 1,
            'typical_time_gap': time_gaps.mode()[0]
        }
    }

# Example usage with test data
panel_data = pd.DataFrame({
    'City': ['Berlin']*5 + ['Munich']*5,
    'Year': [2015, 2016, 2017, 2018, 2019]*2,
    'Air Pollution Level': [45, 47, np.nan, 50, 52, 40, 42, 44, 46, 48],
    'SPD': [25.1, 24.8, 24.5, 24.2, 23.9, 30.2, 30.0, 29.8, 29.6, 29.4]
}).set_index(['City', 'Year'])

validation = validate_panel_data(panel_data)

print("Balance Check:")
print(f"Balanced panel: {validation['balance_check']['is_balanced']}")
print(f"Consistent time range: {validation['balance_check']['time_range_consistency']}")

print("\nCompleteness Check:")
print("Missing values:")
print(validation['completeness_check']['missing_values'])

print("\nTemporal Consistency:")
print(f"Consistent time intervals: {validation['temporal_consistency']['consistent_time_gaps']}")
print(f"Typical time gap: {validation['temporal_consistency']['typical_time_gap']}")
