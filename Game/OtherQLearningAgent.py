import numpy as np
import pickle
import random
import os

class OtherQLearningAgent:
    def __init__(self, game, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.game = game
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}
        self.visit_counts = {}
        self.training_progress = []

    def train(self, episodes=10000):
        for episode in range(episodes):
            self.game.reset(1)
            state = self.game.get_state()
            done = False
            total_reward = 0
            while not done:
                action = self.select_action(state)
                if action is None:
                    done = True
                    reward = -100
                else:
                    next_state, reward, done = self.game.step(action)
                    self.update_q_value(state, action, reward, next_state)
                    state = next_state
                total_reward += reward
            self.training_progress.append(total_reward)

    def select_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return self.random_action(state)
        return self.best_action(state)

    def random_action(self, state):
        actions = self.game.get_possible_actions(state)
        if not actions:
            return None
        return random.choice(actions)

    def best_action(self, state):
        actions = self.game.get_possible_actions(state)
        if not actions:
            return None
        q_values = [self.q_table.get((state, action), 0) for action in actions]
        return actions[np.argmax(q_values)]

    def update_q_value(self, state, action, reward, next_state):
        current_q = self.q_table.get((state, action), 0)
        max_future_q = max(
            [self.q_table.get((next_state, a), 0) for a in self.game.get_possible_actions(next_state)],
            default=0
        )
        self.q_table[(state, action)] = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)

    def save_model(self, filepath):
        # Load existing data if the file exists
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'rb') as f:
                other_existing_q_table, other_existing_visit_counts = pickle.load(f)
            # Update the existing data with the new data
            other_existing_q_table.update(self.q_table)
            other_existing_visit_counts.update(self.visit_counts)
        else:
            other_existing_q_table = self.q_table
            other_existing_visit_counts = self.visit_counts

        # Save the updated data
        with open(filepath, 'wb') as f:
            pickle.dump((other_existing_q_table, other_existing_visit_counts), f)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        with open(filepath, 'rb') as f:
            self.q_table, self.visit_counts = pickle.load(f)

    def plot_training_progress(self):
        import matplotlib.pyplot as plt
        plt.plot(self.training_progress)
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.title('Training Progress')
        plt.show()
