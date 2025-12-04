import pandas as pd
import numpy as np
from fractions import Fraction


def get_inputs():
    mode = input("Type 'c' for calls, 'p' for puts, 'b' for both: ").strip().lower()

    X1 = int(input("Enter strike 1: "))
    X2 = int(input("Enter strike 2: "))
    X3 = int(input("Enter strike 3: "))

    cx1 = cx2 = cx3 = None
    px1 = px2 = px3 = None

    if mode in ("c", "b"):
        cx1 = float(input("Enter CALL price at strike 1: "))
        cx2 = float(input("Enter CALL price at strike 2: "))
        cx3 = float(input("Enter CALL price at strike 3: "))

    if mode in ("p", "b"):
        px1 = float(input("Enter PUT price at strike 1: "))
        px2 = float(input("Enter PUT price at strike 2: "))
        px3 = float(input("Enter PUT price at strike 3: "))

    return {
        "mode": mode,
        "Cx1": cx1, "Cx2": cx2, "Cx3": cx3,
        "Px1": px1, "Px2": px2, "Px3": px3,
        "X1": X1, "X2": X2, "X3": X3
    }



def check_arbitrage(inputs):
    cx1, cx2, cx3 = inputs['Cx1'], inputs['Cx2'], inputs['Cx3']
    px1, px2, px3 = inputs['Px1'], inputs['Px2'], inputs['Px3']
    X1, X2, X3 = inputs['X1'], inputs['X2'], inputs['X3'] 
    
    
    flags = []
   
    if inputs['mode'] in ('c', 'b'):
    
        if cx1 < cx2:
            flags.append('cx2_overpriced')

        if cx1 - cx2 > X2 - X1:
            flags.append('cx1_overpriced')

        if (cx1 - cx2)/(X2 - X1) < (cx2 - cx3)/(X3 - X2):
            flags.append('butterfly')
    
    if inputs['mode'] in ('p', 'b'):
        
        if px1 > px2:
            flags.append('px1_overpriced')

        if px2 - px1 > X2 - X1:
            flags.append('px2_overpriced')
    
        if (px2 - px1) / (X2 - X1) > (px3 - px2) / (X3 - X2):
            flags.append('butterfly_put')
   
    return flags



def payoff_table(inputs, flags):
    cx1, cx2 = inputs['Cx1'], inputs['Cx2']
    px1, px2 = inputs['Px1'], inputs['Px2']
    X1, X2 = inputs['X1'], inputs['X2']

    trans = []
    now = []
    c1 = []
    c2 = []
    c3 = []

    if 'cx2_overpriced' in flags:
        credit = cx2 - cx1
        trans += [f"Long {X1}-strike call", f"Short {X2}-strike call", "Total"]
        now += [-cx1, cx2, credit]
        c1 += ['0','0', f"{credit}"]
        c2 += [f"S(T) - {X1}", '0', f"{credit} + {X2} - S(T)"]
        c3 += [f"S(T) - {X1}", f"{X2} - S(T)", f"{credit + (X2 - X1)}"]

    if 'cx1_overpriced' in flags:
        credit = cx1 - cx2
        trans += [f"Long {X2}-strike call", f"Short {X1}-strike call", "Total"]
        now += [-cx2, cx1, credit]
        c1 += ["0", "0", f"{credit}"]
        c2 += ["0", f"{X1} - S(T)", f"{credit} + {X1} - S(T)"]
        c3 += [f"S(T) - {X2}", f"{X1} - S(T)", f"{credit + (X1 - X2)}"]

    if 'px1_overpriced' in flags:
        credit = px1 - px2
        trans += [f"Long {X2}-strike put", f"Short {X1}-strike put", 'Total']
        now += [-px2, px1, credit]
        c1 += [f"{X2} - S(T)", f"S(T) - {X1}", f"{credit + (X2 - X1)}"]
        c2 += [f"{X2} - S(T)", '0', f"{credit} + {X2} - S(T)"]
        c3 += ['0','0',f"{credit}"]

    if 'px2_overpriced' in flags:
        credit = px2 - px1
        trans += [f"Long {X1}-strike put", f"Short {X2}-strike put", 'Total']
        now += [-px1, px2, credit]
        c1 += [f"{X1} - S(T)", f"S(T) - {X2}", f"{credit + (X1 - X2)}"]
        c2 += ['0', f"S(T) - {X2}", f"{credit} + S(T) - {X2}"]
        c3 += ['0', '0', f"{credit}"]




    data = {
        "Transaction": trans,
        "Time now":   now,
        f"S(T) < {X1}": c1,
        f"{X1} < S(T) < {X2}": c2,
        f"S(T) > {X2}": c3,
    }

    return pd.DataFrame(data)


