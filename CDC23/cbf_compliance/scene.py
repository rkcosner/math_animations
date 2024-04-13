from manim import *
import numpy as np 



class cbf_compliance(Scene):
    def construct(self):
                
        circle0=Circle(color=WHITE, radius=2).set_opacity(0)
        circle0.set_fill(GREEN, opacity=0.5)


        circle=Circle(color=WHITE, radius=10).set_opacity(0)
        circle.set_fill(GREEN, opacity=0.5).move_to(LEFT*10)

        calC = MathTex("\\mathcal{C}")#.move_to(LEFT*4).scale(2)
        self.add(circle0, calC)


        self.play(Wait(1))

        self.play(ReplacementTransform(circle0,  circle), calC.animate.scale(2).move_to(LEFT*3))



        r1_line = Line(start=RIGHT*1.4+UP, end=RIGHT*1.6 + UP, color = YELLOW)
        r1 = MathTex("\\textrm{Sampling Radius, } r_1").move_to(LEFT*4).move_to(RIGHT*4+UP)

        dot = Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(RIGHT*2 + UP*2)
        dot_text = MathTex("\\textrm{Data Point, } D_i").move_to(RIGHT*4 + UP*2)


        self.add(circle, calC)

        # Number of points required
        #num_points = 60
        # Calculate each angle
        angles = [-24, -18, -12, -6, 0, 6, 12, 18, 24] #[n * (360 / num_points) for n in range(num_points)]
        # Points on circumference of circle
        points = [circle.point_at_angle(n*DEGREES) for n in angles]
        radii = [Line(  start=circle.point_at_angle(n*DEGREES), 
                        end=circle.point_at_angle(n*DEGREES)+RIGHT*0.53, 
                        color=YELLOW
                    )
                for n in angles]
                

        # Create circles at each point
        circles = [Circle(radius=0.1, color=ORANGE, fill_opacity=1).move_to(p) for p in points]
        outers = [Circle(radius=0.53, color=GREY, fill_opacity=0).move_to(p) for p in points]
        
        # Add each of the points to the scene
        self.play(Write(dot), Write(dot_text), run_time = 0.5)
        for c in circles:
            self.play(Write(c), run_time=0.1)

        
        self.play(Write(r1), Write(r1_line), run_time = 0.5)
        for i in range(len(radii)): 
            self.play(Write(radii[i]), Write(outers[i]), run_time=0.5)


        self.play(Wait(3))

        for i in range(len(radii)): 
            self.play(FadeOut(radii[i]), FadeOut(outers[i]), run_time=0.5)
        self.play(FadeOut(r1), FadeOut(r1_line), run_time = 0.5)


        #########################################################
        #########################################################

        