from lib2to3.pgen2.token import NEWLINE
from manim import *

class ZoHAnimation(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        legend1 = Text("Continuous Signal", color= YELLOW_D).scale(0.5).next_to(np.array([2,3,0]))
        self.add(legend1)
        legend2 = Text("Actual Signal", color=RED_D).scale(0.5).next_to(legend1, DOWN)
        self.add(legend2)
        legend3 = Text("Discrete Jumps", color=BLUE).scale(0.5).next_to(legend2, DOWN)
        self.add(legend3)
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4,0,0])
        self.curve_start = np.array([-4,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex("1"), MathTex("2"),
            MathTex("3"), MathTex("4"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-2 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

        x_label_text = Text("Time").scale(0.5).next_to(np.array([5, -0.1, 0]), UP)
        self.add(x_label_text)

        y_label_text = Text("Signal").scale(0.5).rotate(PI/2)
        y_label_text.next_to(np.array([-4.75, 1.25, 0]))
        self.add(y_label_text)

    def move_dot_and_draw_curve(self):

        dot = Dot(radius=0.05, color=YELLOW)
        self.t_int = 0
        self.x_offset = -4.0
        self.dt = 0.01

        def go_around_circle(mob, dt):
            self.t_int += 1
            mob.move_to(np.array([self.t_int*self.dt*4 + self.x_offset, 2*np.sin(np.pi*self.t_int*self.dt), 0.0]))


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_int * self.dt * 4 
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        self.zoh = VGroup()
        self.zoh.add(Line(self.curve_start,self.curve_start))
        def get_zoh_curve():
            last_line = self.zoh[-1]


            if self.t_int % 10 == 0: 
                last_point = last_line.get_end()
                x = last_point[0] + self.dt#self.curve_start[0] + self.t_int * self.dt * 4 
                y = last_point[1]#2*np.sin(np.pi*(self.t_int * self.dt - 0.1))
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=RED_D)
                self.zoh.add(new_line)
                last_line = self.zoh[-1]

                x = self.curve_start[0] + self.t_int * self.dt * 4 
                y = 2*np.sin(np.pi*np.floor(self.t_int * self.dt *10)/10 )
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=BLUE)
                self.zoh.add(new_line)
            else:
                x = self.curve_start[0] + self.t_int * self.dt * 4 
                y = 2*np.sin(np.pi*np.floor(self.t_int * self.dt * 10)/10 )
                new_line = Line(last_line.get_end(),np.array([x,y,0]), color=RED_D)
                self.zoh.add(new_line)

            return self.zoh

        dot.add_updater(go_around_circle)

        # origin_to_circle_line = always_redraw(get_line_to_circle)
        # dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)
        zoh_curve = always_redraw(get_zoh_curve)
        
        self.add(zoh_curve)
        self.add(sine_curve_line)
        self.add(dot)
        self.wait(15)

        dot.remove_updater(go_around_circle)