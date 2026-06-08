from pathlib import Path

from manim import *


ASSET_DIR = Path(__file__).parent / "assets"
AUDIO_PATH = ASSET_DIR / "narracion_roc_gini.aiff"
LOGO_PATH = ASSET_DIR / "cerebroDatabankHorizontal.png"


class VideoROCGini30s(Scene):
    def logo_scene(self, logo, halo, linea, run_time=1.4):
        self.play(
            FadeIn(logo, shift=UP * 0.15),
            halo.animate.set_opacity(0.35),
            run_time=run_time,
        )
        self.play(
            logo.animate.scale(1.04),
            halo.animate.scale(1.08).set_opacity(0.12),
            linea.animate.set_opacity(0.85),
            run_time=1.0,
        )

    def construct(self):
        self.camera.background_color = "#17051f"

        if AUDIO_PATH.exists():
            self.add_sound(str(AUDIO_PATH), gain=-2)

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

        # --- 1. INTRO DATABANK ACADEMY ---
        self.logo_scene(logo, halo, linea)
        self.wait(0.4)
        self.play(
            FadeOut(logo, shift=UP * 0.2),
            FadeOut(halo),
            FadeOut(linea),
            run_time=0.8,
        )

        # --- 2. INTRODUCCION Y EJES ---
        titulo = Text("Curva ROC, AUC y Coeficiente de Gini", font_size=28, color=BLUE_B)
        titulo.to_edge(UP, buff=0.4)
        self.play(Write(titulo), run_time=1.4)
        self.wait(0.6)

        ejes = Axes(
            x_range=[0, 1.1, 0.2],
            y_range=[0, 1.1, 0.2],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY_C, "include_numbers": True},
        ).shift(LEFT * 2.5 + DOWN * 0.5)

        etiqueta_x = Text("FPR (1 - Especificidad)", font_size=14, color=GRAY_B)
        etiqueta_x.next_to(ejes.x_axis, DOWN, buff=0.3)
        etiqueta_y = Text("TPR (Sensibilidad)", font_size=14, color=GRAY_B)
        etiqueta_y.next_to(ejes.y_axis, LEFT, buff=0.3).rotate(PI / 2)

        self.play(Create(ejes), FadeIn(etiqueta_x), FadeIn(etiqueta_y), run_time=2.5)
        self.wait(1.0)

        # --- 3. LINEA ALEATORIA Y CURVA ROC ---
        linea_base = ejes.plot(lambda x: x, color=GRAY_A)
        linea_aleatoria = DashedVMobject(linea_base, num_dashes=30)

        lbl_aleatorio = Text("Modelo Aleatorio (AUC = 0.5)", font_size=12, color=GRAY_A)
        lbl_aleatorio.move_to(LEFT * 0.8 + DOWN * 0.8).rotate(PI / 4)

        curva_roc = ejes.plot(lambda x: x ** (1 / 3), color=YELLOW, x_range=[0, 1])
        lbl_roc = Text("Curva ROC", font_size=16, color=YELLOW).move_to(LEFT * 3.5 + UP * 1.5)

        self.play(Create(linea_aleatoria), FadeIn(lbl_aleatorio), run_time=2.0)
        self.play(Create(curva_roc), FadeIn(lbl_roc), run_time=2.5)
        self.wait(2.0)

        # --- 4. EXPLICACION DEL AUC ---
        auc_area = ejes.get_area(curva_roc, x_range=[0, 1], color=YELLOW_E, opacity=0.4)

        panel_txt = VGroup(
            MathTex(r"\text{AUC} = \int_{0}^{1} \text{ROC}(x) dx", color=YELLOW),
            Text("Mide la capacidad de separación.", font_size=14, color=GRAY_A),
            MathTex(r"\text{Gini} = 2 \times \text{AUC} - 1", color=GREEN_B),
            Text("Mide la ganancia sobre el azar.", font_size=14, color=GRAY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT * 3.5 + UP * 0.5)

        self.play(FadeIn(auc_area), run_time=1.0)
        self.play(Write(panel_txt[0]), run_time=2.0)
        self.play(FadeIn(panel_txt[1]), run_time=0.8)
        self.wait(3.0)

        # --- 5. RELACION CON EL GINI ---
        gini_area = ejes.get_area(
            curva_roc,
            x_range=[0, 1],
            bounded_graph=linea_base,
            color=GREEN_E,
            opacity=0.6,
        )

        self.play(FadeOut(auc_area), run_time=0.7)
        self.play(FadeIn(gini_area), run_time=1.0)
        self.play(Write(panel_txt[2]), run_time=2.0)
        self.play(FadeIn(panel_txt[3]), run_time=0.8)
        self.play(Indicate(panel_txt[2], color=GREEN_B), scale_factor=1.1)
        self.wait(2.5)

        self.play(
            FadeOut(titulo),
            FadeOut(ejes),
            FadeOut(etiqueta_x),
            FadeOut(etiqueta_y),
            FadeOut(linea_aleatoria),
            FadeOut(lbl_aleatorio),
            FadeOut(curva_roc),
            FadeOut(lbl_roc),
            FadeOut(gini_area),
            FadeOut(panel_txt),
            run_time=1.1,
        )

        # --- 6. CIERRE DATABANK ACADEMY ---
        logo.set_width(7.5)
        logo.move_to(ORIGIN)
        halo.set_width(4.5)
        halo.move_to(LEFT * 2.6)
        halo.set_opacity(0.0)
        linea.next_to(logo, DOWN, buff=0.35)
        linea.set_opacity(0.0)
        self.logo_scene(logo, halo, linea, run_time=1.2)
        self.wait(9.0)
