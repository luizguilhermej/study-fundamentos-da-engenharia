GÊMEO DIGITAL TÉRMICO — PACOTE CAD EVOLUÍDO

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
