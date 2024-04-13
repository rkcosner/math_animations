
from manim import *
import numpy as np 


class set_inv(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_length = 6, 
            y_length = 6, 
            z_length = 0.01, 
            tips = False
        )

        axesR = ThreeDAxes(
            x_length = 0.01, 
            y_length = 0.01, 
            z_length = 4,
            tips = False 
        )

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        phi.set_value(0)
        theta.set_value(-PI/2)
        distance_to_origin.set_value(0.5)

        
        circle=Circle(color=WHITE, radius=3).set_opacity(0).scale(0.75)
        circle.set_fill(color=GREEN, opacity=0.5)
        C_text = MathTex("\mathcal{C}").move_to(RIGHT + UP)
        self.add(circle, C_text)


        self.add(axes, axesR)

        z_label = axesR.get_z_axis_label("\\quad h(\mathbf{x})")
        self.add(z_label)
        

        self.wait(1)


        self.play(phi.animate.set_value(75*DEGREES), theta.animate.set_value(-60*DEGREES), distance_to_origin.animate.set_value(1))



        def cbf(x,y): 
            z = (9 - np.linalg.norm(np.array([x,y]))**2) * 0.2
            return np.array([x,y,z])

        cbf_surface = Surface(
            cbf, 
            resolution=(24,24), 
            v_range=[-3,3], 
            u_range=[-3,3]
        ).scale(0.75)



        cbf_surface.set_style(fill_opacity=1, stroke_color=WHITE)
        cbf_surface.set_fill_by_checkerboard(WHITE, WHITE, opacity=0.25)
        self.play(Create(cbf_surface))

        self.play(FadeOut(cbf_surface))

        new_loc = LEFT*4 +  DOWN*2
        self.play(circle.animate.move_to(new_loc), C_text.animate.move_to(new_loc + RIGHT + UP), axes.animate.move_to(new_loc), FadeOut(z_label), axesR.animate.move_to(RIGHT*4 + UP*2))

        # phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        # self.play( FadeOut(h_on_plot),phi.animate.set_value(0), theta.animate.set_value(-PI/2), distance_to_origin.animate.set_value(0.5), FadeOut(cbf_surface))

        h_tex = MathTex("h : \\mathbb{R}^n \\to \\mathbb{R}").move_to(UP*2).scale(0.85)
        hinv_tex = MathTex("h^{-1}: \\mathbb{R} \\rightsquigarrow \\mathcal{P}(\\mathbb{R}^n) ").move_to(DOWN*2).scale(0.85)
        self.add_fixed_in_frame_mobjects(h_tex, hinv_tex)
        self.play(FadeIn(h_tex), FadeIn(hinv_tex))


        self.wait(1)

        dot = Sphere(circle.point_at_angle(3*np.pi/4), radius=0.1, color=BLUE)


        self.play(FadeIn(dot),run_time = 0.2)
        self.play(dot.animate.move_to(ORIGIN+np.array([-1,-1,2])))
        self.play(dot.animate.move_to(np.array([1,1,2])).set_color(RED).scale(0.5))
        self.play(dot.animate.move_to(axesR.coords_to_point(0,0,0)))
        self.play(FadeOut(dot))

        dot.move_to(axesR.coords_to_point(0,0,2))

        self.play(FadeIn(dot))
        self.play(dot.animate.move_to(np.array([1.4,1.1,-2.3])))
        

        self.play(dot.animate.move_to([-2,-1.6,-1.9]).set_color(BLUE).scale(2))
        circle_dot = Circle(radius = 2, color=WHITE).set_opacity(1).scale(0.75)
        circle_dot.set_fill(color=BLUE, opacity=0.5)
        circle_dot.move_to(new_loc)
        self.play(ReplacementTransform(dot, circle_dot))
        self.play(FadeOut(circle_dot))

        ##########################################

        center = circle.get_center()
        dot = Sphere((circle.point_at_angle(3*np.pi/4)-center)*0.5 + center, radius=0.1, color=BLUE)
        self.play(FadeIn(dot), run_time=0.2)
        
        self.play(FadeIn(dot),run_time = 0.2)
        self.play(dot.animate.move_to(ORIGIN+np.array([-1,-1,2])))
        self.play(dot.animate.move_to(np.array([1,1,2])).set_color(RED).scale(0.5))
        self.play(dot.animate.move_to(axesR.coords_to_point(0,0,1)))
        self.play(FadeOut(dot))

        dot.move_to(axesR.coords_to_point(0,0,-2))

        self.play(FadeIn(dot))
        self.play(dot.animate.move_to(np.array([1.4,1.1,-2.3])))
        

        self.play(dot.animate.move_to([-2,-1.6,-1.9]).set_color(BLUE).scale(2))
        circle_dot = Circle(radius = 4, color=WHITE).set_opacity(1).scale(0.75)
        circle_dot.set_fill(color=BLUE, opacity=0.5)
        circle_dot.move_to(new_loc)
        self.play(ReplacementTransform(dot, circle_dot))
        self.play(FadeOut(circle_dot))

        # Clean Up
        self.play(
            phi.animate.set_value(0), 
            theta.animate.set_value(-PI/2), 
            distance_to_origin.animate.set_value(0.5), 
            FadeOut(h_tex), 
            FadeOut(hinv_tex), 
            FadeOut(axesR), 
            axes.animate.move_to(ORIGIN), 
            C_text.animate.move_to(RIGHT+UP), 
            circle.animate.move_to(ORIGIN)
            )
