import cadquery as cq
from cadquery import exporters
from pathlib import Path
import math, os, json

OUT=Path('/mnt/data/cad_gemeo_gpu_evoluido')
OUT.mkdir(exist_ok=True)

# =========================
# Parameters
# =========================
L=170.0; W=70.0; BASE=5.0
FIN_H=25.0; FIN_T=2.0; NFIN=12
PCB_L=169.4; PCB_W=68.8; PCB_T=1.6
FAN_L=60.0; FAN_W=60.0; FAN_T=10.0
FAN_CENTERS=[50.0,120.0]
DUCT_H=12.0
M3_CLEAR=3.4
# Conceptual mounting pattern (NOT an official L4 PCB hole pattern)
HOLES=[(10,10),(160,10),(10,60),(160,60)]
# Central thermal contact patch (conceptual envelope)
CONTACT_L=90.0; CONTACT_W=50.0

# -------------------------
# Heatsink
# -------------------------
base=cq.Workplane('XY').box(L,W,BASE, centered=(False,False,False))
# four conceptual mounting holes through base
for x,y in HOLES:
    base=base.cut(cq.Workplane('XY').center(x,y).circle(M3_CLEAR/2).extrude(BASE))
# thermal contact pocket/marking: shallow 0.15 mm recess, conceptual
# leave as solid flat base for fabrication robustness

# equal margins and gaps: 3 mm margin, equal gaps
margin=3.0
gap=(W-2*margin-NFIN*FIN_T)/(NFIN+1)
ys=[]
for i in range(NFIN):
    y=margin+gap*(i+1)+FIN_T*i+FIN_T/2
    ys.append(y)
    fin=cq.Workplane('XY').center(L/2,y).box(L,FIN_T,FIN_H, centered=(True,True,False)).translate((0,0,BASE))
    base=base.union(fin)
heatsink=base

# -------------------------
# GPU reference board/envelope
# -------------------------
pcb=cq.Workplane('XY').box(PCB_L,PCB_W,PCB_T, centered=(False,False,False))
# approximate edge connector tongue, visual only
connector=cq.Workplane('XY').box(90,8,0.15, centered=(False,False,False)).translate((10,-0.2,PCB_T))
pcb=pcb.union(connector)
# conceptual GPU package and memory blocks, not manufacturer geometry
pkg=cq.Workplane('XY').box(50,50,3.0, centered=(False,False,False)).translate(((PCB_L-50)/2,(PCB_W-50)/2,PCB_T))
# 8 memory blocks around package, conceptual
mems=[]
for x,y in [(35,8),(67,8),(99,8),(35,53),(67,53),(99,53),(8,22),(128,22)]:
    m=cq.Workplane('XY').box(18,10,2.0, centered=(False,False,False)).translate((x,y,PCB_T))
    mems.append(m)
gpu=pkg
for m in mems: gpu=gpu.union(m)
gpu_assembly=pcb.union(gpu)

# -------------------------
# Thermal interface layer
# -------------------------
tim=cq.Workplane('XY').box(CONTACT_L,CONTACT_W,0.5, centered=(False,False,False)).translate(((L-CONTACT_L)/2,(W-CONTACT_W)/2,PCB_T+3.0))
# Note: visual/assembly layer; contact is aligned under heatsink base in assembled view.

# -------------------------
# Fan model: simplified housing + rotor + blades
# -------------------------
def fan(cx):
    # centered at x,y; z starts at top of fins
    z=BASE+FIN_H
    housing=cq.Workplane('XY').box(FAN_L,FAN_W,FAN_T, centered=(True,True,False)).translate((cx,W/2,z))
    housing=housing.cut(cq.Workplane('XY').center(cx,W/2).circle(26).extrude(FAN_T).translate((0,0,z)))
    hub=cq.Workplane('XY').center(cx,W/2).circle(9).extrude(FAN_T).translate((0,0,z))
    rotor=hub
    # 7 simplified radial blades, swept rectangles
    for i in range(7):
        a=math.radians(i*360/7)
        blade=cq.Workplane('XY').box(20,5,2, centered=(False,True,False))
        blade=blade.translate((cx+7*math.cos(a),W/2+7*math.sin(a),z+4)).rotate((cx,W/2,z),(cx,W/2,z+1),i*360/7)
        rotor=rotor.union(blade)
    return housing.union(rotor)

fans=[fan(c) for c in FAN_CENTERS]
fan_assembly=fans[0].union(fans[1])

# -------------------------
# Duct / shroud: top plate + perimeter walls, two fan openings
# -------------------------
z0=BASE+FIN_H+FAN_T
duct=cq.Workplane('XY').box(L,W,DUCT_H, centered=(False,False,False)).translate((0,0,z0))
# two circular openings
for cx in FAN_CENTERS:
    opening=cq.Workplane('XY').center(cx,W/2).circle(27).extrude(DUCT_H)
    duct=duct.cut(opening.translate((0,0,z0)))
# inlet grill ribs (conceptual)
for x in range(8,163,8):
    rib=cq.Workplane('XY').box(2,W,2, centered=(False,False,False)).translate((x,0,z0+DUCT_H-2))
    # only outside the openings is guaranteed; keep ribs as decorative top grille
    # avoid merging into circular openings by using the whole plate minus openings already
    duct=duct.union(rib.cut(cq.Workplane('XY').box(0.1,0.1,0.1)))

