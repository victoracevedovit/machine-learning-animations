from manim import *


class VideoSHAP20s(Scene):
    def construct(self):
        # --- 1. TITULO Y PRESENTACION (0-3 segundos) ---
        titulo = Text("¿Qué son los Valores SHAP?", font_size=36, color=BLUE_B)
        titulo.to_edge(UP, buff=0.5)
        self.play(Write(titulo))
        self.wait(1)

        # --- 2. LA FORMULA MATEMATICA (3-10 segundos) ---
        # Explicacion de la propiedad aditiva de SHAP de forma simplificada y academica
        subtitulo_formula = Text("Propiedad Aditiva (Explicación Local)", font_size=20, color=GRAY_A)
        subtitulo_formula.next_to(titulo, DOWN, buff=0.3)
        self.play(FadeIn(subtitulo_formula))

        # f(x) = g(z') = phi_0 + sum phi_i x_i
        formula = MathTex(
            r"f(x)", r"=", r"\phi_0", r"+", r"\sum_{i=1}^{M}", r"\phi_i", r"x_i",
            font_size=40
        )
        formula.move_to(UP * 0.5)

        # Coloreamos partes clave de la formula para la explicacion
        formula[0].set_color(YELLOW)   # f(x) - Prediccion
        formula[2].set_color(WHITE)    # phi_0 - Valor Base
        formula[5].set_color(GREEN_B)  # phi_i - Valor SHAP (Impacto)

        self.play(Write(formula), run_time=2)
        self.wait(2)

        # Breve desglose visual de la formula antes de ir al grafico
        lbl_pred = Text("f(x): Predicción Final", font_size=15, color=YELLOW)
        lbl_base = MathTex(r"\phi_0:\ \text{Valor Base}", font_size=28, color=WHITE)
        lbl_shap = MathTex(r"\phi_i:\ \text{Contribución}", font_size=28, color=GREEN_B)

        labels_formula = VGroup(lbl_pred, lbl_base, lbl_shap)
        labels_formula.arrange(RIGHT, buff=0.75)
        labels_formula.next_to(formula, DOWN, buff=0.55)

        self.play(
            LaggedStart(
                FadeIn(lbl_pred, shift=DOWN * 0.15),
                FadeIn(lbl_base, shift=DOWN * 0.15),
                FadeIn(lbl_shap, shift=DOWN * 0.15),
                lag_ratio=0.2
            )
        )
        self.wait(3)

        self.play(FadeOut(labels_formula), FadeOut(subtitulo_formula))

        # Movemos la formula arriba para que coexista con el ejemplo crediticio
        self.play(formula.animate.scale(0.7).to_edge(UP, buff=0.3), FadeOut(titulo))

        # --- 3. APLICACION AL CONTEXTO CREDITICIO (10-20 segundos) ---
        # Eje de probabilidad
        eje = NumberLine(x_range=[0, 100, 10], length=10, color=GRAY_C, include_numbers=True)
        eje.shift(DOWN * 1.5)
        eje_label = Text("Probabilidad de Aprobación de Crédito (%)", font_size=16, color=GRAY_B)
        eje_label.next_to(eje, DOWN, buff=0.5)
        self.play(Create(eje), FadeIn(eje_label))

        # Valor Base (phi_0 = 50%)
        val_base_x = eje.n2p(50)
        linea_base = Line(val_base_x + UP * 0.3, val_base_x + DOWN * 0.3, color=WHITE, stroke_width=4)
        txt_base = Text("Valor Base (50%)", font_size=14, color=WHITE).next_to(linea_base, UP, buff=0.1)
        self.play(Create(linea_base), FadeIn(txt_base))

        # Variable 1: Historial Crediticio (phi_1 = +30%)
        val_historial_x = eje.n2p(80)
        flecha_pos = Arrow(start=val_base_x, end=val_historial_x, color=GREEN_D, buff=0, stroke_width=5)
        flecha_pos.shift(UP * 0.4)
        txt_pos = Text("+30% Historial Crediticio", font_size=14, color=GREEN_B).next_to(flecha_pos, UP, buff=0.1)
        self.play(GrowArrow(flecha_pos), FadeIn(txt_pos))
        self.wait(1)

        # Variable 2: Deudas Elevadas (phi_2 = -15%)
        val_deudas_x = eje.n2p(65)
        flecha_neg = Arrow(start=val_historial_x, end=val_deudas_x, color=RED_D, buff=0, stroke_width=5)
        flecha_neg.shift(UP * 1.0)
        txt_neg = Text("-15% Deudas Altas", font_size=14, color=RED_B).next_to(flecha_neg, UP, buff=0.1)
        self.play(GrowArrow(flecha_neg), FadeIn(txt_neg))
        self.wait(1)

        # Prediccion Final (f(x) = 65%)
        linea_final = Line(val_deudas_x + UP * 0.4, val_deudas_x + DOWN * 0.4, color=YELLOW, stroke_width=5)
        txt_final = Text("Predicción: 65%", font_size=18, color=YELLOW, weight=BOLD).next_to(linea_final, DOWN, buff=0.3)

        self.play(Create(linea_final))
        self.play(Indicate(txt_final, color=YELLOW), FadeIn(txt_final))

        # Pausa final para completar los 20 segundos totales de video
        self.wait(3.5)
