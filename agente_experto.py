import clips

class AgenteExperto:
    def __init__(self):
        self.env = clips.Environment()
        self._cargar_reglas()
    
    def _cargar_reglas(self):
        """Definición de reglas de negocio de un banco"""

        reglas = [
            '(defrule r1 (perfil perfil_solvente) (mora no) => (assert (resultado "CREDITO APROBADO: Cliente de bajo riesgo")))', # Regla 1: Cliente con perfil alto y sin mora
            '(defrule r2 (perfil perfil_riesgo) => (assert (resultado "CREDITO RECHAZADO: Riesgo financiero excesivo")))', # Regla 2: Cliente con perfil de riesgo (rechazo automático)
            '(defrule r3 (mora si) => (assert (resultado "CREDITO RECHAZADO: Reportado en centrales de riesgo")))', # Regla 3: Si tiene antecedentes de mora (rechazo por política)
            '(defrule r4 (perfil perfil_promedio) (mora no) => (assert (resultado "ESTUDIO MANUAL: Requiere avalista")))' # Regla 4: Perfil promedio sin mora (pasa a revisión humana)
        ]

        for regla in reglas:
            self.env.build(regla)
    
    def evaluar_caso(self, perfil_difuso, tiene_mora):
        """Recibir datos procesados y devuelve decisión del experto"""
        self.env.reset()

        self.env.assert_string(f"(perfil {perfil_difuso})")
        self.env.assert_string(f"(mora {'si' if tiene_mora else 'no'})")

        self.env.run()

        for f in self.env.facts():
            if f.template.name == 'resultado':
                return f[0]
        
        return "ERROR: No se pudo determinar un veredicto"


