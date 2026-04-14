import matplotlib.pyplot as plt
import seaborn as sns

def plot_attack_distribution(y):
    plt.figure(figsize=(8, 5))
    sns.countplot(x=y, palette="viridis")
    plt.title("Distribution of Traffic Types")
    plt.xticks([0, 1], ['Normal (0)', 'Attack (1)'])
    plt.ylabel("Number of Samples")
    plt.savefig("outputs/attack_distribution.png") # Saves for your GitHub README!
    plt.show()