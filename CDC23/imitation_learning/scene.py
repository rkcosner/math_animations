from manim import *
import numpy as np 



class imitation_learning(Scene):
    def construct(self):
                
        circle0=Circle(color=WHITE, radius=2).set_opacity(0)
        circle0.set_fill(GREEN, opacity=0.5).move_to(3*LEFT)

        circle_r1 = Circle(radius=1).set_opacity(0).move_to(3*LEFT)
        hline = Line(start=RIGHT*1+UP*1, end=RIGHT*6.5+UP*1, color=GREY)

        self.add(circle0, hline) #, calC)

        dot = Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(RIGHT*2 + UP*3)
        dot_text = MathTex("\\textrm{Data Point, } D_i").move_to(RIGHT*4 + UP*3)
        expert_tex = MathTex("\\textrm{Expert Controller, } \\mathbf{k}(\\mathbf{x})").next_to(dot_text, DOWN)
        expert_arr = Arrow(start=0.5*RIGHT, end=0.5*LEFT, stroke_width=4, color=WHITE, max_stroke_width_to_length_ratio=10).next_to(expert_tex, LEFT)
        learned_tex = MathTex("\\textrm{Learned Controller, } \\mathbf{k}_\\theta (\\mathbf{x})").next_to(expert_tex, DOWN)
        learned_arr = Arrow(start=0.5*RIGHT, end=0.5*LEFT, stroke_width=4, color=YELLOW, max_stroke_width_to_length_ratio=10).next_to(learned_tex, LEFT)

        self.add(circle0)

        # Number of points required
        #num_points = 60
        # Calculate each angle

        num_points = 10 
        angles = [n * (360 / num_points) for n in range(num_points)]
        num_points = 5 
        angles_r1 = [n * (360 / num_points) for n in range(num_points)]

        # Points on circumference of circle
        points = [circle0.point_at_angle(n*DEGREES) for n in angles]
        points_r1 = [circle_r1.point_at_angle(n*DEGREES) for n in angles_r1]

        # Create circles at each point
        circles = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points]
        circles_r1 = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points_r1]
        

        # Add each of the points to the scene
        self.add(dot, dot_text, expert_arr, expert_tex, learned_arr, learned_tex)
        # self.play(Write(dot), Write(dot_text), run_time = 0.5)
        mid_circle = Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(3*LEFT)
        actions = []
        for idx, c in enumerate(circles):
            self.add(c)
        for idx, c in enumerate(circles_r1):
            self.add(c)
        self.add(mid_circle)

        # self.play(*actions)

        self.wait(1)



        def random_vec(): 
            magnitude = np.random.rand()*0.5 + 0.25
            theta = 2*np.pi*np.random.rand()
            vec = magnitude * (UP*np.sin(theta) + RIGHT*np.cos(theta))
            return vec


        points.extend(points_r1)
        points.extend([ORIGIN + 3*LEFT])

        k_experts = [Arrow(stroke_width = 2, color=WHITE, tip_length = 0.1, max_stroke_width_to_length_ratio =10).put_start_and_end_on( p, p + random_vec()) for p in points]


        # self.play(Write(expert_tex), Create(expert_arr))

        actions = [Create(k) for k in k_experts]
        self.play(*actions)

        def mean0unif(): 
            return (np.random.rand()-0.5)*2

        def get_similar_vec(v, scale): 
            theta = v.get_angle() + scale*mean0unif()*np.pi
            mag = np.linalg.norm(v.get_vector()) + mean0unif()*scale
            vec = (RIGHT*np.cos(theta)  + UP*np.sin(theta)) * mag
            return vec 

        def get_error(expert, learned): 
            errors = []
            for idx in range(len(expert)): 
                errors.append(np.linalg.norm(expert[idx].get_vector() - learned[idx].get_vector()))
            errors = np.array(errors)
            return np.mean(errors)

        k_learned = [Arrow(stroke_width = 2, color=YELLOW, tip_length = 0.1, max_stroke_width_to_length_ratio =10).put_start_and_end_on(p,p+get_similar_vec(k_experts[idx], 1.6)) for idx, p in enumerate(points)]        


        # self.play(Create(learned_arr), Write(learned_tex))


        actions = [Create(k) for k in k_learned]
        self.play(*actions)



        ax = Axes(
            x_range=[0,6,1], 
            y_range=[0,1.2],
            y_length=5
        ).move_to(RIGHT*4+DOWN*1.1).scale(0.4)
        loss_tex = MathTex("\\textrm{Loss, } \\mathcal{L}(\\mathbf{k}(\\mathbf{x}), \\mathbf{k}_\\theta(\\mathbf{x}))").next_to(ax, UP)
        x_label = MathTex("\\textrm{Learning Step}").next_to(ax, DOWN/2).scale(0.75)
        self.play(Write(ax), Write(loss_tex), Write(x_label))
        

        loss = get_error(k_experts, k_learned)
        dot = Dot(ax.coords_to_point(0, loss), color=WHITE)
        self.play(Write(dot))

        dots = [dot]
        lines = []
        for i, scale in enumerate([0.8, 0.4, 0.2, 0.1, 0.05, 0.025]): 
            actions = []
            for idx, k in enumerate(k_learned): 
                actions.append(k.animate.put_start_and_end_on(points[idx], points[idx] + get_similar_vec(k_experts[idx],scale)))
            
            loss = get_error(k_experts, k_learned)
            dots.append(Dot(ax.coords_to_point(i+1, loss), color=WHITE))
            line = Line(start=dots[-2].get_center(), end=dots[-1].get_center())
            lines.append(line)
            self.play(*actions,run_time=2)
            self.play( Write(dots[-1]), Write(line), run_time=0.5)


        self.wait(1)

        actions = [FadeOut(ax), FadeOut(dots[0]), FadeOut(loss_tex), FadeOut(x_label)]
        for i in range(len(lines)): 
            actions.extend([FadeOut(lines[i]), FadeOut(dots[i+1])])

        for idx, k in enumerate(k_experts): 
            actions.extend([FadeOut(k), FadeOut(k_learned[idx])])

        self.play(*actions)        

        #########################################################
        #########################################################
        