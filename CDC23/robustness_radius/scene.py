from manim import *
import numpy as np 


class robustness_radius(Scene):
    def construct(self):
        axes = Axes(x_range=[-4,4,1], y_range=[-4,4,1])
        circle=Circle(color=WHITE, radius=1.5)
        circle.set_fill(GREEN, opacity=1)


        # self.set_camera_orientation(phi=0, theta=-PI/2)
        axes.move_to(np.array([-3,0,0]))

        # cont_safety_txt = Text("Continuous-Time Safety")
        # cont_safety_txt.scale(0.5).next_to(axes_left, UP)

        # disc_safety_txt = Text("Sampled-Data Safety")
        # disc_safety_txt.scale(0.5).next_to(axes_right, UP)

        self.add(axes)
        circle.move_to(axes.get_center())
        # self.add(cont_safety_txt, disc_safety_txt)
        self.play(Create(circle))

        self.wait(2)

        # ss_pt = Dot(point=np.array([-3,0,0]), radius = 0.1, color=YELLOW) 

        # self.add(ss_pt)
        # self.t_int = 0 
        # self.dt = 0.1
        # alpha = 0.5
        # self.h = 2.25 * 0.2
        # def update_state(mob, dt):
        #     # State Starts at -5, radius in image is 3.2
        #     self.t_int += 1
        #     state = mob.get_center()
        #     perspective_ratio = 1
            
        #     x_k = (state[0]+3)/perspective_ratio/np.cos(-PI/4)
        #     h_k = (2.25 - x_k**2) * 0.2
        #     h_kp1 = (1 - alpha * dt) * h_k 
        #     self.h = h_kp1
        #     x_kp1 = np.sqrt(- (h_kp1 / 0.2 - 2.25))
        #     state[0] = x_kp1 * np.cos(-PI/4) * perspective_ratio - 3
        #     state[1] = x_kp1 * np.sin(-PI/4) * perspective_ratio 
        #     mob.move_to(state)



        # self.ss_curve = VGroup()
        # self.ss_curve.add(Line(ss_pt.get_center(),ss_pt.get_center()))

        # def get_ss_curve():
        #     last_ss = self.ss_curve[-1]
        #     new_ss = Line(last_ss.get_end(),ss_pt.get_center(), color=YELLOW)
        #     self.ss_curve.add(new_ss)
        #     return self.ss_curve

        # ss_pt.add_updater(update_state)
        # ss_line = always_redraw(get_ss_curve)

        # self.add(ss_line)#, h_line, hdot_line)
        # self.add(ss_pt) #, h_pt, hdot_pt)



        # dots = [] 
        # dots.append(Dot(point=np.array([3,0,0]), radius = 0.025, color=YELLOW))
        # self.add(dots[-1])
        # self.wait(0.1)
        # for i in range(30): 
        #     state = dots[-1].get_center()
        #     perspective_ratio = 1
            
        #     x_k = (state[0]-3)/perspective_ratio/np.cos(-PI/4)
        #     h_k = (2.5 - x_k**2) * 0.2
        #     h_kp1 = (1 - alpha * self.dt) * h_k 
        #     self.h = h_kp1
        #     x_kp1 = np.sqrt(- (h_kp1 / 0.2 - 2.5))
        #     state[0] = x_kp1 * np.cos(-PI/4) * perspective_ratio + 3
        #     state[1] = x_kp1 * np.sin(-PI/4) * perspective_ratio 
        #     dots.append(Dot(point=state, radius = 0.025, color=YELLOW))
        #     self.add(dots[-1])
        #     self.wait(0.1)


        ss_pt = Dot(point=np.array([-3,0,0]), radius = 0.1, color=YELLOW) 

        self.add(ss_pt)
        self.t_int = 0 
        self.dt = 0.1
        alpha = 0.5
        self.h = 2.25 * 0.2
        def update_state(mob, dt):
            # State Starts at -5, radius in image is 3.2
            self.t_int += 1
            state = mob.get_center()
            perspective_ratio = 1
            
            x_k = (state[0]+3)/perspective_ratio/np.cos(-PI/4)
            h_k = (2.25 - x_k**2) * 0.2
            h_kp1 = (1 - alpha * dt) * h_k 
            self.h = h_kp1
            x_kp1 = np.sqrt(- (h_kp1 / 0.2 - 2.25))
            state[0] = x_kp1 * np.cos(-PI/4) * perspective_ratio - 3
            state[1] = x_kp1 * np.sin(-PI/4) * perspective_ratio 
            mob.move_to(state)



        self.ss_curve = VGroup()
        self.ss_curve.add(Line(ss_pt.get_center(),ss_pt.get_center()))

        def get_ss_curve():
            last_ss = self.ss_curve[-1]
            new_ss = Line(last_ss.get_end(),ss_pt.get_center(), color=YELLOW)
            self.ss_curve.add(new_ss)
            return self.ss_curve

        ss_pt.add_updater(update_state)
        ss_line = always_redraw(get_ss_curve)

        self.add(ss_line)#, h_line, hdot_line)
        self.add(ss_pt) #, h_pt, hdot_pt)



        dots = [] 
        dots.append(Dot(point=np.array([3,0,0]), radius = 0.025, color=YELLOW))
        self.add(dots[-1])
        self.wait(0.1)
        for i in range(30): 
            state = dots[-1].get_center()
            perspective_ratio = 1
            
            x_k = (state[0]-3)/perspective_ratio/np.cos(-PI/4)
            h_k = (2.5 - x_k**2) * 0.2
            h_kp1 = (1 - alpha * self.dt) * h_k 
            self.h = h_kp1
            x_kp1 = np.sqrt(- (h_kp1 / 0.2 - 2.5))
            state[0] = x_kp1 * np.cos(-PI/4) * perspective_ratio + 3
            state[1] = x_kp1 * np.sin(-PI/4) * perspective_ratio 
            dots.append(Dot(point=state, radius = 0.025, color=YELLOW))
            self.add(dots[-1])
            self.wait(0.1)

