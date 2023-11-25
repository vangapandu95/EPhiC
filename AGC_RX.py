from __future__ import annotations

import gdsfactory as gf
import numpy as np
from gdsfactory.component import Component
from gdsfactory.components.straight import straight as straight_function
from gdsfactory.typings import ComponentSpec
import pandas as pd


@gf.cell
def straight_array(
    n: int = 168,
    spacing: float = 0.300,
    straight: ComponentSpec = straight_function,
    **kwargs,
) -> Component:
    """Array of straights connected with grating couplers.

    useful to align the 4 corners of the chip

    Args:
        n: number of straights.
        spacing: edge to edge straight spacing.
        straight: straight straight Component or library.
        kwargs: straight settings.
    """
    c = Component()
    #wg = gf.get_component(straight, length=0.48,**kwargs)
    # The above line should be defined inside the for loop after defining the parameter width_s

    for i in range(n):
        excel_file='apd_gc.xlsx'
        df=pd.read_excel(excel_file,sheet_name="RX",usecols="A")
        #width_s=np.linspace(1,2,4, endpoint=False, dtype=float)
        pert=df.at[i,'W']
        width_set= 0.35+1e-3*pert
        #print(width_set)
        wg = gf.get_component(straight, width=width_set, length=0.30,**kwargs)
        #print(straight_function.width)
        wref = c.add_ref(wg)
        #width_Set=0.2
        wref.x += i * (spacing + wg.info["length"])
        c.add_ports(wref.ports, prefix=str(i))

    c.auto_rename_ports()
    return c


if __name__ == "__main__":
    c = straight_array()
    # c.pprint_ports()
    c.show(show_ports=False)
