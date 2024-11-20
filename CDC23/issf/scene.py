from manim import *
import numpy as np 

WHITE_BACKGROUND = True
if WHITE_BACKGROUND:
    colors = [WHITE, BLACK, BLUE, RED]
else:
    colors = [BLACK, WHITE, YELLOW, RED]

class issf(Scene):
    def construct(self):

        self.camera.background_color = colors[0]
                
        axes = Axes(
            x_range = [-5.5, 5.5, 1],
            y_range = [-5.5, 5.5, 1], 
            x_length = 6, 
            y_length = 6, 
            tips = True
        )
        axes.color = colors[1]
        circle=Circle(color=colors[1], radius=1.5)
        circle.set_fill(GREEN, opacity=0.5)


        # h0 = MathTex("h(\\mathbf{x}) = 0 ").move_to(RIGHT + DOWN*1.7).scale(0.75)
        self.add(axes, circle)


        # Number of points required
        num_points = 60
        # Calculate each angle
        angles = [n * (360 / num_points) for n in range(num_points)]
        # Points on circumference of circle
        points = [circle.point_at_angle(n*DEGREES) for n in angles]
        # Create circles at each point
        circles = [Circle(radius=0.005, color=colors[1], fill_opacity=1).move_to(p) for p in points]
        # Add each of the points to the scene
        for c in circles:
            self.add(c)


        calC = MathTex("\\mathcal{C}", color=colors[1]).move_to(RIGHT/2 + UP/2)
        calCd = MathTex("\\mathcal{C}_\delta", color=colors[1]).move_to(RIGHT/2 + UP/2)
        self.add(calC)

        disturbance_txt = MathTex("\\textrm{Disturbance:} \\\\ \\Vert \\mathbf{d}(t) \\Vert_\infty \leq \delta ", color=colors[1]).move_to(RIGHT*3 + UP*2)
        # self.play(Write(disturbance_txt))
        delta = MathTex("\\delta", color=colors[1]).move_to(RIGHT*3 + UP*2)
        self.add(delta)
        # self.play(FadeOut(disturbance_txt), FadeIn(delta))

        up_arrow = Arrow(start=DOWN/2, end=UP/2, color=colors[1]).next_to(delta, RIGHT)
        
        
        self.play(FadeIn(up_arrow))
        dist_group = Group(delta, up_arrow)

        self.play(circle.animate.scale(1.5), ReplacementTransform(calC, calCd), dist_group.animate.scale(2), run_time = 2)
        
        hgamma = MathTex("h(\\mathbf{x}) \geq -\\iota(\\vert \\delta \\vert_\\infty) ", color=colors[1]).move_to(RIGHT*1.5 + (DOWN*1.7)*1.5).scale(0.75)
        self.play(Write(hgamma))

        start_and_end = up_arrow.get_start_and_end()

        down_arrow = Arrow(start=start_and_end[1] + UP/4, end=start_and_end[0] + DOWN/4, color=colors[1], tip_length=1)
        

        self.play(ReplacementTransform(up_arrow, down_arrow))

        dist_group = Group(delta, down_arrow)

        calC0 = MathTex("\\mathcal{C}", color=colors[1]).move_to(RIGHT/2 + UP/2)

        self.play(circle.animate.scale(2.0/3), dist_group.animate.scale(0.5), Transform(calCd, calC0), FadeOut(hgamma), run_time = 2)
        self.play(FadeOut(down_arrow))


