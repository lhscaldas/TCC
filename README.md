# Controle de um Navio Autônomo para Contramedidas de Minagem Utilizando o MOOS-IvP

Repositório dedicado aos códigos implementados para minha monografia do curso de Engenharia Mecatrônica da Escola politécnica da Universidade de São Paulo.

O controlador foi implementado utilizando a arquitetura do MOOS-IvP, framework de controle de navios autônomos desenvolvido em parceria pelo MIT e pela Universidade de Oxford. O controlador de rumo e trajetória é do tipo PID.

Para a configuração do controlador para diferentes missões foi implementada uma interface gráfica (GUI) em Python utilizando a biblioteca tkinter. Nesta interface gráfica foi implementado também um otimizador de rotas que utiliza um Algorótimo Genético para gerar uma rota entre dois pontos de forma que o caminho seja o menor possível sem colidir com obstáculos.

Para validação do controlador foi implementada uma interface com a biblioteca Pydyna, utilizada pelo Tanque de Provas Numérico da Universidade de São Paulo para a simulação da dinâmica de navios. Além disso também foi implementado um módulo para interface entre o controlador e o Simulador de Manobras Hidrodinâmico (SMH) do TPN, de forma a realizar simulações com visualização em 3D neste simulador. 


