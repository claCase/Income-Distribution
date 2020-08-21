import numpy as np
import os
import matplotlib.pyplot as plt
import tqdm
import argparse
import matplotlib.animation as animation

cwd = os.getcwd()
parser = argparse.ArgumentParser()
parser.add_argument("--iter", type=int, default=100000)
parser.add_argument("--agents", type=int, default=1000)
parser.add_argument("--endow", type=int, default=100)
parser.add_argument("--show", type=bool, default=False)
parser.add_argument("--save", type=bool, default=False)
parser.add_argument("--l", type=float, default=1)
parser.add_argument("--exp", type=bool, default=False)
parser.add_argument("--mu", type=float, default=1)
parser.add_argument("--sigma", type=float, default=1)
parser.add_argument("--normal", type=bool, default=False)
parser.add_argument("--a", type=float, default=0)
parser.add_argument("--b", type=float, default=1)
parser.add_argument("--unif", type=bool, default=False)
parser.add_argument("--const", type=float, default=1)
parser.add_argument("--test_all", type=bool, default=False)
args = parser.parse_args()
iterations = args.iter
agents_n = args.agents
initial_endowment = args.endow
show = args.show
save = args.save
l = args.l
exp = args.exp
mu = args.mu
sigma = args.sigma
normal = args.normal
a = args.a
b = args.b
unif = args.unif
const = args.const
test_all = args.test_all


def positive_normal(mean, sigma):
    x = np.random.normal(mean, sigma, 1)
    return x if x >= 0 else positive_normal(mean, sigma)


def amount(distribution):
    if distribution == "exp":
        return np.random.exponential(l)
    elif distribution == "normal":
        return positive_normal(mu, sigma)
    elif distribution == "unif":
        return np.random.uniform(a, b)
    elif distribution == "const":
        return const


if test_all:
    distributions = ["exp", "normal", "unif", "const"]
    print("AGENTS: {}\nTRANSACTIONS: {}".format(agents_n, iterations))
else:
    distributions = [
        "exp" if exp else ("normal" if normal else ("unif" if unif else "const"))
    ]
for dist in distributions:
    agents = np.ones(agents_n) * initial_endowment  # equal initial endowment
    idx = np.arange(agents_n)
    agents_history = np.empty((1, agents_n))
    print("\nDistribution: {}".format(dist))
    progress = tqdm.tqdm(total=iterations)
    for i in range(iterations):
        # Make transactions between two randomly chosen agents
        ag1 = np.random.choice(idx)
        ag2 = np.random.choice(idx)
        am1 = amount(distribution=dist)
        if agents[ag1] > am1:
            agents[ag1] -= am1
            agents[ag2] += am1

        if not i % 10000:
            agents_history = np.vstack((agents_history, agents))
            progress.update(n=10000)

    progress.close()

    # PLOT DISTRIBUTION
    fig, ax = plt.subplots(figsize=(10, 10))

    def update(i):
        ax.clear()
        ax.set_title("Money Distribution at time {}".format(i), fontsize=30)
        ax.set_xlabel("Income", fontsize=20)
        ax.set_ylabel("Probability", fontsize=20)
        ax.hist(agents_history[i], 25, density=True)

    if save:
        i = 1
        path = os.path.join(cwd, "figures")
        while os.path.exists(os.path.join(path, str(i))):
            i += 1
        path = os.path.join(path, str(i))
        os.mkdir(path)
    anim = animation.FuncAnimation(
        fig, update, frames=len(agents_history) - 1, repeat=False
    )
    writer = animation.FFMpegWriter(50)
    if save:
        anim.save(os.path.join(path, "animation.mp4"), writer=writer)
        print("mp4 saved to {}".format(os.path.join(path, "animation.mp4")))
    if show:
        plt.show()
    plt.close()

    fig, ax = plt.subplots(2, 1, figsize=(5, 10))
    ax[0].set_title("Money Frequency Distribution")
    ax[1].set_title("Money Cumulative Distribution")
    ax[0].hist(np.mean(agents_history[-5:], axis=0), 25, density=True)
    ax[1].hist(np.mean(agents_history[-5:], axis=0), 25, density=True, cumulative=True)

    if save:
        plt.savefig(os.path.join(path, "money_dist.png"))
        print("figure saved to {}".format(os.path.join(path, "money_dist.png")))
        with open(os.path.join(path, "settings.txt"), "wb") as file:
            settings = (
                "Transactions {} \n".format(iterations)
                + "Agents {} \n".format(agents_n)
                + "Distribution {} \n".format(dist)
            )
            file.write(str.encode(settings))
    if show:
        plt.show()
    plt.close()
