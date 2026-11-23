# spec: heroes.py
Write a NEW file /root/newsimg23-entry/heroes.py (do not read or edit other files).
It must define one function:

    def draw_scene(d, scene, x0, y0, w, h, PAL)

`d` is a PIL ImageDraw, `PAL` a dict with keys PAPER, PAPER2, INK, NAVY, RED, TEAL, AMBER, GREY.
Draw flat vector newspaper illustrations, no text except a short banner, no randomness,
no network, no imports beyond what is given.

Scenes:
- "smoke": failed UN climate plenary. Horseshoe delegates table, 10 head circles around it,
  a podium block, a navy banner with amber 'COP31' letters at the top, a gavel at right.
- "rubble": collapsed apartment block. Angled fallen slab with two rows of small windows,
  a standing broken tower, 3 rescuers (one with a white square bearing a red cross),
  12 scattered debris blocks, dust haze band at the bottom.
- "ship": burning naval ship at a naval base. Dark navy hull, white superstructure block,
  two grey smoke plumes, orange/red flame shapes, water band with wave arcs, and a small
  dark drone boat with an antenna mast approaching from the right.

Each scene fills the rect (x0,y0,w,h) with PAL['PAPER2'] background, keeps 8px padding,
and stays deterministic. Keep it about 120 lines. Run `python3 -c "import heroes"` to check syntax.
