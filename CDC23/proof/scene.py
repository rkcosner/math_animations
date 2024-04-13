from manim import *
import numpy as np 



class proof(Scene):
    def construct(self):
                
        circle0=Circle(color=WHITE, radius=2).set_opacity(0)
        circle0.set_fill(GREEN, opacity=0.5)


        circle=Circle(color=WHITE, radius=10).set_opacity(0)
        circle.set_fill(GREEN, opacity=0.5).move_to(LEFT*8)

        calC = MathTex("\\mathcal{C}")#.move_to(LEFT*4).scale(2)
        self.add(circle0, calC)


        self.play(Wait(1))

        self.play(ReplacementTransform(circle0,  circle), calC.animate.scale(2).move_to(LEFT*1+DOWN))


        circleBr2 = Circle(color=WHITE, radius=14).set_opacity(1).move_to(LEFT*8).set_fill(opacity=0)
        cbr2_tex = MathTex("\\mathcal{C}\oplus \\mathcal{B}_{r_2}").move_to(RIGHT*4 +  DOWN)
        self.play(FadeIn(circleBr2, cbr2_tex))


        theta = np.pi/20
        dot = Dot(color=BLUE, radius=0.2).move_to(-0.15*(circleBr2.point_at_angle(theta)- circleBr2.get_center()) + circleBr2.point_at_angle(theta))
        self.play(Write(dot))

        dot_dC = Dot(color=YELLOW, radius=0.2).move_to(circle.point_at_angle(theta))
        line_dC = Line(start=dot.get_center(), end=dot_dC.get_center())
        r1_tex = MathTex("\\leq r_2").next_to(line_dC, UP)
        self.play(Create(dot_dC), FadeIn(line_dC), Write(r1_tex))
        self.wait(3)

        dot_D = Dot(color=ORANGE, radius=0.2).move_to(circle.point_at_angle(0))
        line_D = Line(start=dot_dC.get_center(), end=dot_D.get_center())
        r2_tex = MathTex("\\leq r_1").next_to(line_D, LEFT)
        self.play(Create(dot_D), FadeIn(line_D), Write(r2_tex))
        self.wait(3)


        line_r3 = Line(start=dot.get_center(), end=dot_D.get_center())
        r3_tex = MathTex("\\leq r_3").move_to(line_r3.get_center() + 0.5*(0.5*DOWN+RIGHT))
        self.play(FadeIn(line_r3), Write(r3_tex))

        self.play(FadeOut(dot_dC, line_dC, line_D, r1_tex, r2_tex, ))


        consider_tex = MathTex("\\textrm{Consider the set: }").move_to(LEFT*2.75 +UP*2.75)
        Cd_tex = MathTex("\\mathcal{C}_\\delta =\\left \\{ \\mathbf{x} ~|~ h(\\mathbf{x}) \\geq \\alpha^{-1} \\left(\\frac{-1}{ 2\\varphi } (\\mathfrak{L}_{\\mathbf{k}_\\theta} r_3 + M_\\mathbf{e})^2  \\right)  \\right \\}" ).scale(0.7).next_to(consider_tex, DOWN)
        self.play(Write(consider_tex), Write(Cd_tex))

        implies_tex = MathTex("\\textrm{U.S.C} \\implies \\exists \\; \\varphi \\textrm{ s.t. } \\mathcal{C}_\\delta \\subset \\mathcal{C} \\oplus \\mathcal{B}_{r_2}").scale(0.9).move_to(Cd_tex.get_center() + 0.8*DOWN + 0.2*RIGHT)
        self.play(Write(implies_tex))


        hinvC = Circle(color=WHITE, radius=13).set_opacity(1).move_to(LEFT*8).set_fill(opacity=0)
        hinvC_tex = MathTex("\\mathcal{C}_\\delta").move_to(RIGHT*3.5 + DOWN)
        self.play(FadeIn(hinvC, hinvC_tex), FadeOut(cbr2_tex)) 
        self.wait(2)
        self.play(FadeOut( circleBr2), run_time=2)





        ### Return to start

        self.play(FadeOut(
            hinvC, hinvC_tex, consider_tex, Cd_tex, implies_tex, line_r3, dot, dot_D, r3_tex
        ))
        circle0=Circle(color=WHITE, radius=2).set_opacity(0)
        circle0.set_fill(GREEN, opacity=0.5)
        self.play(ReplacementTransform(circle, circle0), calC.animate.scale(0.5).move_to(ORIGIN))
        