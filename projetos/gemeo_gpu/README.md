# Gêmeo Digital Térmico - GPU de Inferência de IA

Projeto acadêmico de Fundamentos de Engenharia.

## Caso analisado
- Referência: NVIDIA L4
- Potência térmica: 72 W
- Temperatura ambiente nominal: 25 °C
- Limite térmico de projeto: 80 °C
- Dissipador: Alumínio 6061, 170 x 70 x 5 mm, 12 aletas de 170 x 2 x 25 mm
- Resfriamento de projeto: ventilação forçada, h = 40 W/m².K

## Principais resultados
- Tmax com h = 40 W/m².K: 41,7 °C
- Tmax com h = 10 W/m².K: 84,2 °C
- Conclusão: fluxo de ar forçado é necessário para margem térmica confortável.

## Estrutura
- relatorio/: PDF final
- cad/: STEP, STL e script para gerar FCStd no FreeCAD
- simulacao/: notebook e CSV
