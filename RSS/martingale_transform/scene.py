from manim import *



WHITE_BACKGROUND = True
if WHITE_BACKGROUND:
    colors = [WHITE, BLACK, PURE_BLUE, "#019429", PURE_RED]
else:
    colors = [BLACK, WHITE, YELLOW, RED]

np.random.seed(0)

class PlotScene(Scene):
    def construct(self):
        # Set background color to white
        self.camera.background_color = colors[0]

        # Create axes
        axes = Axes(
            x_range=(0, 25),
            y_range=(-5, 10),
            axis_config={"color": colors[1]},
            x_length=10,
            y_length=6,
            tips=True,
        )

        # Add axes and graph to the scene
        
        M = 8
        alpha = 0.9
        K = 25
        N = 10

        self.h = [[M for i in range(K)] for j in range(N)]
        h_lines = [[0 for i in range(K)] for j in range(N)]
        w_lines = [[0 for i in range(K)] for j in range(N)]
        creations = [0 for j in range(N)]
        w_creations = [0 for j in range(N)]


        for i in range(N): 
            for j in range(1, K):
                self.h[i][j] = alpha*self.h[i][j-1] + np.random.normal(0, 0.5)
                W_last = -self.h[i][j-1]*alpha**(K-j)     + alpha**K*M  #- sum([alpha**(K-k) for k in range(1,i)])  
                W =      -self.h[i][j]*alpha**(K-(j+1))   + alpha**K*M  #- sum([alpha**(K-k) for k in range(1,i+1)])
                W_last /= 0.25
                W /= 0.25
                w_lines[i][j] = W                


            creations[i] = axes.plot_line_graph(x_values = [i for i in range(K)], y_values = self.h[i])
            creations[i].set_color(colors[2])
            w_creations[i] = axes.plot_line_graph(x_values = [i for i in range(K)], y_values = w_lines[i])
            w_creations[i].set_color(colors[3])
            # self.play(  creations[i][0], 
            #             creations[i][1], 
            #             creations[i][2], 
            #             creations[i][3], 
            #             creations[i][4], 
            #             creations[i][5], 
            #             creations[i][6], 
            #             creations[i][7], 
            #             creations[i][8], 
            #             creations[i][9],  
            #             run_time=0.125)

    

        h_tag = MathTex("\\textup{DTCBF, }h(\\mathbf{x}_k)").move_to(axes.c2p(13, 9))
        h_tag.set_color(colors[2])
        K_tag = MathTex("\\textup{Time, }k").scale(0.8).move_to(axes.c2p(27, -1))
        K_tag.set_color(colors[1])
        value_tag = MathTex("\\textup{Value}").scale(0.8).move_to(axes.c2p(-1, 6)).rotate(angle = PI/2)
        value_tag.set_color(colors[1])
               
        self.add(axes, K_tag, value_tag)

        self.play(*[FadeIn(c) for c in creations], Write(h_tag), run_time=1)
        self.wait(3)

        h_safety_line = axes.plot_line_graph(x_values = [0,K], y_values = [0,0])
        h_safety_line.set_color(colors[4])
        h_criterion = MathTex("h(\\mathbf{x}) \\geq 0  \\textup{ safety criterion}").scale(0.8).move_to(axes.c2p(6, -1))
        h_criterion.set_color(colors[4])

        locs = [i for i in range(24)]
        arrows = []
        for loc in locs:
            arrow = Arrow(start=axes.c2p(loc, 0), end=axes.c2p(loc, 2), color=colors[4])
            arrows.append(arrow)

        self.play( Create(h_safety_line), Write(h_criterion),*[Write(a) for a in arrows], run_time = 1)
        self.wait(3)    
        self.play(*[FadeOut(a) for a in arrows], run_time=1)
        self.wait(2)

        
        w_tag = MathTex("\\textup{Martingale, }W_k = -\\alpha^{K-k} h(\\mathbf{x}_k)  + \\alpha^Kh(\\mathbf{x}_0)").move_to(axes.c2p(13, 9))
        w_tag.set_color(colors[3])

        animations = []
        for i in range(0, N):
            animations.append(ReplacementTransform(creations[i], w_creations[i]))
        self.play( *animations, ReplacementTransform(h_tag, w_tag),  run_time=1.5)

        safety_line = axes.plot_line_graph(x_values=[0,K], y_values=[alpha**K*M/0.25, alpha**K*M/0.25]) #Line(axes.c2p(0,alpha**K*M/0.5), axes.c2p(K,alpha**K*M/0.5), color=colors[3])
        safety_line.set_color(colors[4])

        w_criterion = MathTex("W <\\alpha^K h(\\mathbf{x}_0)  \\textup{ safety criterion}").scale(0.8).move_to(axes.c2p(8, 0.75 + alpha**K*M/0.25))
        w_criterion.set_color(colors[4])

        self.play(ReplacementTransform(h_safety_line, safety_line), ReplacementTransform(h_criterion, w_criterion), run_time = 2)

        locs = [i for i in range(24)]
        arrows = []
        for loc in locs:
            arrow = Arrow(start=axes.c2p(loc, alpha**K*M/0.25 + 0.5), end=axes.c2p(loc, alpha**K*M/0.25-2 + 0.5), color=colors[4])
            arrows.append(arrow)

        self.play(*[Write(a) for a in arrows], run_time = 1)
        self.wait(3)    
        self.play(*[FadeOut(a) for a in arrows], run_time=1)

        self.wait(3)

        self.play(*[FadeOut(c) for c in w_creations], FadeOut(w_tag), FadeOut(safety_line), FadeOut(w_criterion), run_time=1.5)




# Render the scene
if __name__ == "__main__":
    config = {
        "frame_width": 800,
        "frame_height": 400,
        "background_color": colors[0]
    }
    renderer = renderer = renderer = VideoRenderer(config=config)
    renderer.render(PlotScene())
