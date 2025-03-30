# blackjack-rl

Reinforcement learning method for solving blackjack using Monte Carlo Control (MCC) in Python.

## Description

This repository contains a python implementation of the Monte Carlo Control (MCC) algorithm to learn an optimal policy for playing Blackjack. The agent learns by interacting with the Blackjack environment and updating its policy based on the rewards received. The implementation uses constant-alpha epsilon-greedy exploration.

## Installation

1.  **Prerequisites:**

    *   Python 3.x
    *   Jupyter Notebook
    *   Libraries: `numpy`, `matplotlib`

    You can install the necessary libraries using pip:

    ```bash
    pip install numpy matplotlib
    ```

2.  **Clone the repository:**

    ```bash
    git clone https://github.com/mattbailey1991/blackjack-rl.git
    cd blackjack-rl
    ```

3.  **Run the Jupyter Notebook:**

    ```bash
    jupyter notebook trainer.ipynb
    ```

## Key Features

*   **Monte Carlo Control (MCC):** Implements the MCC algorithm for learning the optimal Blackjack strategy.
*   **Epsilon-Greedy Exploration:** Uses epsilon-greedy exploration to balance exploration and exploitation.

## Training Performance Charts

![Image](https://github.com/user-attachments/assets/5114cd45-cc30-4bd4-aa19-540d4e2c95a0)

![Image](https://github.com/user-attachments/assets/7141377c-40cd-476e-a623-28ee13664add)
