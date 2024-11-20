from manim import *
import numpy as np 

WHITE_BACKGROUND = True
if WHITE_BACKGROUND:
    colors = [WHITE, BLACK, BLUE]
else:
    colors = [BLACK, WHITE, YELLOW]

class safety(ThreeDScene):
    def construct(self):
        self.camera.background_color = colors[0]

        axes = ThreeDAxes()
        axes.color = colors[1]

        circle=Circle(color=colors[1], radius=3)
        circle.set_fill(GREEN, opacity=0.5)

        safe_text = Text("Safe Region", color=colors[1])
        C_text = MathTex("\mathcal{C}", color=colors[1])

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        self.add_fixed_in_frame_mobjects(safe_text)
        safe_text.to_corner(UL)
        C_text.scale(2).next_to(np.array([0,0,0]), np.array([3,3,0]))

        self.play(Create(circle), Write(safe_text), Write(C_text))

        self.wait(2)

        def cbf(x,y): 
            z = (9 - np.linalg.norm(np.array([x,y]))**2) * 0.2
            return np.array([x,y,z])

        cbf_surface = Surface(
            cbf, 
            resolution=(24,24), 
            v_range=[-3,3], 
            u_range=[-3,3]
        )
        cbf_surface.set_color(colors[1])


        h_text = MathTex(r"\textrm{CBF } h, \; \mathcal{C} = \{ \mathbf{x} ~|~ h(\mathbf{x})\geq 0 \} ", color=colors[1])
        h_on_plot = MathTex(r"h(\mathbf{x})", color=colors[1])
        self.add_fixed_in_frame_mobjects( h_text, h_on_plot)
        h_text.to_corner(UL)
        h_on_plot.move_to(np.array([2,2,0]))

        cbf_surface.set_style(fill_opacity=1, stroke_color=GREEN, stroke_width=0.5)
        cbf_surface.set_fill_by_checkerboard(GREEN, GREEN, opacity=0.25)
        self.remove(safe_text)
        self.play(Create(cbf_surface),  Write(h_text), Write(h_on_plot))

        self.wait(2)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        self.play( FadeOut(h_on_plot),phi.animate.set_value(0), theta.animate.set_value(-PI/2), distance_to_origin.animate.set_value(0.5), FadeOut(cbf_surface))

        self.wait(2)

        self.play(FadeOut(h_text), axes.animate.move_to(np.array([-5,0,0])), circle.animate.move_to(np.array([-5,0,0])), C_text.animate.next_to(np.array([-5,0,0]), np.array([3,3,0])))

        axes_h = Axes(x_range=[0,10,2], y_range=[-1,5,2], color=colors[1])
        axes_h.color = colors[1]
        axes_h.scale(0.5).move_to(np.array([7,3,0]))
        axes_hdot = Axes(x_range=[0,10,2], y_range=[-3,3,2])
        axes_hdot.color = colors[1]
        axes_hdot.scale(0.5).move_to(np.array([7,-4,0]))

        h_plot_text = MathTex(r"h(\mathbf{x})", color=colors[1])
        h_plot_text.scale(2).next_to(axes_h,UP)
        h_dot_plot_text = MathTex(r"\frac{dh}{dt}(\mathbf{x}, \mathbf{u})", color=colors[1])
        h_dot_plot_text.scale(2).next_to(axes_hdot, UP)

        self.play(Create(axes_h), Create(axes_hdot), Write(h_plot_text), Write(h_dot_plot_text))

        ss_pt = Dot(point=np.array([-5,0,0]), radius = 0.25, color=colors[2]) 
        h_pt = Dot(point=np.array([4.15,4,0]), radius=0.1, color=colors[2])
        hdot_pt = Dot(point=np.array([4.15,-5.5,0]), radius=0.1, color=colors[2])


        self.t_int = 0 
        self.dt = 0.2
        alpha = 0.5
        self.h = 9 * 0.2
        def update_state(mob, dt):
            # State Starts at -5, radius in image is 3.2
            self.t_int += 1
            state = mob.get_center()
            perspective_ratio = 1
            
            x_k = (state[0]+5)/perspective_ratio/np.cos(-PI/4)
            h_k = (9 - x_k**2) * 0.2
            h_kp1 = (1 - alpha * dt) * h_k 
            self.h = h_kp1
            x_kp1 = np.sqrt(- (h_kp1 / 0.2 - 9))
            state[0] = x_kp1 * np.cos(-PI/4) * perspective_ratio - 5
            state[1] = x_kp1 * np.sin(-PI/4) * perspective_ratio 
            mob.move_to(state)

        def update_h(mob, dt):
            pt = mob.get_center()
            y_scale = 2 / (9*0.2)
            offset = 2 
            y = (self.h * y_scale + offset) 
            pt[0] += dt 
            pt[1] = y 
            mob.move_to(pt)

        def update_hdot(mob, dt): 
            pt = mob.get_center()
            scale = 1.5
            offset = -4
            pt[0] += dt
            pt[1] = -alpha*self.h * scale + offset
            mob.move_to(pt) 



        self.ss_curve = VGroup()
        self.ss_curve.add(Line(ss_pt.get_center(),ss_pt.get_center(), color=colors[2]))
        self.h_curve = VGroup()
        self.h_curve.add(Line(h_pt.get_center(), h_pt.get_center(), color=colors[2]))
        self.hdot_curve = VGroup()
        self.hdot_curve.add(Line(hdot_pt.get_center(), hdot_pt.get_center(), color=colors[2]))


        def get_ss_curve():
            last_ss = self.ss_curve[-1]
            new_ss = Line(last_ss.get_end(),ss_pt.get_center(), color=colors[2])
            self.ss_curve.add(new_ss)
            return self.ss_curve

        def get_h_curve(): 
            last_h = self.h_curve[-1]
            new_h = Line(last_h.get_end(),h_pt.get_center(), color=colors[2])
            self.h_curve.add(new_h)
            return self.h_curve

        def get_hdot_curve(): 
            last_hdot = self.hdot_curve[-1]
            new_hdot = Line(last_hdot.get_end(),hdot_pt.get_center(), color=colors[2])
            self.hdot_curve.add(new_hdot)
            return self.hdot_curve

        ss_pt.add_updater(update_state)
        h_pt.add_updater(update_h)
        hdot_pt.add_updater(update_hdot)

        ss_line = always_redraw(get_ss_curve)
        h_line = always_redraw(get_h_curve)
        hdot_line = always_redraw(get_hdot_curve)

        self.add(ss_line, h_line, hdot_line)
        self.add(ss_pt, h_pt, hdot_pt)



        self.wait(5.5)
        #################

        # ss_pt.remove_updater(update_state)    
        # h_pt.remove_updater(update_h)
        # hdot_pt.remove_updater(update_hdot)

        # self.begin_3dillusion_camera_rotation(rate=2)
        # self.wait(1)
        # self.stop_3dillusion_camera_rotation()

scene = safety()