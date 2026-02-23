from agente_experto import AgenteExperto
from motor_difuso import MotorDifuso

class SistemaFinanciero:
    def __init__(self):
        self.experto = AgenteExperto()
        self.difuso  = MotorDifuso()
        
    def ejecutar(self):
        print("="*40)
        print(" SISTEMA INTELIGENTE DE RIESGO BANCARIO")
        print("="*40)

        try:
            # Entrada de datos por consola
            nombre = input("Nombre del solicitante: ")
            salario = float(input("Nivel de ingresos (0-10): "))
            estabilidad = float(input("Años estabilidad laboral (0-10): "))
            mora = input("¿Aparece en lista de morosos? (s/n): ").lower() == 's'

            # Obtenemos perfil con LD
            perfil, score_num = self.difuso.calcular_perfil(salario, estabilidad)

            # Consultar agente experto.
            decision = self.experto.evaluar_caso(perfil, mora)


            # Salida de resultados.
            print("\n" + "-"*30)
            print(f"DIAGNÓSTICO PARA: {nombre}")
            print(f"SCORE DIFUSO: {score_num:.2f}/100")
            print(f"CATEGORÍA {perfil.upper()}")
            print(f"DECISIÓN FINAL: {decision}")
            print("-"*30)
        
        except Exception as e:
            print(f"\nERROR REAL: {e}")

if __name__ == "__main__":
    app = SistemaFinanciero()
    app.ejecutar()