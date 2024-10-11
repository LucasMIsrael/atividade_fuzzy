import numpy as np
import skfuzzy as fuzz 
from skfuzzy import control as ctrl 

#variaveis fuzzy - qualidade da refeição, qualidade do serviço e tempo de atendimento
comida = ctrl.Antecedent(np.arange(0, 11, 1), 'comida')
servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
tempo = ctrl.Antecedent(np.arange(0, 31, 1), 'tempo')

gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')

comida['insossa'] = fuzz.trimf(comida.universe, [0, 0, 5])
comida['saborosa'] = fuzz.trimf(comida.universe, [5, 10, 10])

servico['ruim'] = fuzz.trimf(servico.universe, [0, 0, 5])
servico['excelente'] = fuzz.trimf(servico.universe, [5, 10, 10])

tempo['demorado'] = fuzz.trimf(tempo.universe, [20, 30, 30])
tempo['mediano'] = fuzz.trimf(tempo.universe, [10, 20, 30])
tempo['rapido'] = fuzz.trimf(tempo.universe, [0, 0, 10])

gorjeta['nenhuma'] = fuzz.trimf(gorjeta.universe, [0, 0, 5])
gorjeta['pouca'] = fuzz.trimf(gorjeta.universe, [0, 5, 10])
gorjeta['generosa'] = fuzz.trimf(gorjeta.universe, [10, 20, 25])

rule1 = ctrl.Rule(comida['insossa'] & servico['ruim'], gorjeta['pouca'])
rule2 = ctrl.Rule(comida['saborosa'] & servico['excelente'], gorjeta['generosa'])
rule3 = ctrl.Rule(tempo['demorado'], gorjeta['nenhuma'])
rule4 = ctrl.Rule((tempo['mediano'] | tempo['rapido']) & (comida['saborosa'] | servico['excelente']), gorjeta['generosa'])

sistema_gorjeta = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
simulador = ctrl.ControlSystemSimulation(sistema_gorjeta)

#entrada
simulador.input['comida'] = 8  
simulador.input['servico'] = 9 
simulador.input['tempo'] = 12 

simulador.compute()

print(f"Gorjeta: {simulador.output['gorjeta']:.2f}%")