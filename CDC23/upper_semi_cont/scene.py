from manim import *
import numpy as np 



class upper_semi_cont(Scene):
    def construct(self):
                
        axes = Axes(
            x_range = [-5.5, 5.5, 1],
            y_range = [-5.5, 5.5, 1], 
            x_length = 6, 
            y_length = 6, 
            tips = True
        )
        circle=Circle(color=WHITE, radius=1.5)
        circle.set_fill(GREEN, opacity=0.5)

        calC = MathTex("\\mathcal{C}").move_to((UP + RIGHT)*0.5)

        # h0 = MathTex("h(\\mathbf{x}) = 0 ").move_to(RIGHT + DOWN*1.7).scale(0.75)
        self.add(axes, circle, calC)


        B_eps = Circle(color=WHITE, radius=0.4)
        B_eps.set_fill(WHITE, opacity=0.25).move_to(UP*2 + RIGHT*3)
        B_eps_tex = MathTex("\\mathcal{B}_\\epsilon").next_to(B_eps, RIGHT)
        self.play(Create(B_eps),FadeIn(B_eps_tex))
        self.play(FadeOut(B_eps_tex),run_time = 0.5)




        # # # Number of points required
        num_points = 60
        # Calculate each angle
        angles = [n * (360 / num_points) for n in range(num_points)]
        # Points on circumference of circle
        points = [circle.point_at_angle(n*DEGREES) for n in angles]
        points.append(points[0])
        # Add each of the points to the scene
        self.play(B_eps.animate.move_to(points[0]))
        for p in points:
            self.play(B_eps.animate.move_to(p), run_time=0.01)


        cOplusB = Circle(radius = 1.5+0.42, color=WHITE)
        cOplusB.set_fill(GREEN, opacity=0.5)
        cOplusB_tex = MathTex("\\mathcal{C} \\oplus \\mathcal{B}_\\epsilon").move_to(calC.get_center() + RIGHT/2)
        self.play(ReplacementTransform(circle, cOplusB), ReplacementTransform(calC, cOplusB_tex), FadeOut(B_eps))
        self.play(FadeOut(calC, cOplusB_tex), cOplusB.animate.set_fill(GREY))

        eta_interval = MathTex("[-\\eta, \\eta]").move_to(UP*2 + RIGHT*3)
        arrow = Arrow(start=ORIGIN, end=UP)
        c_tex = MathTex("c").next_to(arrow, 0.5*DOWN)

        c_group = VGroup(arrow, c_tex).move_to(eta_interval.get_center() +  0.8*DOWN)


        self.play(FadeIn(c_group, eta_interval))

        eta_circle = Circle(color=WHITE, radius=1.5)
        eta_circle.set_fill(BLUE, opacity=1)
        hinv0_tex = MathTex("h^{-1}(0)")
        hinvc_tex = MathTex("h^{-1}(c)")
        hinvpn_tex = MathTex("h^{-1}(\\eta)")
        hinvnn_tex = MathTex("h^{-1}(-\\eta)")
        
        self.play(FadeIn(eta_circle, hinv0_tex))
        self.play(ReplacementTransform(hinv0_tex, hinvc_tex))
        self.play(eta_circle.animate.scale(1.2), ReplacementTransform(hinvc_tex,hinvpn_tex),c_group.animate.move_to(eta_interval.get_center() +  0.8*DOWN+0.6*RIGHT),  run_time=2)
        self.play(eta_circle.animate.scale(0.6), ReplacementTransform(hinvpn_tex, hinvnn_tex), c_group.animate.move_to(eta_interval.get_center() +  0.8*DOWN+0.6*LEFT), run_time=2)
        self.wait(1)
        

        calC = MathTex("\\mathcal{C}").move_to((UP + RIGHT)*0.5)
        self.play(FadeOut(eta_interval, hinvnn_tex, eta_circle, c_group), cOplusB.animate.scale(1.5/1.92).set_fill(GREEN), FadeIn(calC))


        # calC = MathTex("\\mathcal{C}").move_to(RIGHT/2 + UP/2)
        # calCd = MathTex("\\mathcal{C}_\delta").move_to(RIGHT/2 + UP/2)
        # self.add(calC)

        # disturbance_txt = MathTex("\\textrm{Disturbance:} \\\\ \\Vert \\mathbf{d}(t) \\Vert_\infty \leq \delta ").move_to(RIGHT*3 + UP*2)
        # # self.play(Write(disturbance_txt))
        # delta = MathTex("\\delta").move_to(RIGHT*3 + UP*2)
        # self.add(delta)
        # # self.play(FadeOut(disturbance_txt), FadeIn(delta))

        # up_arrow = Arrow(start=DOWN/2, end=UP/2, color=WHITE).next_to(delta, RIGHT)
        
        
        # self.play(FadeIn(up_arrow))
        # dist_group = Group(delta, up_arrow)

        # self.play(circle.animate.scale(1.5), ReplacementTransform(calC, calCd), dist_group.animate.scale(2), run_time = 2)
        
        # hgamma = MathTex("h(\\mathbf{x}) \geq -\\gamma(\\delta) ").move_to(RIGHT*1.5 + (DOWN*1.7)*1.5).scale(0.75)
        # self.play(Write(hgamma))

        # start_and_end = up_arrow.get_start_and_end()

        # down_arrow = Arrow(start=start_and_end[1] + UP/4, end=start_and_end[0] + DOWN/4, color=WHITE, tip_length=1)
        

        # self.play(ReplacementTransform(up_arrow, down_arrow))

        # dist_group = Group(delta, down_arrow)

        # calC0 = MathTex("\\mathcal{C}").move_to(RIGHT/2 + UP/2)

        # self.play(circle.animate.scale(2.0/3), dist_group.animate.scale(0.5), Transform(calCd, calC0), FadeOut(hgamma), run_time = 2)
        # self.play(FadeOut(down_arrow))


