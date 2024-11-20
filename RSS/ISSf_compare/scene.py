from manim import *

from scipy.stats import truncnorm


WHITE_BACKGROUND = True
if WHITE_BACKGROUND:
    colors = [WHITE, BLACK, PURE_BLUE, "#019429", PURE_RED]
else:
    colors = [BLACK, WHITE, YELLOW, RED]

np.random.seed(0)



# Run Simulation
n_steps = 400
n_sims = 10
h0 = 10
alpha = 0.99
p = 1/6
sigma_step = np.sqrt(4/12)
n_plots = 400


def randomSample(n_sims, dist_type="uniform"):
    r = np.random.uniform(size=n_sims)
    if dist_type == "uniform": # uniform distribution
        return r*2 - 1
    elif dist_type == "trunc_norm": # truncated gausssian, variance = 0.29112509
        r = truncnorm.rvs(-1,1,size=n_sims)
    elif dist_type == "binary": # binary
        r = -1 * (r < p) + (p/(1-p)) * (r>=p)
    return r

# Define probability bounds
def Pu_Hoeff(K, x, sigma):
    if x <= K:
        frac1 = (sigma**2) / (x + sigma**2)
        exp1 = (x + sigma**2)
        if x < K:
            frac2 = (K) / (K - x)
            exp2 = (K - x)
        else:
            frac2 = 1
            exp2 = 1

        if frac1**exp1*frac2**exp2 < 1 :
            return (frac1**exp1*frac2**exp2)**(K/(K + sigma**2))
        else:
            return 1
    else:
        return 0


def Pu_Freedman(x, sigma):
    try:
        frac1 = (sigma**2) / (x + sigma**2)
        exp1 = (x + sigma**2)
    except:
        breakpoint()
    return frac1**exp1 * np.exp(x)

def Pu(K,x,sigma):
    return Pu_Freedman( x, sigma)


def run_sim(dist_type = "uniform"):

    ts = []
    trajs = np.zeros((n_sims, n_steps))
    x0 = np.ones(n_sims)*h0
    x_next = x0
    for i in range(n_steps):
        ts.append(i)
        r = randomSample(n_sims, dist_type)
        x_next = alpha*x_next + r
        trajs[:,i] = x_next
    return ts, trajs


class PlotScene(Scene):
    def construct(self):
        # Set background color to white
        self.camera.background_color = colors[0]

        # Create axes
        axes = Axes(
            x_range=(0, 100),
            y_range=(-0.1, 1),
            axis_config={"color": colors[1]},
            x_length=10,
            y_length=6,
            tips=True,
        )

    
        K_tag = MathTex("\\textup{Level Set Value, } \\delta").scale(0.8).move_to(axes.c2p(50, -0.1))
        K_tag.set_color(colors[1])
        value_tag = MathTex("\\mathbb{P}_\\textup{unsafe}(K, \\mathbf{x}_0) \\textup{ upper-bound}").scale(0.8).move_to(axes.c2p(-5, 0.5)).rotate(angle = PI/2)
        value_tag.set_color(colors[1])

        issf_tag = MathTex("\\textup{ISSF Probability Bound}").scale(0.8).move_to(axes.c2p(50, 0.6))
        issf_tag.set_color(colors[4])

        freedman_tag = MathTex("\\textup{Freedman Probability Bound}").scale(0.8).move_to(axes.c2p(50, 0.5))
        freedman_tag.set_color(colors[2])
               
        self.add(axes, K_tag, value_tag)



        dists = ["binary"] #"uniform", "trunc_norm", 
        if True:
            cs = np.linspace(0, 1/(1-alpha), 1000)


            for d_idx, dist in enumerate(dists):
                # ts, trajs = run_sim(dist)

                Ks = np.linspace(1, n_steps, n_plots)
                for i, k in enumerate(Ks):
                    probs = []
                    sum_quad_var = 0 
                    for i in range(int(k)):                
                        sum_quad_var += alpha**(2*(k -i) ) 

                    sigma = sigma_step*np.sqrt(sum_quad_var)
                    hmin = alpha**k*h0 + sum([-alpha**i for i in range(int(k)) ])
                    # hmin = min(hmin, 0 )
                    ps = []
                    # p_unsafe = []
                    for c in cs:
                        lambduh = alpha**k * (h0 + c )
                        if dist == "binary":
                            if -c < hmin:
                                ps.append(0)
                            else:
                                ps.append(Pu(k, lambduh, sigma))
                        # unsafe = np.sum(trajs[:,:int(k)] < -c, axis = 1)
                        # n_unsafe = np.sum(unsafe>0)
                        # p_unsafe.append(n_unsafe/n_sims)



                    # sim_lines = axes.plot_line_graph(x_values = cs.tolist(), y_values = p_unsafe)
                    # sim_lines.set_color(colors[3])


                    if dist == dists[-1]:
                        if hmin < 0:
                            issf_line = axes.plot_line_graph(x_values =[0, -hmin, -hmin, cs[-1]],y_values = [1,1,0,0], add_vertex_dots=False, stroke_width=10)
                        else:
                            issf_line = axes.plot_line_graph(x_values = [0, 0, 0, cs[-1]],y_values = [0,0,0,0], add_vertex_dots = False, stroke_width=10)
                        issf_line.set_color(colors[4])
                        p_line = axes.plot_line_graph(x_values = cs.tolist(), y_values =ps, add_vertex_dots = False, stroke_width=10)
                        p_line.set_color(colors[2])

                    time_tag = MathTex("K = "+str(int(k))).scale(0.8).move_to(axes.c2p(50, 1.1))
                    time_tag.set_color(colors[1])

                    if 'p_line_old' in locals():
                        self.play(ReplacementTransform(p_line_old, p_line),
                                ReplacementTransform(issf_line_old, issf_line),
                                ReplacementTransform(time_tag_old, time_tag),
                                run_time=0.05)
                    else: 
                        self.play(FadeIn(p_line), FadeIn(issf_line), FadeIn(time_tag), FadeIn(issf_tag), FadeIn(freedman_tag), run_time=0.5)
                    # sim_line_old = sim_lines
                    p_line_old = p_line
                    issf_line_old = issf_line
                    time_tag_old = time_tag
                    # self.wait(1)
                # axs[i].set_box_aspect(1)

        self.wait(5)



# Render the scene
if __name__ == "__main__":
    config = {
        "frame_width": 800,
        "frame_height": 400,
        "background_color": colors[0]
    }
    renderer = renderer = renderer = VideoRenderer(config=config)
    renderer.render(PlotScene())
