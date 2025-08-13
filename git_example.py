import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import collections
import time

# Suppress warnings for a cleaner output
tf.get_logger().setLevel('ERROR')


class Game2048:
    """
    A class to represent the 2048 game environment.
    The agent interacts with this class to play the game.
    """

    def __init__(self):
        self.grid_size = 4
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.score = 0
        self.game_over = False
        self._add_new_tile()
        self._add_new_tile()

    def reset(self):
        """Resets the game to its initial state."""
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.score = 0
        self.game_over = False
        self._add_new_tile()
        self._add_new_tile()
        return self.get_state()

    def _get_empty_tiles(self):
        """Returns a list of coordinates for all empty tiles (where value is 0)."""
        return list(zip(*np.where(self.grid == 0)))

    def _add_new_tile(self):
        """Adds a new tile (either 2 or 4) to a random empty spot on the grid."""
        empty_tiles = self._get_empty_tiles()
        if not empty_tiles:
            return

        row, col = empty_tiles[np.random.randint(0, len(empty_tiles))]
        self.grid[row, col] = 2 if np.random.rand() < 0.9 else 4

    def get_state(self):
        """
        Returns the current state of the game board.
        We use log2 of the tile values and normalize to help the neural network.
        A value of 0 on the board becomes 0 in the state.
        """
        # Replace zeros with ones for log operation, then set them back to zero
        grid_no_zeros = np.where(self.grid == 0, 1, self.grid)
        log_grid = np.log2(grid_no_zeros)
        # Normalize the state to be between 0 and 1
        # The max possible tile is theoretically infinite, but 65536 (2^16) is a reasonable upper bound
        normalized_grid = log_grid / 16.0
        return normalized_grid.flatten()  # Flatten the 4x4 grid to a 16-element vector

    def _compress(self, row):
        """Helper function to squeeze non-zero elements to the left."""
        new_row = [i for i in row if i != 0]
        new_row += [0] * (self.grid_size - len(new_row))
        return new_row

    def _merge(self, row):
        """Helper function to merge identical adjacent tiles and calculate score."""
        row = self._compress(row)
        merge_score = 0
        for i in range(self.grid_size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                merge_score += row[i]
        row = self._compress(row)
        return row, merge_score

    def _is_game_over(self):
        """Checks if there are any valid moves left."""
        temp_grid = self.grid.copy()
        for move in range(4):
            rotated_grid = np.rot90(temp_grid, k=move)
            for i in range(self.grid_size):
                row, _ = self._merge(rotated_grid[i])
                if list(row) != list(rotated_grid[i]):
                    return False  # A valid move was found
        return True  # No valid moves left

    def step(self, action):
        """
        Performs a game step based on the given action.
        Action mapping: 0: up, 1: right, 2: down, 3: left
        Returns: (next_state, reward, done)
        """
        original_grid = self.grid.copy()

        # Rotate the grid so we can always apply a 'left' merge logic
        rotated_grid = np.rot90(self.grid, k=action)

        current_move_score = 0
        for i in range(self.grid_size):
            row, merge_score = self._merge(rotated_grid[i])
            rotated_grid[i] = row
            current_move_score += merge_score

        # Rotate back to the original orientation
        self.grid = np.rot90(rotated_grid, k=4 - action)

        # Check if the move changed the board
        if not np.array_equal(original_grid, self.grid):
            self._add_new_tile()
            reward = float(current_move_score) if current_move_score > 0 else 1.0  # Reward for merging or just moving
            self.score += current_move_score
        else:
            reward = -2.0  # Penalize invalid moves

        if not self._get_empty_tiles() and self._is_game_over():
            self.game_over = True
            reward = -100.0  # Heavy penalty for losing

        done = self.game_over
        return self.get_state(), reward, done


class PPOAgent:
    """
    The PPO Agent class. It contains the actor-critic model and the training logic.
    """

    def __init__(self, state_dim, action_dim):
        # Hyperparameters
        self.gamma = 0.99  # Discount factor
        self.clip_ratio = 0.2  # PPO clipping parameter
        self.lambda_gae = 0.95  # Lambda for Generalized Advantage Estimation
        self.actor_lr = 0.0003  # Learning rate for the actor
        self.critic_lr = 0.001  # Learning rate for the critic
        self.train_epochs = 10  # Number of epochs to train on a batch of data
        self.batch_size = 64  # Minibatch size for training

        self.state_dim = state_dim
        self.action_dim = action_dim

        # Create Actor-Critic model
        self.model = self._build_actor_critic_model()
        self.actor_optimizer = keras.optimizers.Adam(learning_rate=self.actor_lr)
        self.critic_optimizer = keras.optimizers.Adam(learning_rate=self.critic_lr)

    def _build_actor_critic_model(self):
        """Builds the neural network for the Actor and Critic."""
        inputs = layers.Input(shape=(self.state_dim,))

        # Shared layers for feature extraction
        common = layers.Dense(128, activation="relu")(inputs)
        common = layers.Dense(128, activation="relu")(common)

        # Actor head: outputs action probabilities
        action_probs = layers.Dense(self.action_dim, activation="softmax", name="actor_output")(common)

        # Critic head: outputs the state value
        state_value = layers.Dense(1, name="critic_output")(common)

        model = keras.Model(inputs=inputs, outputs=[action_probs, state_value])
        return model

    def get_action_and_value(self, state):
        """
        Given a state, returns an action sampled from the policy and the state's value.
        """
        state_tensor = tf.convert_to_tensor(state)
        state_tensor = tf.expand_dims(state_tensor, 0)
        action_probs, state_value = self.model(state_tensor)

        # Sample an action from the probability distribution
        action = tf.random.categorical(tf.math.log(action_probs), 1)[0, 0].numpy()

        return action, action_probs[0, action].numpy(), state_value[0, 0].numpy()

    def _compute_advantages_and_returns(self, rewards, values, dones):
        """
        Computes advantages and returns using Generalized Advantage Estimation (GAE).
        """
        num_steps = len(rewards)
        advantages = np.zeros(num_steps, dtype=np.float32)
        last_advantage = 0

        # We need one more value for the last step's calculation
        # If the last step was a terminal state, its value is 0.
        last_value = values[-1] if dones[-1] else 0

        # Iterate backwards to calculate advantages
        for t in reversed(range(num_steps)):
            if dones[t]:
                delta = rewards[t] - values[t]
                last_advantage = delta
            else:
                delta = rewards[t] + self.gamma * values[t + 1] - values[t]
                last_advantage = delta + self.gamma * self.lambda_gae * last_advantage
            advantages[t] = last_advantage

        returns = advantages + values[:-1]  # The target for the critic
        return advantages, returns

    def train(self, memory):
        """Trains the agent using the collected experience."""
        # Unpack memory
        states, actions, old_probs, rewards, values, dones = memory

        # Compute advantages and returns
        advantages, returns = self._compute_advantages_and_returns(rewards, values, dones)

        # Normalize advantages
        advantages = (advantages - np.mean(advantages)) / (np.std(advantages) + 1e-8)

        # Prepare data for training
        states = np.array(states)
        actions = np.array(actions)
        old_probs = np.array(old_probs)

        # Train for multiple epochs
        for _ in range(self.train_epochs):
            indices = np.arange(len(states))
            np.random.shuffle(indices)

            for start in range(0, len(states), self.batch_size):
                end = start + self.batch_size
                batch_indices = indices[start:end]

                with tf.GradientTape() as actor_tape, tf.GradientTape() as critic_tape:
                    # Get data for the minibatch
                    batch_states = tf.convert_to_tensor(states[batch_indices])
                    batch_actions = tf.convert_to_tensor(actions[batch_indices], dtype=tf.int32)
                    batch_advantages = tf.convert_to_tensor(advantages[batch_indices])
                    batch_returns = tf.convert_to_tensor(returns[batch_indices])
                    batch_old_probs = tf.convert_to_tensor(old_probs[batch_indices])

                    # --- Actor Loss ---
                    action_probs, critic_values = self.model(batch_states)
                    action_indices = tf.stack([tf.range(len(batch_actions)), batch_actions], axis=1)
                    new_probs = tf.gather_nd(action_probs, action_indices)

                    ratio = new_probs / batch_old_probs

                    clipped_ratio = tf.clip_by_value(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
                    surrogate1 = ratio * batch_advantages
                    surrogate2 = clipped_ratio * batch_advantages

                    actor_loss = -tf.reduce_mean(tf.minimum(surrogate1, surrogate2))

                    # --- Critic Loss ---
                    critic_loss = tf.reduce_mean(tf.square(batch_returns - critic_values))

                # Apply gradients
                actor_grads = actor_tape.gradient(actor_loss, self.model.trainable_variables)
                critic_grads = critic_tape.gradient(critic_loss, self.model.trainable_variables)

                self.actor_optimizer.apply_gradients(zip(actor_grads, self.model.trainable_variables))
                self.critic_optimizer.apply_gradients(zip(critic_grads, self.model.trainable_variables))


# --- Main Training Loop ---
if __name__ == "__main__":
    # Initialization
    env = Game2048()
    state_dim = env.grid_size * env.grid_size
    action_dim = 4  # 4 possible moves
    agent = PPOAgent(state_dim, action_dim)

    # Training parameters
    total_timesteps = 200000
    timesteps_per_batch = 2048  # Number of steps to collect before training

    # Logging
    episode_count = 0
    total_score = 0
    max_tile_history = collections.deque(maxlen=100)
    score_history = collections.deque(maxlen=100)

    state = env.reset()
    start_time = time.time()

    for t in range(1, total_timesteps + 1):
        # Memory buffers for the batch
        states_mem, actions_mem, old_probs_mem, rewards_mem, values_mem, dones_mem = [], [], [], [], [], []

        for i in range(timesteps_per_batch):
            action, prob, value = agent.get_action_and_value(state)

            next_state, reward, done = env.step(action)

            # Store experience
            states_mem.append(state)
            actions_mem.append(action)
            old_probs_mem.append(prob)
            rewards_mem.append(reward)
            values_mem.append(value)
            dones_mem.append(done)

            state = next_state

            if done:
                episode_count += 1
                score_history.append(env.score)
                max_tile_history.append(np.max(env.grid))
                state = env.reset()

        # We need the value of the last state to compute advantages correctly
        _, _, last_value = agent.get_action_and_value(state)
        values_mem.append(last_value)

        # Train the agent
        memory = (states_mem, actions_mem, old_probs_mem, rewards_mem, values_mem, dones_mem)
        agent.train(memory)

        # Logging
        if t % timesteps_per_batch == 0:
            avg_score = np.mean(score_history) if score_history else 0
            avg_max_tile = np.mean(max_tile_history) if max_tile_history else 0
            time_elapsed = time.time() - start_time

            print(f"Timestep: {t}/{total_timesteps} | Episodes: {episode_count}")
            print(f"Avg Score (last 100): {avg_score:.2f} | Avg Max Tile (last 100): {avg_max_tile:.2f}")
            print(f"Time Elapsed: {time_elapsed:.2f}s")
            print("-" * 30)

    print("Training finished!")
