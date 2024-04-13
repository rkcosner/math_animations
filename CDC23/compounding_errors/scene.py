from manim import *
import numpy as np 



class compounding_errors(Scene):
    def construct(self):
                
        circle0=Circle(color=WHITE, radius=2).set_opacity(0)
        circle0.set_fill(GREEN, opacity=0.5)


        circle=Circle(color=WHITE, radius=9).set_opacity(0).move_to(LEFT*10)
        circle.set_fill(GREEN, opacity=0.5)
        circle_r9 = Circle(radius=9).set_opacity(0).move_to(LEFT*10)
        circle_r8 = Circle(radius=7).set_opacity(0).move_to(LEFT*10) 
        circle_r6 = Circle(radius=5).set_opacity(0).move_to(LEFT*10)
        circle_r4 = Circle(radius=3).set_opacity(0).move_to(LEFT*10)
        safeSet=Circle(color=WHITE, radius=9).set_opacity(0).move_to(LEFT*10)

        # calC = MathTex("\\mathcal{C}")#.move_to(LEFT*4).scale(2)
        self.add(circle) #, calC)


        # self.play(Wait(1))

        # self.play(ReplacementTransform(circle0,  circle)) # , calC.animate.scale(2).move_to(LEFT*3))



        r1_line = Line(start=RIGHT*1.4+UP, end=RIGHT*1.6 + UP, color = YELLOW)
        r1 = MathTex("\\textrm{Sampling Radius, } r_1").move_to(LEFT*4).move_to(RIGHT*4+UP)

        dot = Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(RIGHT*2 + UP*3)
        dot_text = MathTex("\\textrm{Data Point, } D_i").move_to(RIGHT*4 + UP*3)


        self.add(circle)# , calC)
        self.add(dot, dot_text)

        # Number of points required
        #num_points = 60
        # Calculate each angle
        angles = [-24, -18, -12, -6, 0, 6, 12, 18, 24] #[n * (360 / num_points) for n in range(num_points)]
        angles_r8 = [-40, -30, -20, -10, 0, 10, 20, 30, 40]
        angles_r6 = [-80, -60, -40, -20, 0, 20, 40, 60, 80]
        angles_r4 = [-100, -75, -50, -25, 0, 25, 50, 75, 100]

        # Points on circumference of circle
        points_r9 = [circle_r9.point_at_angle(n*DEGREES) for n in angles]
        points_r8 = [circle_r8.point_at_angle(n*DEGREES) for n in angles_r8]
        points_r6 = [circle_r6.point_at_angle(n*DEGREES) for n in angles_r6]
        points_r4 = [circle_r4.point_at_angle(n*DEGREES) for n in angles_r4]


        # Create circles at each point
        circles_r9 = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points_r9]
        circles_r8 = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points_r8]
        circles_r6 = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points_r6]
        circles_r4 = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points_r4]

    
        # Add each of the points to the scene
        for idx, c in enumerate(circles_r9):
            self.add(c)
            self.add(circles_r8[idx])
            self.add(circles_r6[idx])
            self.add(circles_r4[idx])


        state_dot = Circle(radius=0.2, color=BLUE, fill_opacity=1).move_to(LEFT*3 + UP*2)
        dot_loc = state_dot.get_center()
        
        state_label = MathTex("\\mathbf{x}", color=WHITE).next_to(state_dot, 0.5*(RIGHT+DOWN))
        dist = np.linalg.norm(safeSet.get_center() - state_dot.get_center()) - 10 

        theta = -1.2*np.pi/(1 + np.exp(-dist))  - 0.2 
        k_expert  = Arrow(start=dot_loc, end=dot_loc + UP*np.sin(theta) + RIGHT*np.cos(theta), stroke_width=4, color=WHITE, max_stroke_width_to_length_ratio=10)
        k_expert.put_start_and_end_on( dot_loc, dot_loc + UP*np.sin(theta) + RIGHT*np.cos(theta))
        expert_tex = MathTex("\\textrm{Expert Controller, } \\mathbf{k}(\\mathbf{x})").next_to(dot_text, DOWN)
        expert_arr = Arrow(start=0.5*RIGHT, end=0.5*LEFT, stroke_width=4, color=WHITE, max_stroke_width_to_length_ratio=10).next_to(expert_tex, LEFT)

        theta = -0.9*np.pi/(1 + np.exp(-dist))
        k_learned = Arrow(start=dot_loc, end=dot_loc + UP*np.sin(theta) + RIGHT*np.cos(theta), stroke_width=4, color=YELLOW, max_stroke_width_to_length_ratio=10)
        k_learned.put_start_and_end_on( dot_loc, dot_loc + UP*np.sin(theta) + RIGHT*np.cos(theta))
        learned_tex = MathTex("\\textrm{Learned Controller, } \\mathbf{k}_\\theta (\\mathbf{x})").next_to(expert_tex, DOWN)
        learned_arr = Arrow(start=0.5*RIGHT, end=0.5*LEFT, stroke_width=4, color=YELLOW, max_stroke_width_to_length_ratio=10).next_to(learned_tex, LEFT)


        self.add(expert_arr, expert_tex, learned_arr, learned_tex)
        self.play(FadeIn(state_dot), FadeIn(state_label))
        self.play(Create(k_expert), FadeOut(state_label)) #Write(expert_tex), Create(expert_arr), FadeOut(state_label))
        self.play(Create(k_learned)) #, Write(learned_tex), Create(learned_arr))


        state = VGroup(state_dot, k_expert, k_learned)


        np.random.seed(4)

        self.time = 0 
        self.random_walk = [0,0]
        def move_state(mob, dt): 

            dist = np.linalg.norm(safeSet.get_center() - mob[0].get_center()) - 10 

            expert_theta = -1.2*np.pi/(1 + np.exp(-dist))  - 0.2 # sigmoid from 0 to -pi, minus 0.2

            if dist < 0: 
                learned_theta = -0.9*np.pi/(1 + np.exp(-dist))  # sigmoid from 0 to -0.9 pi 
                learned_mag = 1 - self.time/5
            else: 
                self.random_walk[0] += (np.random.rand()-0.6)*np.log(dist+1)*0.1
                self.random_walk[1] += (np.random.rand()-0.4)*np.log(dist+1)*0.1
                learned_theta = -0.9*np.pi/2 + 2*np.sin(np.log(dist+1)) + self.random_walk[0]
                learned_mag = 1 - self.time/5 +np.log(dist+1) + self.random_walk[1]

            expert_mag = 1 - self.time/3

            dx = learned_mag * dt/2 * np.array([ np.cos(learned_theta), np.sin(learned_theta), 0])

            loc = mob.get_center()
            mob.move_to(loc + dx)
            expert = mob[1]
            learned = mob[2]

            dot_loc = mob[0].get_center()

            self.time += dt*0.1
            learned.put_start_and_end_on( dot_loc, dot_loc + learned_mag*(UP*np.sin(learned_theta) + RIGHT*np.cos(learned_theta)))
            expert.put_start_and_end_on(dot_loc, dot_loc + expert_mag * (UP*np.sin(expert_theta) + RIGHT*np.cos(expert_theta)))

        
        state.add_updater(move_state)
        self.add(state)


        self.wait(18)


        #########################################################
        #########################################################
        