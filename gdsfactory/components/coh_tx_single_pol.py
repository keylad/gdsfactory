from __future__ import annotations

from functools import partial
from typing import Optional

import gdsfactory as gf
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import select_ports
from gdsfactory.routing.get_route import get_route
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

default_mzm = dict(
    component="mzi",
    settings=dict(
        straight_x_top="straight_pin",
        cross_section_x_top="pin",
        delta_length=10.0,
    ),
)


@cell
def coh_tx_single_pol(
    balanced_phase_shifters: bool = False,
    mzm_y_spacing: float = 50.0,
    phase_shifter: ComponentSpec = "straight_pin",
    phase_shifter_length: float = 100.0,
    mzm_ps_spacing: float = 40.0,
    splitter: ComponentSpec = "mmi1x2",
    combiner: Optional[ComponentSpec] = None,
    mzm: ComponentSpec = default_mzm,
    mzm_length: float = 200.0,
    with_pads: bool = True,
    xspacing: float = 40.0,
    input_coupler: Optional[ComponentSpec] = None,
    output_coupler: Optional[ComponentSpec] = None,
    pad_array: ComponentSpec = "pad_array",
    cross_section: CrossSectionSpec = "strip",
    **kwargs,
) -> Component:
    """MZM-based single polarization coherent transmitter.

    Args:
        balanced_phase_shifters: True adds phase sifters after the MZM at both the I and Q arms.
            False, only adds Q arm has a phase shifter.
        mzm_y_spacing: vertical spacing between the bottom of the I MZM and the top of the Q MZM.
        phase_shifter: phase_shifter spec.
        phase_shifter_length: length of the phase shifter.
        mzm_ps_spacing: spacing between the end of the mzm and the phase shifter.
        splitter: splitter spec.
        combiner: combiner spec.
        mzm: Mach-Zehnder modulator spec.
        mzm_length: length of the MZMs.
        with_pads: if True, we draw pads for all the electrical contacts.
        xspacing: horizontal spacing between the splitter and combiner and the mzm.
        input_coupler: Optional coupler to add before the splitter.
        output_coupler: Optional coupler to add after the combiner.
        pad_array: array of pads spec.
        cross_section: for routing (splitter to mzms and mzms to combiners).
        kwargs: cross_section settings.

    .. code::

                                ___ mzm_i __ ps_i__
                                |                  |
                                |                  |
                                |                  |
       (in_coupler)---splitter==|                  |==combiner---(out_coupler)
                                |                  |
                                |                  |
                                |___ mzm_q __ ps_q_|
    """
    from gdsfactory.components.straight import straight as straight_function

    combiner = combiner or splitter
    pad_array = dict(component=pad_array, settings=dict(columns=1, rows=1))

    # ----- Draw MZIs -----
    c = Component()

    if with_pads:
        mzm_mod = gf.routing.add_electrical_pads_top(
            component=gf.get_component(mzm, length_x=mzm_length),
            direction="right",
            spacing=(-100, -136),
            select_ports=partial(select_ports, names=["e1", "e2"]),
            pad_array=pad_array,
        )
        mzm_mod_p = gf.routing.add_electrical_pads_top(
            component=mzm_mod,
            direction="right",
            spacing=(100, -250),
            select_ports=partial(select_ports, names=["e3", "e4"], clockwise=False),
            pad_array=pad_array,
        )
    else:
        mzm_mod_p = mzm(length_x=mzm_length)

    mzm_i = c << mzm_mod_p
    mzm_q = c << mzm_mod_p

    # Separate the two mzms so they don't overlap
    mzm_q.movey(mzm_i.ymin - mzm_y_spacing - mzm_q.ymax)

    # ------------ Phase shifter addition (for I/Q arm definition) ----------------

    phase_shifter = gf.get_component(phase_shifter, length=phase_shifter_length)

    if with_pads:
        ps_w_pads = gf.routing.add_electrical_pads_top(
            component=phase_shifter,
            direction="right",
            spacing=(50, -136),
            select_ports=partial(select_ports, names=["bot_e2", "top_e2"]),
            pad_array=pad_array,
        )
    else:
        ps_w_pads = phase_shifter

    if balanced_phase_shifters:
        ps_i = c << ps_w_pads
    else:
        # only the q arm has a phase shifter
        straight = straight_function(
            length=phase_shifter_length, cross_section=cross_section, **kwargs
        )
        ps_i = c << straight
    ps_q = c << ps_w_pads

    # Connect to the right ports
    if mzm_ps_spacing <= 0.0:
        ps_i.connect("o1", mzm_i.ports["o2"])
        ps_q.connect("o1", mzm_q.ports["o2"])
    else:
        straight_conn = straight_function(
            length=mzm_ps_spacing, cross_section=cross_section, **kwargs
        )
        straight_i = c << straight_conn
        straight_q = c << straight_conn
        straight_i.connect("o1", mzm_i.ports["o2"])
        straight_q.connect("o1", mzm_q.ports["o2"])
        ps_i.connect("o1", straight_i.ports["o2"])
        ps_q.connect("o1", straight_q.ports["o2"])

    # ------------ Splitters and combiners ---------------

    splitter = gf.get_component(splitter)
    sp = c << splitter
    sp.x = mzm_q.xmin - xspacing
    sp.y = (mzm_i.ports["o1"].y + mzm_q.ports["o1"].y) / 2

    route = get_route(
        sp.ports["o2"],
        mzm_i.ports["o1"],
        cross_section=cross_section,
        with_sbend=False,
        **kwargs,
    )
    c.add(route.references)

    route = get_route(
        sp.ports["o3"],
        mzm_q.ports["o1"],
        cross_section=cross_section,
        with_sbend=False,
        **kwargs,
    )
    c.add(route.references)

    combiner = gf.get_component(combiner)
    comb = c << combiner
    comb.mirror()

    comb.x = ps_q.xmax + xspacing
    comb.y = (mzm_i.ports["o2"].y + mzm_q.ports["o2"].y) / 2

    route = get_route(
        comb.ports["o2"],
        ps_i.ports["o2"],
        cross_section=cross_section,
        with_sbend=False,
        **kwargs,
    )
    c.add(route.references)

    route = get_route(
        comb.ports["o3"],
        ps_q.ports["o2"],
        cross_section=cross_section,
        with_sbend=False,
        **kwargs,
    )
    c.add(route.references)

    # ------- In and out couplers (if indicated) -----

    if input_coupler is not None:
        # Add input coupler
        in_coupler = gf.get_component(input_coupler)
        in_coup = c << in_coupler
        in_coup.connect("o1", sp.ports["o1"])

    else:
        c.add_port("o1", port=sp.ports["o1"])

    if output_coupler is not None:
        # Add output coupler
        output_coupler = gf.get_component(output_coupler)
        out_coup = c << output_coupler
        out_coup.connect("o1", comb.ports["o1"])
    else:
        c.add_port("o2", port=comb.ports["o1"])

    # ------ Extract electrical ports (if no pads) -------
    if not with_pads:
        c.add_ports(ps_i.get_ports_list(port_type="electrical"), prefix="ps_i")
        c.add_ports(ps_q.get_ports_list(port_type="electrical"), prefix="ps_q")
        c.add_ports(mzm_i.get_ports_list(port_type="electrical"), prefix="mzm_i")
        c.add_ports(mzm_q.get_ports_list(port_type="electrical"), prefix="mzm_q")
        c.auto_rename_ports()

    return c


if __name__ == "__main__":
    c = coh_tx_single_pol(with_pads=True)
    c.show(show_ports=True)
