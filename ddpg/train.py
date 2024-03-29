import sys
import os
import shutil
import argparse
import numpy as np

from utils import Utils

import tensorflow as tf

sys.path.append('..')
from env.rocketlander import get_state_sample
from env.constants import *


def train(env, agent, FLAGS):
    obs_size = env.observation_space.shape[0]

    util = Utils()
    state_samples = get_state_sample(samples=6000, normal_state=True)
    util.create_normalizer(state_sample=state_samples)

    for episode in range(1, FLAGS.num_episodes + 1):
        old_state = None
        done = False
        total_reward = 0

        state = env.reset()
        state = util.normalize(state)
        max_steps = 600

        for t in range(max_steps): # env.spec.max_episode_steps
            if FLAGS.show or episode % 10 == 0:
                env.refresh(render=True)

            old_state = state

            # infer an action
            action = agent.get_action(np.reshape(state, (1, obs_size)), not FLAGS.test)

            # take it
            state, reward, done, _ = env.step(action[0])
            state = util.normalize(state)
            total_reward += reward

            if not FLAGS.test:
                # update q vals
                agent.update(old_state, action[0], np.array(reward), state, done)

            if done:
                break

        agent.log_data(total_reward, episode)

        if episode % 100 == 0 and not FLAGS.test:
            print('Saved model at episode', episode)
            agent.save_model(episode)
        print("Episode:\t{0}Reward:\t{1}".format(episode, total_reward))

# Left here from the original code repo reference
def set_up():
    #print(f"Im here - 23")

    # Hide GPU from visible devices
    tf.config.set_visible_devices([], 'GPU')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--num_episodes',
        type=int,
        default=2000,
        help='How many episodes to train for'
    )

    parser.add_argument(
        '--show',
        default=False,
        action='store_true',
        help='At what point to render the cart environment'
    )

    parser.add_argument(
        '--wipe_logs',
        default=False,
        action='store_true',
        help='Wipe logs or not'
    )

    # not working correctly

    # parser.add_argument(
    #     '--log_dir',
    #     default='./logs',
    #     help='Where to store logs'
    # )

    # parser.add_argument(
    #     '--retrain',
    #     default=True, # changed to retrain
    #     action='store_true',
    #     help='Whether to start training from scratch again or not'
    # )

    parser.add_argument(
        '--test',
        default=False,
        action='store_true',
        help='Test more or no (true = no training updates)'
    )

    FLAGS, unparsed = parser.parse_known_args()

    if FLAGS.wipe_logs and os.path.exists(os.getcwd() + '/' + FLAGS.log_dir):
        shutil.rmtree(os.getcwd() + '/' + FLAGS.log_dir)

    return FLAGS
