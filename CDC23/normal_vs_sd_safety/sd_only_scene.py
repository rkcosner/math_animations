from manim import *
import numpy as np 


class normal_vs_sd_safety(MovingCameraScene):
    def construct(self):
        axes_left = Axes( x_length=10, y_length=10)
        axes_right = Axes(x_length=10, y_length=10)
        circle_left=Circle(color=WHITE, radius=1.5)
        circle_right=Circle(color=WHITE, radius=1.5)
        circle_left.set_fill(GREEN, opacity=0.5)
        circle_right.set_fill(GREEN, opacity=0.5)


        axes_left.scale(0.5).move_to(np.array([-3,0,0]))
        axes_right.scale(0.5).move_to(np.array([3,0,0]))

        cont_safety_txt = Text("Continuous-Time Safety")
        cont_safety_txt.scale(0.5).next_to(axes_left, UP)

        disc_safety_txt = Text("Sampled-Data Safety")
        disc_safety_txt.scale(0.5).next_to(axes_right, UP)

        self.add(axes_left, axes_right)
        circle_left.move_to(axes_left.get_center())
        circle_right.move_to(axes_right.get_center())
        self.add(cont_safety_txt, disc_safety_txt)
        self.add(circle_left, circle_right)


        self.wait(1)

        scale = 3

        axes_2 = Axes(x_length=10, y_length=10)
        axes_2.move_to(np.array([-6,0,0]))
        axes_2.scale(scale)

        self.play(FadeOut(axes_left), FadeOut(circle_left), FadeOut(cont_safety_txt), FadeOut(disc_safety_txt))
        self.play(
            Transform(axes_right, axes_2), 
            circle_right.animate.scale(scale).move_to(np.array([-6,0,0]))
        )

        self.wait(2)

        dot = Dot(radius=0.1, color=YELLOW)
        dot.move_to(np.array([-6, 0, 0 ]) + np.array([0,-scale,0]) * circle_right.get_radius())
        self.add(dot)


        self.t_int = 0 
        self.sample_pts = []

        def update_state(mob, dt):
            self.t_int += 1
            state = mob.get_center()
            time = self.t_int * dt

            state[0] = -6 + np.cos(-PI * 2 /3 + time/3) * circle_right.get_radius() * scale 
            state[1] =  0 + np.sin(-PI * 2 /3 + time/3) * circle_right.get_radius() * scale
            
            radius_vec = np.array([state[0]+6, state[1], 0]) * (1.09 + 0.1*np.sin(self.t_int*PI/10-PI/2))
            state[0] = -6 + radius_vec[0]
            state[1] = radius_vec[1]

            if self.t_int % 20 == 0: 
                self.sample_pts.append(Dot(radius=0.1, color=BLUE))
                self.sample_pts[-1].move_to(state)
                self.add(self.sample_pts[-1])

            mob.move_to(state)            


        self.ss_curve = VGroup()
        self.ss_curve.add(Line(np.array([-10,-10,0]), np.array([-10,-10,0])))
        def get_ss_curve():
            last_ss = self.ss_curve[-1]
            new_ss = Line(last_ss.get_end(),dot.get_center(), color=YELLOW)
            self.ss_curve.add(new_ss)
            return self.ss_curve

        
        
        cont_pts_text = Text("Continuous Trajectory", color=YELLOW)
        disc_pts_text = Text("Sample Points", color=BLUE)

        cont_pts_text.to_corner(UR)
        disc_pts_text.next_to(cont_pts_text, DOWN)

        self.play(Write(cont_pts_text))
        self.play(Write(disc_pts_text))

        ss_line = always_redraw(get_ss_curve)
        dot.add_updater(update_state)        
        self.add(ss_line)
        self.add(dot)


        self.wait(10)

        line1 = Text("The continuous trajectory\_line"), 
        line2 = Text("is unsafe, but its sampled\_line"),
        line3 = Text("trajectory is safe")

        text.move_to(np.array([6, -1, 0]))
        self.play(Write(text))
