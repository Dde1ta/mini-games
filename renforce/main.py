import os
import numpy as np
import tensorflow as tf

'''
Deep Q Learning

     2 networks (cnn):
     
        1) tell us an action
        2) To tell us the value of the action
'''


class DeepQNetwork(object):

    def __int__(self, alpha, n_actions, name, fc1_dims=256,
                input_dims=(210, 160, 4), save_dir="models/dpn/dump",
                chkpt_dir="models/dpn/checkpoint"):
        if not os.path.exists(save_dir):
            print("Making Dirs ....")
            os.makedirs(save_dir)
            os.makedirs(chkpt_dir)
            print("Maked Dirs ....")

        self.alpha = alpha
        self.action = n_actions
        self.name = name
        self.fc1_dims = fc1_dims
        self.input_dims = input_dims

        self.build_network()

        self.saver = tf.saved_model

        self.checkpoint_file = os.path.join(chkpt_dir, f"deepQnet{name}.chkpt")

        self.params = tf.get_collection

