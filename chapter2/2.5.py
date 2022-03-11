import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm



class arm:
    def __init__(self, q):
        self.q_star = q
    
    def random_walk(self):
        self.q_star += np.random.normal(0, 0.01)

    def pull(self):
        return np.random.normal(self.q_star, 1)

def random_walk_all_arm(arm_list) :
    for bandit in arm_list:
        bandit.random_walk()

def update_approx_q_average(q_approx_list, count_list, idx, r):
    count_list[idx] += 1
    q_approx_list[idx] = q_approx_list[idx] + (r -  q_approx_list[idx])/count_list[idx]


def update_approx_q_fixed_step(q_approx_list, count_list, idx, r):
    count_list[idx] += 1
    q_approx_list[idx] = q_approx_list[idx] + 0.1 * (r -  q_approx_list[idx])

def main_average(steps,episode_length, interval):
    """
    10-arm bandit
    """
    np.random.seed(0)
    random.seed(0)
    epsilon = 0.1
    init_q_star = 1
    
    # 初始化为0
    q_approx_list_average = [0.0 for _ in range(10)]
    count_list = [ 0 for _ in range(10) ]
    r_list = []

    arm_list = []
    for _ in range(10):
        arm_list.append(arm(init_q_star))
    
    for i in tqdm(range(steps)):
        avg_reward = 0.
        for k in range(episode_length):
            if random.random() <= epsilon: # exploration
                idx = random.randint(0,9)
            else:
                idx = np.argmax(q_approx_list_average)
            
            r = arm_list[idx].pull()
            update_approx_q_average(q_approx_list_average, count_list, idx, r)
            random_walk_all_arm(arm_list)
            avg_reward += r
        avg_reward /= episode_length

        r_list.append(avg_reward)
    return r_list

def main_fixed_stepsize(steps, episode_length, interval):
    """
    10-arm bandit
    """
    np.random.seed(0)
    random.seed(0)
    epsilon = 0.1
    init_q_star = 1
    
    # 初始化为0
    q_approx_list_fixed_step = [0.0 for _ in range(10)]
    count_list = [ 0 for _ in range(10) ]
    r_list = []

    arm_list = []
    for _ in range(10):
        arm_list.append(arm(init_q_star))
    
    for i in tqdm(range(steps)):
        avg_reward = 0.
        for k in range(episode_length):
            if random.random() <= epsilon: # exploration
                idx = random.randint(0,9)
            else:
                idx = np.argmax(q_approx_list_fixed_step)
            
            r = arm_list[idx].pull()
            update_approx_q_fixed_step(q_approx_list_fixed_step, count_list, idx, r)
            random_walk_all_arm(arm_list)
            avg_reward += r
        avg_reward /= episode_length

        r_list.append(avg_reward)
    return r_list



        


if __name__=="__main__":
    steps = 50_000
    episode_length=100
    interval=1
    r_average = main_average(steps, episode_length, interval)
    r_fixed = main_fixed_stepsize(steps, episode_length, interval)

    plt.figure()
    plt.plot(r_fixed, color="red", label="fixed step size")
    plt.plot(r_average, color="blue", label="moving average")
    plt.legend()
    plt.savefig("result.jpg")
    plt.show()