def payoff_table_butterfly(inputs, flags):
    cx1, cx2, cx3 = inputs['Cx1'], inputs['Cx2'], inputs['Cx3']
    px1, px2, px3 = inputs['Px1'], inputs['Px2'], inputs['Px3']
    X1, X2, X3 = inputs['X1'], inputs['X2'], inputs['X3']

    lambda_ = (X3 - X2) / (X3 - X1)
    frac = Fraction(lambda_).limit_denominator(100)   # e.g. 0.4 -> 2/5
    n2 = frac.denominator                         # X2 weight
    n1 = frac.numerator                           # X1 weight
    n3 = n2 - n1                                  # X3 weight

    trans = []
    now = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []

    if 'butterfly' in flags:
        credit_long_x1 = -n1 * cx1
        credit_short_x2 = n2 * cx2
        credit_long_x3 = -n3 * cx3

        credit = credit_long_x1 + credit_short_x2 + credit_long_x3
        trans += [f"Long {n1}: {X1}-strike call", f"Short {n2}: {X2}-strike call", f"Long {n3}: {X3}-strike call", "Total"]
        now += [credit_long_x1, credit_short_x2, credit_long_x3, credit]
        c1 += ['0', '0', '0', f"{credit}"]
        c2 += [f"{n1}(S(T) - {X1})", '0', '0', f"{credit} + {n1}(S(T) - {X1})"]
        c3 += [f"{n1}(S(T) - {X1})", f"{n2}({X2} - S(T))", '0', f"{credit} + {n3}({X3} - S(T))"]
        c4 += [f"{n1}(S(T) - {X1})", f"{n2}({X2} - S(T))", f"{n3}(S(T) - {X3})", f"{credit}"]

    if 'butterfly_put' in flags:
        credit_long_x1 = -n1 * px1
        credit_short_x2 = n2 * px2
        credit_long_x3 = -n3 * px3

        credit = credit_long_x1 + credit_short_x2 + credit_long_x3
        trans += [f"Long {n1}: {X1}-strike put", f"Short {n2}: {X2}-strike put", f"Long {n3}: {X3}-strike put", 'Total']
        now += [credit_long_x1, credit_short_x2, credit_long_x3, credit]
        c1 += [f"{n1}({X2} - S(T))", f"{n2}(S(T) - {X2})", f"{n3}({X3} - S(T))", f"{credit}"]
        c2 += ['0', f"{n2}(S(T) - {X2})", f"{n3}({X3} - S(T)", f"{credit} + {n1}({X1} - S(T))"]
        c3 += ['0', '0', f"{n3}({X3} - S(T))", f"{credit} + {n3}({X3} - S(T))" ]
        c4 += ['0', '0', '0', f"{credit}"]
            
    

    data = {
        "Transaction": trans,
        "Time now":   now,
        f"S(T) < {X1}": c1,
        f"{X1} < S(T) < {X2}": c2,
        f"{X2} < S(T) < {X3}": c3,
        f"S(T) > {X3}": c4
    }

    return pd.DataFrame(data)


def vertical_call_payoff(S, X1, X2, cx1, cx2, which):  
    if which == 'cx2_overpriced':
        return (np.maximum(0, S-X1)-cx1) - (np.maximum(0, S-X2)-cx2)
    elif which == 'cx1_overpriced':
        return (np.maximum(0, S-X2)-cx2) - (np.maximum(0, S-X1)-cx1)

def vertical_put_payoff(S, X1, X2, px1, px2, which):
    if which == 'px1_overpriced':
        return (np.maximum(X1-S,0)-px1) - (np.maximum(X2-S,0)-px2)
    elif which == 'px2_overpriced':
        return (np.maximum(X2-S,0)-px2) - (np.maximum(X1-S,0)-px1)
    
def butterfly_call_payoff(S, X1, X2, X3, cx1, cx2, cx3):
    lam  = (X3-X2)/(X3-X1)
    frac = Fraction(lam).limit_denominator(100)
    n2 = frac.denominator; n1 = frac.numerator; n3 = n2-n1
    return (n1 * (np.maximum(0,S-X1)-cx1)
           -n2 * (np.maximum(0,S-X2)-cx2)
           +n3 * (np.maximum(0,S-X3)-cx3))

def butterfly_put_payoff(S, X1, X2, X3, px1, px2, px3):
    lam  = (X3-X2)/(X3-X1)
    frac = Fraction(lam).limit_denominator(100)
    n2 = frac.denominator; n1 = frac.numerator; n3 = n2-n1
    return (n1 * (np.maximum(X1-S,0)-px1)
           -n2 * (np.maximum(X2-S,0)-px2)
           +n3 * (np.maximum(X3-S,0)-px3))
