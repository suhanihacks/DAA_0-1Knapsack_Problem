import os
import time

def parse_input_file(filepath):
    test_cases = []
    current_test = None
    
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#Test"):
                if current_test:
                    test_cases.append(current_test)
                current_test = {'n': 0, 'W': 0, 'items': []}
            elif current_test is not None:
                parts = list(map(int, line.split()))
                if current_test['n'] == 0 and len(parts) == 2 and not current_test['items']:
                    current_test['n'] = parts[0]
                    current_test['W'] = parts[1]
                else:
                    current_test['items'].append((parts[0], parts[1]))
                    
    if current_test and len(current_test['items']) == current_test['n']:
        test_cases.append(current_test)
        
    return test_cases

def print_ascii_dp_table(dp, items, n, W):
    """Prints an ASCII visualization of the 0-1 Knapsack DP Table."""
    print(f"--- 0/1 Knapsack DP Table Visualization (Capacity: {W}) ---\n")
    
    # Header row
    header = "Item \\ Cap |" + "".join([f"{w:>5}" for w in range(W + 1)])
    print(header)
    print("-" * len(header))
    
    # Base row (0 items)
    row_str = f"{'0 (None)':<11}|"
    for w in range(W + 1):
        row_str += f"{dp[0][w]:>5}"
    print(row_str)
    
    # Item rows
    for i in range(1, n + 1):
        wt, val = items[i - 1]
        row_str = f"{f'i={i} (w:{wt},v:{val})':<11}|"
        for w in range(W + 1):
            row_str += f"{dp[i][w]:>5}"
        print(row_str)
    print("-" * len(header))

def solve_knapsack(n, W, items):
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = items[i - 1]
        for w in range(W + 1):
            if wt <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - wt] + val)
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][W], dp

if __name__ == "__main__":
    test_cases = parse_input_file("Knapsack data (2).txt")
    results = []
    
    for test in test_cases:
        n, W, items = test['n'], test['W'], test['items']
        max_val, dp_table = solve_knapsack(n, W, items)
        results.append(f"#Test case input ({n} {W}) {max_val}")
        
    with open("result.txt", "w") as f:
        f.write("\n".join(results))
