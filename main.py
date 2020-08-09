import numpy as np 
import os 
import matplotlib.pyplot as plt
import tqdm 
import argparse 
import matplotlib.animation as animation

cwd = os.getcwd()
parser = argparse.ArgumentParser()
parser.add_argument("--iter", type=int, default = 100000)
parser.add_argument("--agents", type=int, default = 1000)
parser.add_argument("--endow", type=int, default = 100)
parser.add_argument("--show", type=bool, default = False)
parser.add_argument("--save", type=bool, default = False)
args = parser.parse_args()
iterations = args.iter
agents_n = args.agents
initial_endowment = args.endow
show = args.show
save = args.save
amount = 1
agents = np.ones(agents_n)*initial_endowment #equal initial endowment 
idx = np.arange(agents_n)
agents_history = np.empty((1, agents_n))
progress = tqdm.tqdm(total=iterations)

for i in range(iterations):
	# Make transactions between two randomly chosen agents
	ag1 = np.random.choice(idx)
	ag2 = np.random.choice(idx)
	
	if agents[ag1] > amount:
		agents[ag1] -= 1 
		agents[ag2] += 1

	if not i%10000:
		agents_history = np.vstack((agents_history, agents))
	progress.update(n=1)

progress.close()

#PLOT Distributions
fig, ax = plt.subplots(1,1, figsize=(10,10))

def update(i):
	ax.clear()
	ax.set_title("Money Distribution at time {}".format(i), fontsize=30)
	ax.set_xlabel("Income", fontsize=20)
	ax.set_ylabel("Probability", fontsize=20)
	ax.hist(agents_history[i], 20, density=True)

if save:
	anim = animation.FuncAnimation(fig, update, frames=len(agents_history)-1, repeat=False)
	writer = animation.FFMpegWriter(50)
	anim.save(os.path.join(cwd, "figures", "animation.mp4"), writer=writer)
if show:
	plt.show()

fig, ax = plt.subplots(2,1, figsize=(5,10))
ax[0].set_title("Money Frequency Distribution")
ax[1].set_title("Money Cumulative Distribution")
ax[0].hist(np.mean(agents_history[-5:], axis=0), 20, density=True)
ax[1].hist(np.mean(agents_history[-5:], axis=0), 20, density=True, cumulative=True)

if save:
	i = 0
	path = os.path.join(cwd, "figures")
	while os.path.exists(os.path.join(path, str(i) + "_iter_" + str(iterations) + "_ag_"+ str(agents_n) + ".png")):
		i+=1
	path = os.path.join(path, str(i) + "_iter_" + str(iterations) + "_ag_"+ str(agents_n) + ".png")
	plt.savefig(path)
	print("figure saved to {}".format(path))
if show:
	plt.show()