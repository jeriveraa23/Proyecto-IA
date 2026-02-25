import customtkinter as ctk
from motor_difuso import MotorDifuso
from agente_experto import AgenteExperto

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VentanaBancaria(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analizador de Crédito")
        self.geometry("600x650")

        self.motor_difuso   = MotorDifuso()
        self.agente_experto = AgenteExperto()

        self.grid_columnconfigure(0, weight=1)

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="ANÁLISIS DE CRÉDITO INTELIGENTE", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=25)

        # Frame de entrada
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(pady=10, padx=20, fill="x")

        # Campo nombre
        self.entry_nombre = ctk.CTkEntry(self.frame_input, placeholder_text="Nombre completo del solicitante", height=40)
        self.entry_nombre.pack(pady=10, padx=20, fill="x")

        # Slider ingresos
        self.label_ing = ctk.CTkLabel(self.frame_input, text="Nivel de Ingresos Mensuales (0-10)")
        self.label_ing.pack()
        
        # Variable para mostrar el número
        self.string_ing = ctk.StringVar(value="5") 
        self.frame_ing_row = ctk.CTkFrame(self.frame_input, fg_color="transparent")
        self.frame_ing_row.pack(fill="x", padx=20)

        self.slider_ing = ctk.CTkSlider(self.frame_ing_row, from_=0, to=10, number_of_steps=10,
                                        command=lambda v: self.string_ing.set(str(int(v))))
        self.slider_ing.pack(side="left", expand=True, fill="x")
        
        self.val_ing_label = ctk.CTkLabel(self.frame_ing_row, textvariable=self.string_ing, width=30)
        self.val_ing_label.pack(side="right", padx=5)


        # --- Slider Estabilidad ---
        self.label_est = ctk.CTkLabel(self.frame_input, text="Años de Estabilidad Laboral (0-10)")
        self.label_est.pack()

        # Variable para mostrar el número
        self.string_est = ctk.StringVar(value="5")
        self.frame_est_row = ctk.CTkFrame(self.frame_input, fg_color="transparent")
        self.frame_est_row.pack(fill="x", padx=20)

        self.slider_est = ctk.CTkSlider(self.frame_est_row, from_=0, to=10, number_of_steps=10,
                                        command=lambda v: self.string_est.set(str(int(v))))
        self.slider_est.pack(side="left", expand=True, fill="x")

        self.val_est_label = ctk.CTkLabel(self.frame_est_row, textvariable=self.string_est, width=30)
        self.val_est_label.pack(side="right", padx=5)

        # Switch mora
        self.switch_mora = ctk.CTkSwitch(self.frame_input, text="Reporte en centrales de riesgo (mora)")
        self.switch_mora.pack(pady=15)

        # Botón de acción
        self.btn_evaluar = ctk.CTkButton(self, text="CALCULAR DIAGNÓSTICO", font=("Roboto", 16, "bold"), height=45, command=self.procesar_solicitud)
        self.btn_evaluar.pack(pady=20)

        # Área de resultado
        self.text_resultado = ctk.CTkTextbox(self, width=500, height=200, font=("Consolas", 14))
        self.text_resultado.pack(pady=10, padx=20)

    def procesar_solicitud(self):
        try:
            nombre = self.entry_nombre.get()
            if not nombre:
                nombre = "Usuario Anónimo"
            
            # Obtener valores de la interfaz
            val_ing    = self.slider_ing.get()
            val_est    = self.slider_est.get()
            tiene_mora = self.switch_mora.get() == 1

            # Ejecutar motor difuso
            perfil, score = self.motor_difuso.calcular_perfil(val_ing, val_est)

            # Ejecutar agente experto (CLIPS)
            veredicto = self.agente_experto.evaluar_caso(perfil, tiene_mora)

            self.text_resultado.delete("0.0", "end")
            resultado_formateado = (
                f"RESUMEN DE EVALUACIÓN\n"
                f"{'='*30}\n"
                f"SOLICITANTE: {nombre.upper()}\n"
                f"SCORE DIFUSO: {score:.1f} /100\n"
                f"PERFIL CALCULADO: {perfil.upper()}\n"
                f"ESTADO MORA: {'SI' if tiene_mora else 'NO'}\n"
                f"{'='*30}\n"
                f"DECISIÓN FINAL:\n{veredicto}"
            )
            self.text_resultado.insert("0.0", resultado_formateado)

        except Exception as e:
            self.text_resultado.insert("0.0", f"Error en el proceso: {e}")

if __name__ == "__main__":
    app = VentanaBancaria()
    app.mainloop()

