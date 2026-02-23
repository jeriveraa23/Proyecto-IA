import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class MotorDifuso:
    def __init__(self):
        # Antecedentes: Escala 1 a 10
        self.ingresos    = ctrl.Antecedent(np.arange(0,11,1), 'ingresos')
        self.estabilidad = ctrl.Antecedent(np.arange(0,11,1), 'estabilidad')

        #Consecuente: Score de 0 a 100
        self.score = ctrl.Consequent(np.arange(0,101,1), 'score')


        #MF Ingresos
        self.ingresos['bajo']  = fuzz.trapmf(self.ingresos.universe, [0, 0, 3, 5])
        self.ingresos['medio'] = fuzz.trapmf(self.ingresos.universe, [4, 5, 7, 8])
        self.ingresos['alto']  = fuzz.trapmf(self.ingresos.universe, [7, 9, 10, 10])

        #MF Estabilidad
        self.estabilidad['pobre']     = fuzz.trapmf(self.estabilidad.universe, [0, 0, 2, 4])
        self.estabilidad['buena']     = fuzz.trapmf(self.estabilidad.universe, [3, 5, 7, 8])
        self.estabilidad['excelente'] = fuzz.trapmf(self.estabilidad.universe, [7, 9, 10, 10])

        #MF Score
        self.score['riesgo']   = fuzz.trimf(self.score.universe, [0, 0, 45])
        self.score['promedio'] = fuzz.trimf(self.score.universe, [35, 60, 85])
        self.score['solvente'] = fuzz.trimf(self.score.universe, [75, 100, 100])

        #Regla Difusas
        r1 = ctrl.Rule(self.ingresos['bajo'] & self.estabilidad['pobre'], self.score['riesgo'])
        r2 = ctrl.Rule(self.ingresos['bajo'] & self.estabilidad['buena'], self.score['riesgo'])
        r3 = ctrl.Rule(self.ingresos['medio'] & self.estabilidad['pobre'], self.score['riesgo'])

        r4 = ctrl.Rule(self.ingresos['bajo'] & self.estabilidad['excelente'], self.score['promedio'])
        r5 = ctrl.Rule(self.ingresos['medio'] & self.estabilidad['buena'], self.score['promedio'])
        r6 = ctrl.Rule(self.ingresos['alto'] & self.estabilidad['pobre'], self.score['promedio'])
        
        r7 = ctrl.Rule(self.ingresos['medio'] & self.estabilidad['excelente'], self.score['solvente'])
        r8 = ctrl.Rule(self.ingresos['alto'] & self.estabilidad['buena'], self.score['solvente'])
        r9 = ctrl.Rule(self.ingresos['alto'] & self.estabilidad['excelente'], self.score['solvente'])

        self.control_financiero = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9])
        self.simulador = ctrl.ControlSystemSimulation(self.control_financiero)

    def calcular_perfil(self, valor_ingresos, valor_estabilidad):
        """Calcula el score y devuelve valor para CLIPS"""
        self.simulador.input['ingresos']    = valor_ingresos
        self.simulador.input['estabilidad'] = valor_estabilidad

        try:
            self.simulador.compute()
            puntos = self.simulador.output['score']
        except:
            puntos = 0

        if puntos >= 75:
            return "perfil_solvente", puntos
        elif puntos >= 45:
            return "perfil_promedio", puntos
        else:
            return "perfil_riesgo", puntos