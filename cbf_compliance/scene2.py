from manim import *
import numpy as np 



class property2(Scene):
    def construct(self):
                
        circle=Circle(color=WHITE, radius=2).set_opacity(0)
        circle.set_fill(GREEN, opacity=0.5).move_to(LEFT*4+DOWN)

        axis = Axes(
                        x_range=[0, 1, 0.1], 
                        y_range=[0, 1, 1], 
                        tips = True, 
                        x_length = 6.5, 
                        y_length = 4
        ).move_to(RIGHT*3.5)


        calC = MathTex("\\mathcal{C}").move_to(circle)

        self.play(Create(circle), Create(axis), Write(calC))

        x_label = MathTex("\\textrm{Data Point Index, } i").move_to(RIGHT*3 + DOWN*2.5).scale(1)
        # title = MathTex("\\Vert \\mathbf{k}_T(\\mathbf{x}) - \\mathbf{k}_\\theta (\\mathbf{c}(\\mathbf{x})) \\Vert  \\textrm{ for } \\mathbf{x} \\textrm{ in the dataset } \\mathcal{D}", color=BLUE).move_to(RIGHT*3.3 + UP*2.5).scale(1)
        title = MathTex("\\textrm{Learning Error for } \\mathbf{x} \\textrm{ in } \\mathcal{D}").move_to(RIGHT*3.3 + UP*2.5).scale(1)

        self.play(Write(x_label), Write(title))


        bound_line = DashedLine(start=UP*1+LEFT*0.5, end=UP*1+RIGHT*6.5, color=RED)
        bound_text = MathTex("\\textrm{Error Bound, } M_e", color=RED).move_to(RIGHT*3 + UP*1.3).scale(1)
        self.play(Write(bound_line), Write(bound_text))


        dot = Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(LEFT*5.5 + UP*3).scale(1)
        dot_text = MathTex("\\textrm{Data Point, } D_i").next_to(dot, RIGHT)
        self.play(Create(dot), Write(dot_text))


        self.play(Wait(2))

        #########################################################
        #########################################################

        # Number of points required
        num_points = 10
        # Calculate each angle
        angles = [n * (360 / num_points) for n in range(num_points)]
        # Points on circumference of circle
        points = [circle.point_at_angle(n*DEGREES) for n in angles]
        # Create circles at each point
        circles = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points]

        error_locs = [  [RIGHT*(0+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7],
                        [RIGHT*(1+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(2+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(3+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(4+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(5+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(6+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(7+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(8+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        [RIGHT*(9+0)*0.65+RIGHT*0.3 + UP*(np.random.rand()-0.5)*1.7], 
                        ]

        errs =  [Circle(radius=0.1, color=BLUE, fill_opacity=1).move_to(loc) for loc in error_locs]


        def mean0unif(): 
            return (np.random.rand()-0.5)*2

        def random_vec(): 
            magnitude = np.random.rand()*0.5 + 0.25
            theta = 2*np.pi*np.random.rand()
            vec = magnitude * (UP*np.sin(theta) + RIGHT*np.cos(theta))
            return vec

        def get_similar_vec(v, scale): 
            theta = v.get_angle() + scale*mean0unif()*np.pi
            mag = np.linalg.norm(v.get_vector()) + mean0unif()*scale
            vec = (RIGHT*np.cos(theta)  + UP*np.sin(theta)) * mag
            return vec 

        expert_tex = MathTex("\\textrm{Expert Controller, } \\mathbf{k}(\\mathbf{x})").next_to(dot_text, DOWN)
        expert_arr = Arrow(start=0.5*RIGHT, end=0.5*LEFT, stroke_width=4, color=WHITE, max_stroke_width_to_length_ratio=10).next_to(expert_tex, LEFT)
        learned_tex = MathTex("\\textrm{Learned Controller, } \\mathbf{k}_\\theta (\\mathbf{x})").next_to(expert_tex, DOWN)
        learned_arr = Arrow(start=0.5*RIGHT, end=0.5*LEFT, stroke_width=4, color=YELLOW, max_stroke_width_to_length_ratio=10).next_to(learned_tex, LEFT)

        self.play(Write(expert_tex), Create(expert_arr))
        self.play(Write(learned_tex), Create(learned_arr))


        p_center = circle.get_center()

        for idx, c in enumerate(circles): 
            p = c.get_center()
            k_expert = Arrow(stroke_width = 2, color=WHITE, tip_length = 0.1, max_stroke_width_to_length_ratio =10).put_start_and_end_on( p, (p_center-p)*0.15 + p + random_vec()*0.25) 
            k_learned = Arrow(stroke_width = 2, color=YELLOW, tip_length = 0.1, max_stroke_width_to_length_ratio =10).put_start_and_end_on(p,p+get_similar_vec(k_expert, 0.5))

            self.play(Write(c), Write(errs[idx]), Write(k_expert), Write(k_learned),  run_time=0.5)
            self.play(Wait(0.25))
            


        self.play(Wait(2))
        