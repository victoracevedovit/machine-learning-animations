from pathlib import Path

from manim import *


ASSET_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSET_DIR / "cerebroDatabankHorizontal.png"
AUDIO_PATH = ASSET_DIR / "narracion_shap.aiff"


class VideoSHAP20s(Scene):
    def construct(self):
        self.camera.background_color = "#17051f"

        if AUDIO_PATH.exists():
            self.add_sound(str(AUDIO_PATH), gain=-3)

        # --- 1. INTRO DATABANK ACADEMY ---
        bg = FullScreenRectangle(fill_color="#17051f", fill_opacity=1, stroke_width=0)
        self.add(bg)

        logo = ImageMobject(str(LOGO_PATH))
        logo.set_width(7.5)
        logo.move_to(ORIGIN)

        halo = Circle(radius=2.25, color="#f7a33a", stroke_width=2)
        halo.set_opacity(0.0)
        halo.move_to(LEFT * 2.6)

        linea = Line(LEFT * 4.0, RIGHT * 4.0, color="#f7a33a", stroke_width=2)
        linea.next_to(logo, DOWN, buff=0.35)
        linea.set_opacity(0.0)

        self.play(
            FadeIn(logo, shift=UP * 0.15),
            halo.animate.set_opacity(0.35),
            run_time=1.6,
        )
        self.play(
            logo.animate.scale(1.04),
            halo.animate.scale(1.08).set_opacity(0.12),
            linea.animate.set_opacity(0.85),
            run_time=1.2,
        )
        self.wait(0.4)
        self.play(
            FadeOut(logo, shift=UP * 0.2),
            FadeOut(halo),
            FadeOut(linea),
            run_time=0.9,
        )

        # --- 2. TITULO Y PRESENTACION ---
        titulo = Text("¿Qué son los Valores SHAP?", font_size=38, color=BLUE_B)
        titulo.to_edge(UP, buff=0.55)
        subtitulo = Text(
            "Explicaciones locales para modelos de machine learning",
            font_size=20,
            color=GRAY_A,
        )
        subtitulo.next_to(titulo, DOWN, buff=0.25)

        self.play(Write(titulo), FadeIn(subtitulo, shift=DOWN * 0.15), run_time=1.5)
        self.wait(1.0)

        # --- 3. LA FORMULA MATEMATICA ---
        subtitulo_formula = Text("Propiedad Aditiva", font_size=22, color=GRAY_A)
        subtitulo_formula.next_to(subtitulo, DOWN, buff=0.45)
        self.play(FadeIn(subtitulo_formula))

        formula = MathTex(
            r"f(x)", r"=", r"\phi_0", r"+", r"\sum_{i=1}^{M}", r"\phi_i", r"x_i",
            font_size=42,
        )
        formula.move_to(UP * 0.15)

        formula[0].set_color(YELLOW)   # f(x) - Prediccion
        formula[2].set_color(WHITE)    # phi_0 - Valor Base
        formula[5].set_color(GREEN_B)  # phi_i - Valor SHAP

        self.play(Write(formula), run_time=2.0)
        self.wait(1.0)

        lbl_pred = Text("Predicción final", font_size=16, color=YELLOW)
        lbl_base = MathTex(r"\phi_0:\ \text{valor base}", font_size=28, color=WHITE)
        lbl_shap = MathTex(r"\phi_i:\ \text{impacto de cada variable}", font_size=28, color=GREEN_B)

        labels_formula = VGroup(lbl_pred, lbl_base, lbl_shap)
        labels_formula.arrange(RIGHT, buff=0.55)
        labels_formula.next_to(formula, DOWN, buff=0.55)

        self.play(
            LaggedStart(
                FadeIn(lbl_pred, shift=DOWN * 0.15),
                FadeIn(lbl_base, shift=DOWN * 0.15),
                FadeIn(lbl_shap, shift=DOWN * 0.15),
                lag_ratio=0.2,
            ),
            run_time=1.6,
        )
        self.wait(2.0)

        self.play(
            FadeOut(labels_formula),
            FadeOut(subtitulo_formula),
            FadeOut(subtitulo),
            formula.animate.scale(0.68).to_edge(UP, buff=0.35),
            titulo.animate.scale(0.72).to_corner(UL, buff=0.35),
            run_time=1.2,
        )

        # --- 4. APLICACION AL CONTEXTO CREDITICIO ---
        eje = NumberLine(
            x_range=[0, 100, 10],
            length=10,
            color=GRAY_C,
            include_numbers=True,
            font_size=22,
        )
        eje.shift(DOWN * 1.45)
        eje_label = Text("Probabilidad de Aprobación de Crédito (%)", font_size=18, color=GRAY_B)
        eje_label.next_to(eje, DOWN, buff=0.45)
        self.play(Create(eje), FadeIn(eje_label), run_time=1.2)

        val_base_x = eje.n2p(50)
        linea_base = Line(val_base_x + UP * 0.35, val_base_x + DOWN * 0.35, color=WHITE, stroke_width=4)
        txt_base = Text("Valor Base: 50%", font_size=16, color=WHITE).next_to(linea_base, UP, buff=0.15)
        self.play(Create(linea_base), FadeIn(txt_base), run_time=1.1)
        self.wait(0.4)

        val_historial_x = eje.n2p(80)
        flecha_pos = Arrow(start=val_base_x, end=val_historial_x, color=GREEN_D, buff=0, stroke_width=5)
        flecha_pos.shift(UP * 0.45)
        txt_pos = Text("+30% Historial Crediticio", font_size=16, color=GREEN_B)
        txt_pos.next_to(flecha_pos, UP, buff=0.12)
        self.play(GrowArrow(flecha_pos), FadeIn(txt_pos), run_time=1.4)
        self.wait(0.8)

        val_deudas_x = eje.n2p(65)
        flecha_neg = Arrow(start=val_historial_x, end=val_deudas_x, color=RED_D, buff=0, stroke_width=5)
        flecha_neg.shift(UP * 1.05)
        txt_neg = Text("-15% Deudas Altas", font_size=16, color=RED_B)
        txt_neg.next_to(flecha_neg, UP, buff=0.12)
        self.play(GrowArrow(flecha_neg), FadeIn(txt_neg), run_time=1.4)
        self.wait(0.8)

        linea_final = Line(val_deudas_x + UP * 0.45, val_deudas_x + DOWN * 0.45, color=YELLOW, stroke_width=5)
        txt_final = Text("Predicción: 65%", font_size=22, color=YELLOW, weight=BOLD)
        txt_final.next_to(linea_final, DOWN, buff=0.3)

        self.play(Create(linea_final), run_time=0.8)
        self.play(Indicate(txt_final, color=YELLOW), FadeIn(txt_final), run_time=1.2)
        self.wait(1.8)

        cierre = Text(
            "SHAP muestra cuánto aporta cada variable a una decisión.",
            font_size=24,
            color=WHITE,
        )
        cierre.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cierre, shift=UP * 0.15), run_time=1.0)
        self.wait(6.0)