# -------------------------
# Mounting standoffs + screws, conceptual M3
# -------------------------
mounts=None
for x,y in HOLES:
    st=cq.Workplane('XY').center(x,y).circle(4.5).circle(1.7).extrude(8).translate((0,0,PCB_T+3.0))
    # screw head + shaft visual
    sh=cq.Workplane('XY').center(x,y).circle(1.45).extrude(12).translate((0,0,PCB_T+3.0))
    hd=cq.Workplane('XY').center(x,y).circle(3.0).extrude(1.8).translate((0,0,PCB_T+14.0))
    part=st.union(sh).union(hd)
    mounts=part if mounts is None else mounts.union(part)

# -------------------------
# Bracket / backplate conceptual low-profile bracket
# -------------------------
bracket=cq.Workplane('XZ').box(20,2,58, centered=(False,False,False)).translate((0,-2,0))
# two port cutouts (conceptual)
bracket=bracket.cut(cq.Workplane('XZ').center(10,42).rect(14,12).extrude(2).translate((0,-2,0)))
bracket=bracket.cut(cq.Workplane('XZ').center(10,22).rect(14,12).extrude(2).translate((0,-2,0)))

# -------------------------
# Full assembly
# -------------------------
# Align heatsink over board, board at z=0, heatsink base at z=PCB_T+3.5
hs_assembled=heatsink.translate((0,0,PCB_T+3.5))
full=gpu_assembly.union(hs_assembled).union(fan_assembly).union(duct).union(mounts)

# -------------------------
# Exports
# -------------------------
def exp(obj, name):
    exporters.export(obj, str(OUT/(name+'.step')))
    exporters.export(obj, str(OUT/(name+'.stl')), tolerance=0.05, angularTolerance=0.2)

exp(heatsink,'01_dissipador_al6061')
exp(gpu_assembly,'02_gpu_referencia_l4_envelope')
exp(fan_assembly,'03_duas_ventoinhas_60mm')
exp(duct,'04_carenagem_duto')
exp(mounts,'05_fixacao_conceitual_m3')
exp(full,'06_conjunto_completo')

# Also export the base-only version and a combined thermal stack
thermal_stack=hs_assembled.union(gpu_assembly).union(tim)
exp(thermal_stack,'07_stack_gpu_tim_dissipador')

# JSON parameter manifest
manifest={
 'source_basis':'Projeto Gêmeo Digital Térmico de Hardware Computacional',
 'official_reference': 'NVIDIA L4: 6.67 in x 2.71 in, 1-slot low-profile, 72 W TDP',
 'report_dimensions': {'base_mm':[170,70,5],'fins':12,'fin_mm':[170,2,25],'total_height_mm':30},
 'added_design_hypotheses': {
   'pcb_mm':[PCB_L,PCB_W,PCB_T],
   'fans':'2 x 60 x 60 x 10 mm axial conceptual models',
   'mounting':'4 x M3 clearance holes, 3.4 mm, conceptual pattern; not an official NVIDIA L4 PCB mounting pattern',
   'thermal_contact_mm':[CONTACT_L,CONTACT_W,0.5],
   'duct_height_mm':DUCT_H
 },
 'fin_gap_mm':round(gap,3),
 'coordinate_system':'X length, Y width, Z height',
}
(OUT/'PARAMETROS.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))

# Parametric script copy
script=Path('/mnt/data/build_cad.py').read_text()
(OUT/'gerar_modelo_cad_parametrico.py').write_text(script)

# README
readme = """GÊMEO DIGITAL TÉRMICO — PACOTE CAD EVOLUÍDO

Base do modelo:
- Dissipador do relatório: 170 x 70 x 5 mm, 12 aletas, 25 mm de altura, Al 6061.
- Referência NVIDIA L4: 6,67 x 2,71 pol., formato 1-slot low-profile, TDP 72 W.

Arquivos:
01_dissipador_al6061: dissipador isolado.
02_gpu_referencia_l4_envelope: PCB/envelope conceitual + componentes simplificados.
03_duas_ventoinhas_60mm: duas ventoinhas axiais simplificadas.
04_carenagem_duto: carenagem superior com duas entradas.
05_fixacao_conceitual_m3: elementos de fixação.
06_conjunto_completo: conjunto integrado.
07_stack_gpu_tim_dissipador: pilha térmica.
PARAMETROS.json: parâmetros e hipóteses.
gerar_modelo_cad_parametrico.py: geração paramétrica via CadQuery.

IMPORTANTE:
As dimensões da L4 foram usadas apenas como envelope de referência. A NVIDIA não fornece no material consultado o padrão de furos da PCB necessário para validar a fixação. Portanto, os quatro furos M3, a posição do GPU/package, memórias, ventiladores e carenagem são HIPÓTESES DE PROJETO e não devem ser usados para fabricação de uma L4 real sem desenho mecânico oficial.

O modelo é apropriado para estudo acadêmico, visualização, montagem conceitual, simulação preliminar e evolução para CAD de engenharia.
"""
(OUT/'README.md').write_text(readme,encoding='utf-8')

print('Generated', OUT)
for p in sorted(OUT.iterdir()): print(p.name, p.stat().st_size)
