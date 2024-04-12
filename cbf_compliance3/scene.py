
from manim import *
import numpy as np 


class ThreeDCamera_Safety(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()


        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        phi.set_value(0)
        theta.set_value(-PI/2)
        distance_to_origin.set_value(0.5)

        
        circle=Circle(color=WHITE, radius=3).set_opacity(0)
        circle.set_fill(color=GREEN, opacity=0.5)
        C_text = MathTex("\mathcal{C}")
        self.add(circle, C_text)

        self.wait(1)

        self.play(Create(axes))
        
        self.play(phi.animate.set_value(75*DEGREES), theta.animate.set_value(-60*DEGREES), distance_to_origin.animate.set_value(1))

        z_label = axes.get_z_axis_label("\\textrm{Learned Controller, } \\mathbf{k}_\\theta(\\mathbf{x})")
        
        self.play(Write(z_label))

        # circle=Circle(color=WHITE, radius=3)
        # circle.set_fill(GREEN, opacity=0.5)

        # safe_text = Text("Safe Region", color=GREEN)
        # C_text = MathTex("\mathcal{C}")

        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        # self.add(axes)

        # self.add_fixed_in_frame_mobjects(safe_text)
        # safe_text.to_corner(UL)
        # C_text.scale(2).next_to(np.array([0,0,0]), np.array([3,3,0]))

        # self.play(Create(circle), Write(safe_text), Write(C_text))

        # self.wait(2)

        def input(theta, r):
            x = r*np.cos(theta)
            y = r*np.sin(theta)
            z = np.cos(theta*3)*0.2 + np.sin(theta*12)*0.1 + r*0.25
            return np.array([x,y,z])

        input_surface = Surface(
            input, 
            resolution=(10,24), 
            v_range=[2.5,3.5], 
            u_range=[0,2*np.pi]
        )


        # h_text = MathTex(r"\textrm{CBF } h, \; \mathcal{C} = \{ \mathbf{x} ~|~ h(\mathbf{x})\geq 0 \} ")
        # h_on_plot = MathTex(r"h(\mathbf{x})")
        # self.add_fixed_in_frame_mobjects( h_text, h_on_plot)
        # h_text.to_corner(UL)
        # h_on_plot.move_to(np.array([2,2,0]))

        input_surface.set_style(fill_opacity=1, stroke_color=YELLOW)
        input_surface.set_fill_by_checkerboard(WHITE, WHITE, opacity=0.25)
        self.play(Create(input_surface))

        # self.wait(2)

        # phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        # self.play( FadeOut(h_on_plot),phi.animate.set_value(0), theta.animate.set_value(-PI/2), distance_to_origin.animate.set_value(0.5), FadeOut(input_surface))

        self.wait(5)

        self.play( FadeOut(input_surface),phi.animate.set_value(0), theta.animate.set_value(-PI/2), distance_to_origin.animate.set_value(0.5), FadeOut(input_surface))
        self.play(FadeOut(axes))
