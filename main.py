from agente_experto import AgenteExperto

class SistemaFinanciero:
    def __init__(self):
        self.experto = AgenteExperto()

    def obtener_perfil_difuso(self, salario, gastos):
        disponible = salario - gastos
        if disponible > 3500:
            return "perfil_solvente"
        elif disponible > 1500:
            return "perfil_promedio"
        else:
            return "perfil_riesgo"
        
    def ejecutar(self):
        print("="*40)
        print(" SISTEMA INTELIGENTE DE RIESGO BANCARIO")
        print("="*40)

        try:
            # Entrada de datos por consola
            nombre = input("Nombre del solicitante: ")
            salario = float(input("Ingresos mensuales: "))
            gastos = float(input("Gastos/Deudas mensuales: "))
            mora = input("¿Aparece en lista de morosos? (s/n): ").lower() == 's'

            # Obtener perfil.
            perfil = self.obtener_perfil_difuso(salario, gastos)

            # Consultar agente experto.
            decision = self.experto.evaluar_caso(perfil, mora)

            # Salida de resultados.
            print("\n" + "-"*30)
            print(f"DIAGNÓSTICO PARA: {nombre}")
            print(f"PERFIL CALCULADO: {perfil.upper()}")
            print(f"DECISIÓN FINAL: {decision}")
            print("-"*30)
        
        except ValueError:
            print("\nERROR: Ingrese valores válidos.")

if __name__ == "__main__":
    app = SistemaFinanciero()
    app.ejecutar()