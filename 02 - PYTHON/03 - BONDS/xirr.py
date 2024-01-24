from datetime import date
from pyxirr import xirr, DayCount

dates = [date(2020, 1, 1), date(2021, 1, 1), date(2022, 1, 1)]
amounts = [-1000, 750, 500]

# feed columnar data
# xirr(dates, amounts)

xirr = xirr(dates, amounts, day_count=DayCount.ACT_365F)

print(xirr)

# parse day count from string
# xirr(dates, amounts, day_count="30E/360")

"https://www.rbccm.com/assets/rbccm/docs/legal/doddfrank/Documents/ISDALibrary/2006%20ISDA%20Definitions.pdf"

"https://en.wikipedia.org/wiki/Day_count_convention"

"https://anexen.github.io/pyxirr/functions.html"

"http://www.deltaquants.com/day-count-conventions"

"https://github.com/Anexen/pyxirr"

"https://new.reddit.com/r/merval/comments/l0q41r/como_invertir_en_criptomonedas_paso_a_paso_para/"


"https://new.reddit.com/r/merval/comments/kpah40/introducci%C3%B3n_a_renta_fijabonos_parte_2/"

"https://new.reddit.com/r/merval/comments/kpaffw/introducci%C3%B3n_a_renta_fijabonos_parte_1/"

"https://new.reddit.com/r/merval/comments/jk7nfp/guia_definitiva_para_convertir_dinero_en/"

"https://es.wikipedia.org/wiki/Base_(finanzas)"

"macaulay duration, valor residual, valor tecnico, modified duration xirr"


"""

import numpy as np
import pandas as pd

# feed numpy array
xirr(np.array([dates, amounts]))
xirr(np.array(dates), np.array(amounts))

# feed DataFrame (columns names doesn't matter; ordering matters)
xirr(pd.DataFrame({"a": dates, "b": amounts}))

# feed Series with DatetimeIndex
xirr(pd.Series(amounts, index=pd.to_datetime(dates)))

# bonus: apply xirr to a DataFrame with DatetimeIndex:
df = pd.DataFrame(
    index=pd.date_range("2021", "2022", freq="MS", inclusive="left"),
    data={
        "one": [-100] + [20] * 11,
        "two": [-80] + [19] * 11,
    },
)
df.apply(xirr)  # Series(index=["one", "two"], data=[5.09623547168478, 8.780801977141174])

"""