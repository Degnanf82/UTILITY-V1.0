# ------------------------------------------------------------------ armado de la pagina
CSS_EXTRA = """
.figs { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }
.fig svg.p { min-width: 0; }
.fig h3 { padding: 12px 16px 0; color: var(--fg); font-size: 17px; }
.lead { fill: none; stroke-width: 3; stroke-linejoin: round; }
.l-v33 { stroke: var(--v33); } .l-gnd { stroke: var(--gnd); } .l-sda { stroke: var(--sda); } .l-scl { stroke: var(--scl); }
.l-ana { stroke: var(--ana); } .l-btn { stroke: var(--btn); } .l-gray { stroke: var(--muted); } .l-none { stroke: var(--muted); stroke-dasharray: 3 4; }
.chip rect { stroke-width: 1.5; }
.chip text { font-size: 11.5px; font-weight: 700; }
.c-v33 rect { fill: var(--v33); stroke: var(--v33); } .c-v33 text { fill: #fff; }
.c-gnd rect { fill: #1d2421; stroke: var(--ink); } .c-gnd text { fill: #fff; }
.c-sda rect { fill: var(--sda); stroke: var(--sda); } .c-sda text { fill: #241a00; }
.c-scl rect { fill: var(--scl); stroke: var(--scl); } .c-scl text { fill: #fff; }
.c-ana rect { fill: var(--panel); stroke: var(--ana); } .c-ana text { fill: var(--ana); }
.c-btn rect { fill: var(--panel); stroke: var(--btn); } .c-btn text { fill: var(--btn); }
.c-gray rect { fill: var(--panel); stroke: var(--muted); } .c-gray text { fill: var(--muted); }
.c-none rect { fill: var(--panel); stroke: var(--muted); stroke-dasharray: 3 3; } .c-none text { fill: var(--muted); font-weight: 500; }
.c-esp rect { fill: var(--esp); stroke: var(--esp); } .c-esp text { fill: #fff; }
.c-ads rect { fill: var(--mod); stroke: var(--mod); } .c-ads text { fill: #fff; }
.w-lead { stroke: var(--lead); stroke-width: 3; }
.w-strip { stroke: var(--ana); stroke-width: 8; }
.w-btn { stroke: var(--btn); }
.d-btn { fill: var(--btn); }
.rbody { fill: #e7cf9f; stroke: #a88b55; stroke-width: 1; }
.rbig { fill: #f2f1ec; stroke: #9c9a92; stroke-width: 1.2; }
.rbig-t { fill: #3a3a36; font-size: 11px; font-weight: 700; }
.dbody { fill: #202326; stroke: #000; stroke-width: .8; }
.dband { fill: #d8dbe0; }
.jack-hole { fill: #0a0a0a; }
.fglass { fill: #dcedf5; stroke: #8fb3c4; stroke-width: 1.2; }
.fcap { fill: #b8bcc2; stroke: #8a8e94; stroke-width: 1; }
.fwire { stroke: #6b6f75; stroke-width: 1.5; }
.btn { fill: #2b2f33; stroke: #111; } .btn-cap { fill: #d9dde2; stroke: #8a8e94; }
.buzz { fill: #1e2023; stroke: #000; } .buzz-h { fill: #55595e; }
.to92 { fill: #1e2023; stroke: #000; }
.cables td.n { font: 700 14px var(--f-mono); color: var(--muted); width: 2.5em; }
.sw { display: inline-block; width: 14px; height: 14px; border-radius: 3px; vertical-align: -2px; margin-right: 6px; border: 1px solid var(--rule); }
details.tech { background: var(--panel); border: 1px solid var(--rule); border-radius: 10px; padding: 12px 16px; }
details.tech summary { cursor: pointer; font-family: var(--f-head); font-size: 18px; font-weight: 700; }
details.tech[open] summary { margin-bottom: 12px; }
details.tech .fig { margin-top: 12px; }
"""

