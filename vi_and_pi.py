### MDP Value Iteration and Policy Iteration

import numpy as np
import gym

env_dict = gym.envs.registration.registry.env_specs.copy()

for env in env_dict:
    if 'Deterministic-4x4-FrozenLake-v0' in env:
        print("Remove {} from registry".format(env))
        del gym.envs.registration.registry.env_specs[env]
    if 'Deterministic-8x8-FrozenLake-v0' in env:
        print("Remove {} from registry".format(env))
        del gym.envs.registration.registry.env_specs[env]
    if 'Stochastic-4x4-FrozenLake-v0' in env:
        print("Remove {} from registry".format(env))
        del gym.envs.registration.registry.env_specs[env]

import time
from lake_envs import *
import random

np.set_printoptions(precision=3)

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

def policy_evaluation(P, nS, nA, value_function, policy, gamma=0.9, tol=1e-3):
    """Evaluate the value function from a given policy.

    Parameters
    ----------
    P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
    """
    ############################
    # YOUR IMPLEMENTATION HERE #
    while True:
        new_v_function = np.copy(value_function)
        for s, a in enumerate(policy):
            prob, next_s, reward, terminal = P[s][a][0]
            new_v_function[s] = reward + gamma * prob * value_function[next_s]
            value_change = np.sum(np.abs(value_function - new_v_function))
            
        value_function = new_v_function
        print(new_v_function)
        if value_change < tol:
            break
    return value_function

def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
    """Given the value function from policy improve the policy.

    Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

    Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""

    new_policy = np.copy(policy) # Important

    ############################
    # YOUR IMPLEMENTATION HERE #
    for s in range(nS):
        Q = []
        for a in range(nA):
            prob, next_s, reward, terminal = P[s][a][0]
            Q.append(reward + gamma * prob * value_from_policy[next_s])
        new_policy[s] = np.argmax(Q)
	############################
    return new_policy

def policy_iteration(P, nS, nA, gamma=0.9, max_iteration = 20, tol=10e-3):
    """Runs policy iteration.

	You should call the policy_evaluation() and policy_improvement() methods to
	implement this method.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		tol parameter used in policy_evaluation()
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
    """
    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)

    ############################
    # YOUR IMPLEMENTATION HERE #
    while True:
		# Policy evaluation
        value_function = policy_evaluation(P, nS, nA, value_function, policy, gamma, tol)
		# Policy improvement
        new_policy = policy_improvement(P, nS, nA, value_function, policy, gamma)
        policy_change = (new_policy != policy).sum()
        #print('policy changed in %d states' % (policy_change))
        policy = new_policy
        if policy_change == 0:
            break
	############################
    return value_function, policy

def value_iteration(P, nS, nA, gamma=0.9, max_iteration = 20, tol=1e-3):
    """
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		Terminate value iteration when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
    """

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)

    while True:
        new_v_function = np.copy(value_function)
        for s in range(nS):
            Q = np.zeros(nA, dtype = float)
            for action in range(nA):
                result = P[s][action]
                for num in range(len(result)):
                    prob, nexts, reward, terminal = result[num]
                    Q[action] = reward+prob*gamma*value_function[nexts]
            new_v_function[s] = np.max(Q)
            policy[s] = np.argmax(Q) 
        value_change = np.sum(np.abs(new_v_function-value_function)) 
        value_function = new_v_function
        if value_change < tol:
            break                       
            
    return value_function, policy

def render_single(env, policy, max_steps=100):
  """
    This function does not need to be modified
    Renders policy once on environment. Watch your agent play!

    Parameters
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as
      attributes.
    Policy: np.array of shape [env.nS]
      The action to take at a given state
  """

  episode_reward = 0
  ob = env.reset()
  for t in range(max_steps):
    env.render()
    time.sleep(0.25)
    a = policy[ob]
    ob, rew, done, _ = env.step(a)
    episode_reward += rew
    if done:
      break
  env.render();
  if not done:
    print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
  else:
  	print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":

    # comment/uncomment these lines to switch between deterministic/stochastic environments
    env = gym.make("Deterministic-4x4-FrozenLake-v0")
    #env = gym.make("Stochastic-4x4-FrozenLake-v0")

    print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)

    V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, max_iteration = 1000, tol=1e-3)
    render_single(env, p_pi, 100)

    print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)

    V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, max_iteration = 20, tol=1e-3)
    render_single(env, p_vi, 100)


