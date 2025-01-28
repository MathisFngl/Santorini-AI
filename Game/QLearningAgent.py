import numpy as np
import math
import matplotlib.pyplot as plt
import pickle
import os

class QLearningUCB:
    def __init__(self, game, alpha=0.02, gamma=0.95, c=0.6):
        self.game = game
        self.alpha = alpha # Learning rate parameter : higher values mean that the agent will learn faster
        self.gamma = gamma # Discount factor : higher values mean that the agent will care more about future rewards
        self.c = c # Exploration parameter : higher values mean that the agent will explore more
        self.q_table = {}
        self.visit_counts = {}
        self.rewards = []
        self.win_rate = []

        self.best_model = None
        self.best_reward = float('-inf')

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        max_q_next = max([self.get_q_value(next_state, a) for a in self.game.get_possible_actions(next_state)], default=0.0)
        current_q = self.get_q_value(state, action)
        new_q = current_q + self.alpha * (reward + self.gamma * max_q_next - current_q)
        self.q_table[(state, action)] = new_q

    def select_action(self, state):
        possible_actions = self.game.get_possible_actions(state)
        if not possible_actions:
            return None

        total_visits = sum(self.visit_counts.get((state, a), 0) for a in possible_actions)
        ucb_values = [
            self.get_q_value(state, a) + self.c * math.sqrt(math.log(total_visits + 1) / (self.visit_counts.get((state, a), 1)))
            for a in possible_actions
        ]
        return possible_actions[np.argmax(ucb_values)]

    def update_visit_counts(self, state, action):
        self.visit_counts[(state, action)] = self.visit_counts.get((state, action), 0) + 1

    def train(self, episodes):
        total_wins = 0
        for episode in range(episodes):
            print("game number : ", episode)
            state = self.game.reset(0)
            self.game.printBoard()
            done = False
            episode_reward = 0
            while not done:
                action = self.select_action(state)
                if action is None:
                    print("No valid actions left")
                    break
                next_state, reward, done = self.game.step(action)
                self.update_q_value(state, action, reward, next_state)
                self.update_visit_counts(state, action)
                print("Reward: ", reward)
                state = next_state
                episode_reward += reward
                if reward >= 1000:
                    total_wins += 1
            self.rewards.append(episode_reward)

            # Update best model if current episode reward is the best
            if episode_reward > self.best_reward:
                self.best_reward = episode_reward
                self.best_model = (self.q_table.copy(), self.visit_counts.copy())

            if (episode + 1) % 10 == 0:
                win_rate = total_wins / 10
                self.win_rate.append(win_rate)
                total_wins = 0
            self.c = max(self.c * 0.95, 0.1)  # Ensure c doesn't drop below 0.1
            #self.alpha = max(self.alpha * 0.95, 0.01)  # Ensure alpha doesn't drop below 0.01

    def plot_training_progress(self):
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(self.rewards)
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.title('Rewards over Episodes')

        plt.subplot(1, 2, 2)
        plt.plot(range(10, len(self.win_rate) * 10 + 1, 10), self.win_rate)
        plt.xlabel('Episode')
        plt.ylabel('Win Rate')
        plt.title('Win Rate over Episodes')

        plt.tight_layout()
        plt.show()


    def save_model(self, file_path):
        # Load existing data if the file exists
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'rb') as f:
                existing_q_table, existing_visit_counts = pickle.load(f)
            # Update the existing data with the new data
            existing_q_table.update(self.q_table)
            existing_visit_counts.update(self.visit_counts)
        else:
            existing_q_table = self.q_table
            existing_visit_counts = self.visit_counts

        # Save the updated data
        with open(file_path, 'wb') as f:
            pickle.dump((existing_q_table, existing_visit_counts), f)
        print(f"Model saved to {file_path}")

    def load_model(self, file_path):
        with open(file_path, 'rb') as f:
            self.q_table, self.visit_counts = pickle.load(f)
        print(f"Model loaded from {file_path}")